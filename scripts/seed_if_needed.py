import os
import subprocess
import sys

def run(cmd: list[str]):
    print("Running:", " ".join(cmd), flush=True)
    subprocess.check_call(cmd)

if os.getenv("SEED_DB") == "1":
    # migrate first
    run([sys.executable, "manage.py", "migrate"])
    # load fixture
    run([sys.executable, "manage.py", "loaddata", "seed.json"])
    print(" Seed complete. Remove SEED_DB env var now.", flush=True)
else:
    run([sys.executable, "manage.py", "migrate"])
