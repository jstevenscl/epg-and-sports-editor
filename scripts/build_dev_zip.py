#!/usr/bin/env python3
"""Build a dev zip of EPG & Sports Editor for manual install on a test Dispatcharr.

Usage: python scripts/build_dev_zip.py [out_dir] [--manifest N] [--caps a,b,c]
  e.g. python scripts/build_dev_zip.py out
       python scripts/build_dev_zip.py out --manifest 2 --caps outbound_network,subprocess
  --manifest / --caps override manifest_version / capabilities in the zip's plugin.json
  ONLY (the repo's plugin.json is never touched), so v0 / v1 / v2 trials are one command.

Version follows the dev-build convention: LAST RELEASED version + .MMDDYYYY.HHMM suffix
(never a new semver for unreleased work). Release layout is flat: plugin.json, plugin.py,
logo.png. Does NOT touch the repo.
"""
import json
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
FILES = ["plugin.py", "logo.png"]


def main():
    args = sys.argv[1:]
    opts = {}
    for flag in ("--manifest", "--caps"):
        if flag in args:
            i = args.index(flag)
            opts[flag] = args[i + 1]
            del args[i:i + 2]
    out_dir = Path(args[0]) if args else ROOT
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    version = f"{manifest['version'].split('-')[0]}.{datetime.now():%m%d%Y.%H%M}"
    manifest["version"] = version
    if "--manifest" in opts:
        manifest["manifest_version"] = int(opts["--manifest"])
    if "--caps" in opts:
        manifest["capabilities"] = [c for c in opts["--caps"].split(",") if c]
    out = out_dir / f"epg-and-sports-editor-v{version}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in FILES:
            z.write(ROOT / f, f)
        z.writestr("plugin.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(out)
    print(version)


if __name__ == "__main__":
    main()
