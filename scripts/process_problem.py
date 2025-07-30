import os
import datetime
import fileinput

def update_template(file_path):
    platform = "leetcode" if "leetcode" in file_path.lower() else "codeforces"
    problem_id = os.path.basename(file_path).split('_')[0]
    
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            print(line.replace('{date}', datetime.date.today().strftime("%Y-%m-%d"))
    
    print(f"Processed {file_path}")

if __name__ == "__main__":
    import sys
    update_template(sys.argv[1])
