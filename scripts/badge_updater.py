# Generate shields.io URLs with real-time counts
total = get_solution_count()
badge_url = f"https://img.shields.io/badge/Solved-{total}-brightgreen"
update_readme_badge(badge_url)
