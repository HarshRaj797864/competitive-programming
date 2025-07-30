# Converts solutions.json → README table
import json

with open("solutions.json") as f:
    stats = json.load(f)

table = "| Platform | Easy | Medium | Hard | Total |\n"
table += "|----------|------|--------|------|-------|\n"

for platform, data in stats.items():
    total = sum(data.values())
    table += f"| {platform} | {data.get('Easy',0)} | {data.get('Medium',0)} | {data.get('Hard',0)} | {total} |\n"

# Write to README.md
