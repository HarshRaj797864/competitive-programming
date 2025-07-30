.PHONY: help setup test testall clean header list install

# Default goal
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)🏆 Competitive Programming Automation$(RESET)"
	@echo "$(BLUE)======================================$(RESET)"
	@echo ""
	@echo "$(GREEN)Available commands:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-12s$(RESET) %s\n", $1, $2}'
	@echo ""
	@echo "$(GREEN)Examples:$(RESET)"
	@echo "  make setup PLATFORM=cf CONTEST=1500 PROBLEM=A NAME=\"Max Increase\""
	@echo "  make test DIR=platforms/Codeforces/1500/A"
	@echo "  make testall"
	@echo ""

install: ## Install and setup the automation tools
	@echo "$(BLUE)🔧 Installing competitive programming automation...$(RESET)"
	@chmod +x scripts/cp
	@chmod +x scripts/*.py
	@echo "$(GREEN)✅ Installation complete!$(RESET)"
	@echo ""
	@echo "$(YELLOW)You can now use:$(RESET)"
	@echo "  ./scripts/cp setup cf 1500 A"
	@echo "  ./scripts/cp test"
	@echo "  ./scripts/cp quick"
	@echo ""
	@echo "$(YELLOW)Or add scripts/ to your PATH for global access$(RESET)"

setup: ## Setup a new problem (requires PLATFORM, CONTEST, PROBLEM)
	@if [ -z "$(PLATFORM)" ] || [ -z "$(CONTEST)" ] || [ -z "$(PROBLEM)" ]; then \
		echo "$(RED)❌ Error: Missing required parameters$(RESET)"; \
		echo "Usage: make setup PLATFORM=<platform> CONTEST=<contest> PROBLEM=<problem> [NAME=<name>]"; \
		echo "Example: make setup PLATFORM=cf CONTEST=1500 PROBLEM=A NAME=\"Maximum Increase\""; \
		exit 1; \
	fi
	@echo "$(BLUE)🚀 Setting up problem: $(PLATFORM)/$(CONTEST)/$(PROBLEM)$(RESET)"
	@python3 scripts/setup_problem.py $(PLATFORM) $(CONTEST) $(PROBLEM) $(if $(NAME),--name "$(NAME)") $(if $(URL),--url "$(URL)")

test: ## Test a specific problem (requires DIR)
	@if [ -z "$(DIR)" ]; then \
		echo "$(RED)❌ Error: DIR parameter required$(RESET)"; \
		echo "Usage: make test DIR=<problem_directory>"; \
		echo "Example: make test DIR=platforms/Codeforces/1500/A"; \
		exit 1; \
	fi
	@echo "$(BLUE)🧪 Testing: $(DIR)$(RESET)"
	@python3 scripts/test_solution.py "$(DIR)"

testcurrent: ## Test solutions in current directory
	@echo "$(BLUE)🧪 Testing current directory...$(RESET)"
	@if ls *.cpp *.py *.java Solution.java 2>/dev/null | grep -q .; then \
		python3 scripts/test_solution.py "$(pwd)"; \
	else \
		echo "$(RED)❌ No solution files found in current directory$(RESET)"; \
	fi

testall: ## Test all problems in the repository
	@echo "$(BLUE)🧪 Testing all problems...$(RESET)"
	@find platforms -name "solution.*" -o -name "Solution.java" | \
		sed 's|/[^/]*$||' | sort -u | \
		while read dir; do \
			echo "$(YELLOW)Testing: $dir$(RESET)"; \
			python3 scripts/test_solution.py "$dir" || true; \
			echo ""; \
		done

header: ## Add headers to files (requires DIR, optional AUTHOR)
	@if [ -z "$(DIR)" ]; then \
		echo "$(RED)❌ Error: DIR parameter required$(RESET)"; \
		echo "Usage: make header DIR=<directory> [AUTHOR=<name>]"; \
		exit 1; \
	fi
	@echo "$(BLUE)📝 Adding headers to: $(DIR)$(RESET)"
	@python3 scripts/auto_header.py "$(DIR)" $(if $(AUTHOR),--author "$(AUTHOR)")

list: ## List all problems or problems for a platform (optional PLATFORM)
	@if [ -n "$(PLATFORM)" ]; then \
		echo "$(BLUE)📋 Problems in $(PLATFORM):$(RESET)"; \
		find platforms/$(PLATFORM) -name "solution.*" -o -name "Solution.java" 2>/dev/null | \
			sed 's|platforms/$(PLATFORM)/||' | sed 's|/[^/]*$||' | sort -u | nl; \
	else \
		echo "$(BLUE)📋 Available platforms:$(RESET)"; \
		ls -1 platforms/ 2>/dev/null | nl; \
	fi

clean: ## Clean compiled files and temporary files
	@echo "$(BLUE)🧹 Cleaning compiled files...$(RESET)"
	@find . -name "solution" -type f -delete 2>/dev/null || true
	@find . -name "*.class" -delete 2>/dev/null || true
	@find . -name "*.exe" -delete 2>/dev/null || true
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete$(RESET)"

stats: ## Show repository statistics
	@echo "$(BLUE)📊 Repository Statistics$(RESET)"
	@echo "$(BLUE)========================$(RESET)"
	@echo ""
	@echo "$(YELLOW)Platforms:$(RESET)"
	@ls -1 platforms/ 2>/dev/null | wc -l | xargs echo "  Total platforms:"
	@echo ""
	@echo "$(YELLOW)Problems by platform:$(RESET)"
	@for platform in $(ls platforms/ 2>/dev/null); do \
		count=$(find platforms/$platform -name "solution.*" -o -name "Solution.java" 2>/dev/null | wc -l); \
		echo "  $platform: $count problems"; \
	done
	@echo ""
	@echo "$(YELLOW)Language distribution:$(RESET)"
	@echo -n "  C++: "; find platforms -name "*.cpp" 2>/dev/null | wc -l
	@echo -n "  Python: "; find platforms -name "*.py" 2>/dev/null | wc -l  
	@echo -n "  Java: "; find platforms -name "*.java" 2>/dev/null | wc -l

quick: ## Interactive problem setup
	@echo "$(BLUE)🚀 Quick Problem Setup$(RESET)"
	@python3 scripts/quick_commands.py setup

# Platform-specific shortcuts
cf: ## Quick Codeforces setup (requires CONTEST, PROBLEM)
	@$(MAKE) setup PLATFORM=cf CONTEST=$(CONTEST) PROBLEM=$(PROBLEM) NAME="$(NAME)"

ac: ## Quick AtCoder setup (requires CONTEST, PROBLEM)
	@$(MAKE) setup PLATFORM=ac CONTEST=$(CONTEST) PROBLEM=$(PROBLEM) NAME="$(NAME)"

lc: ## Quick LeetCode setup (requires CONTEST, PROBLEM)
	@$(MAKE) setup PLATFORM=lc CONTEST=$(CONTEST) PROBLEM=$(PROBLEM) NAME="$(NAME)"
