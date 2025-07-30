import os
import json
from collections import defaultdict

stats = defaultdict(lambda: defaultdict(int))

for root, _, files in os.walk("platforms"):
    for file in files:
        if file.endswith(".py") or file.endswith(".cpp"):
            path = os.path.join(root, file)
            with open(path) as f:
                header = f.read().split('"""')[1]
                # Extract metadata
                # Update stats[platform][difficulty] += 1

with open("solutions.json", "w") as f:
    json.dump(stats, f)

if total_solved > 100 and not '100_solved' in unlocked:
    add_achievement("🏆 Reached 100 solutions")
