import subprocess


def start_app_py():
    print("hello world")
    # cmd_1 = ["poetry", "shell"]
    # subprocess.run(cmd_1)
    cmd_2 = ["python", "app.py"]
    subprocess.run(cmd_2)
