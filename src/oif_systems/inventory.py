from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def validate_inventory(data: Any) -> list[str]:
    if not isinstance(data, dict): return ["inventory must be an object"]
    errors = [f"missing field: {k}" for k in ("host_id", "observed_at", "operating_system", "hardware", "software") if k not in data]
    if errors: return errors
    if not isinstance(data["software"], list): return ["software must be an array"]
    seen=set()
    for i,item in enumerate(data["software"]):
        if not isinstance(item,dict) or not all(isinstance(item.get(k),str) and item[k] for k in ("name","version")): errors.append(f"software[{i}] requires name and version"); continue
        key=item["name"].casefold()
        if key in seen: errors.append(f"duplicate software name: {item['name']}")
        seen.add(key)
    return errors

def compare_snapshots(before: dict, after: dict) -> dict:
    old={x["name"].casefold():x for x in before.get("software",[])}; new={x["name"].casefold():x for x in after.get("software",[])}
    return {"added":[{"name":new[k]["name"],"version":new[k]["version"]} for k in sorted(new.keys()-old.keys())],"removed":[{"name":old[k]["name"],"version":old[k]["version"]} for k in sorted(old.keys()-new.keys())],"changed":[{"name":new[k]["name"],"from":old[k]["version"],"to":new[k]["version"]} for k in sorted(old.keys()&new.keys()) if old[k]["version"]!=new[k]["version"]]}

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("before",type=Path); p.add_argument("after",type=Path); a=p.parse_args()
    before=json.loads(a.before.read_text()); after=json.loads(a.after.read_text()); errors=validate_inventory(before)+validate_inventory(after)
    if errors: p.error("; ".join(errors))
    print(json.dumps(compare_snapshots(before,after),indent=2,sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
