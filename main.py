import subprocess

subprocess.run("python3 -u sentry/main.py & python3 -u buttler/main.py", shell=True)
