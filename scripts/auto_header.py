import argparse
import datetime
import os

TEMPLATES = {
    ".py": ".templates/python_header.py",
    ".cpp": ".templates/cpp_header.cpp"
}

def generate_header(file_path):
    _, ext = os.path.splitext(file_path)
    template_path = TEMPLATES.get(ext)
    
    if not template_path or not os.path.exists(template_path):
        return
    
    with open(template_path) as f:
        template = f.read()
    
    placeholders = {
        "{current_date}": datetime.datetime.now().strftime("%Y-%m-%d"),
        "{platform}": "LeetCode",
        "{problem_id}": os.path.basename(file_path).split("_")[0],
        "{problem_name}": " ".join(os.path.basename(file_path).split("_")[1:-1]),
        "{time_complexity}": "n",
        "{space_complexity}": "1"
    }
    
    header = template
    for ph, value in placeholders.items():
        header = header.replace(ph, value)
    
    with open(file_path, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(header.rstrip("\r\n") + "\n\n" + content)
