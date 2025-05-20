from user_bot import get_groups_dict
import asyncio
import json
import os

CONFIG_FILE = "groups_config.json"

async def fetch_and_cache_groups():
    groups = await get_groups_dict()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)
    return groups

def load_groups_from_file():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

async def main():
    groups = load_groups_from_file()
    if groups is None:
        groups = await fetch_and_cache_groups()
    return groups

if __name__ == "__main__":
    my = asyncio.run(main())
    for key, val in my.items():
        print(key, "-", val)
