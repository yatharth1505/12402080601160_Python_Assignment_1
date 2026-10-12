"""
Q8 - Compressed Log Index using Pickle and Zip

BUILD:
    python Q8_compressed_log_index.py
    BUILD logs archive.zip

SEARCH:
    python Q8_compressed_log_index.py
    SEARCH archive.zip.index.pkl 3 error timeout login

The BUILD mode also places the pickle index inside the requested zip archive.
"""
import pickle
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def build_index(folder, archive):
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError("Folder does not exist.")

    index = defaultdict(list)
    files = sorted(p for p in folder.rglob("*") if p.is_file())
    total_lines = 0

    for path in files:
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                for line_no, line in enumerate(handle, 1):
                    total_lines += 1
                    tokens = set(TOKEN_RE.findall(line.lower()))
                    for token in tokens:
                        # Store paths relative to the scanned folder.
                        rel = str(path.relative_to(folder))
                        index[token].append((rel, line_no))
        except OSError:
            continue

    index = dict(index)
    pickle_name = Path(str(archive) + ".index.pkl")
    with pickle_name.open("wb") as handle:
        pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Compress original logs and index together.
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(pickle_name, arcname=pickle_name.name)
        for path in files:
            zf.write(path, arcname=str(Path("logs") / path.relative_to(folder)))

    print(f"FILES {len(files)}")
    print(f"LINES {total_lines}")
    print(f"TOKENS {len(index)}")
    print(f"INDEX {pickle_name}")


def search_index(pickle_path, tokens):
    with open(pickle_path, "rb") as handle:
        index = pickle.load(handle)

    for token in tokens:
        normalized = token.lower()
        print(f"{token}:")
        for filename, line_no in index.get(normalized, []):
            print(f"{filename}:{line_no}")


def main():
    args = sys.stdin.read().split()
    if not args:
        print("Provide BUILD or SEARCH input.", file=sys.stderr)
        sys.exit(1)

    mode = args[0].upper()
    try:
        if mode == "BUILD" and len(args) == 3:
            build_index(args[1], args[2])
        elif mode == "SEARCH" and len(args) >= 3:
            search_index(args[1], args[2:])
        else:
            raise ValueError("BUILD requires folder and zip; SEARCH requires pickle and tokens.")
    except (OSError, ValueError, pickle.PickleError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
