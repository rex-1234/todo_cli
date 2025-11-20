import subprocess
import json
import tempfile
import os

def test_cli_add_many():
    with tempfile.TemporaryDirectory() as tmp:
        tasks_file = os.path.join(tmp, "tasks.json")

        cmd = [
            "python", "main.py", "add-many",
            "--items", "A,2030-01-01", "B,2030-02-01"
        ]

        subprocess.run(cmd, check=True, cwd=os.getcwd())

        assert os.path.exists("tasks.json")

        with open("tasks.json") as f:
            data = json.load(f)

        titles = {t["title"] for t in data}
        assert titles >= {"A", "B"}
