from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def scan_folder(root: Path, store: Path) -> dict[str, dict[str, int]]:
    root = root.resolve()
    store = store.resolve()
    files: dict[str, dict[str, int]] = {}
    for current, dirs, names in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [name for name in dirs if not (current_path / name).is_symlink()]
        for name in names:
            path = current_path / name
            if path.is_symlink() or path.resolve() == store:
                continue
            try:
                info = path.stat()
            except OSError:
                continue
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            files[relative] = {"size": info.st_size, "mtime_ns": info.st_mtime_ns}
    return files


def load_history(store: Path) -> dict[str, object]:
    if not store.exists():
        return {"snapshots": []}
    data = json.loads(store.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("snapshots"), list):
        raise ValueError("History file has an invalid format")
    return data


def save_snapshot(root: Path, store: Path) -> dict[str, object]:
    if not root.is_dir():
        raise NotADirectoryError(f"Not a folder: {root}")
    history = load_history(store)
    snapshot = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root.resolve()),
        "files": scan_folder(root, store),
    }
    history["snapshots"].append(snapshot)
    store.parent.mkdir(parents=True, exist_ok=True)
    temporary = store.with_name(store.name + ".tmp")
    temporary.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    temporary.replace(store)
    return snapshot


def compare(history: dict[str, object]) -> dict[str, object]:
    snapshots = history["snapshots"]
    if len(snapshots) < 2:
        return {"ready": False, "message": "Take at least two snapshots to compare folder growth."}
    before = snapshots[-2]["files"]
    after = snapshots[-1]["files"]
    before_total = sum(item["size"] for item in before.values())
    after_total = sum(item["size"] for item in after.values())
    new = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = []
    for name in sorted(set(before) & set(after)):
        delta = after[name]["size"] - before[name]["size"]
        if delta:
            changed.append({"path": name, "delta": delta})
    changed.sort(key=lambda item: abs(item["delta"]), reverse=True)
    return {"ready": True, "before_total": before_total, "after_total": after_total,
            "delta": after_total - before_total, "new": new, "removed": removed, "changed": changed[:10]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Track folder size changes using metadata-only snapshots.")
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot", help="Record a folder snapshot")
    snap.add_argument("folder", type=Path)
    snap.add_argument("--store", type=Path, default=Path(".folder-growth.json"))
    report = sub.add_parser("report", help="Compare the two newest snapshots")
    report.add_argument("--store", type=Path, default=Path(".folder-growth.json"))
    args = parser.parse_args()
    try:
        if args.command == "snapshot":
            result = save_snapshot(args.folder, args.store)
            total = sum(item["size"] for item in result["files"].values())
            print(f"Saved snapshot: {len(result['files'])} file(s), {total} bytes")
        else:
            result = compare(load_history(args.store))
            if not result["ready"]:
                print(result["message"])
                return
            print(f"Total size: {result['before_total']:,} -> {result['after_total']:,} bytes ({result['delta']:+,})")
            print(f"New files: {len(result['new'])}; removed files: {len(result['removed'])}")
            for item in result["changed"]:
                print(f"  {item['delta']:+,}  {item['path']}")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(2, f"Error: {error}\n")

if __name__ == "__main__":
    main()
