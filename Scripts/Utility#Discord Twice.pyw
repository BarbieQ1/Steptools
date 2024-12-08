import os
import glob
import subprocess

discord_path = os.path.join(os.getenv("LOCALAPPDATA"), "Discord")
latest_version = ""

if os.path.exists(discord_path):
    versions = [os.path.basename(path).replace("app-", "") for path in glob.glob(f"{discord_path}/app-*")]
    latest_version = max(versions, default="") if versions else ""

if latest_version:
    discord_exe = os.path.join(discord_path, f"app-{latest_version}", "Discord.exe")
    if os.path.exists(discord_exe):
        subprocess.Popen([discord_exe, "--multi-instance"], shell=True)
    else:
        print(f"Discord executable not found for version {latest_version}")
        input("Press Enter to continue...")
else:
    print(f"Discord is not installed in {discord_path}")
    input("Press Enter to continue...")
