"""
Q1 - Campus Merit Analyzer using Compound Data Structures
Python 3.10+
Input:
n k m
enrollment name semester cpi mark1 ... markm
"""
from collections import defaultdict
import sys


def solve(data: str) -> str:
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Input is empty.")

    n, k, m = map(int, lines[0].split())
    if not (1 <= n <= 100000 and 1 <= k <= 50 and 1 <= m <= 12):
        raise ValueError("n, k or m is outside the allowed range.")

    records = []
    by_semester = defaultdict(list)
    subject_top = defaultdict(list)

    if len(lines) != n + 1:
        raise ValueError("Number of student records does not match n.")

    for line_no, line in enumerate(lines[1:], 2):
        parts = line.split()
        if len(parts) != 4 + m:
            raise ValueError(f"Invalid record at input line {line_no}.")

        enrollment, name = parts[0], parts[1]
        semester = int(parts[2])
        cpi = float(parts[3])
        marks = tuple(map(int, parts[4:]))

        if not 1 <= semester <= 8:
            raise ValueError("Semester must be between 1 and 8.")
        if not 0.0 <= cpi <= 10.0:
            raise ValueError("CPI must be between 0 and 10.")
        if any(not 0 <= x <= 100 for x in marks):
            raise ValueError("Marks must be between 0 and 100.")

        record = {
            "enrollment": enrollment,
            "name": name,
            "semester": semester,
            "cpi": cpi,
            "marks": marks,
            "average": sum(marks) / m,
        }
        records.append(record)
        by_semester[semester].append(record)

    # CPI descending, average marks descending, enrollment ascending.
    output = []
    for semester in sorted(by_semester):
        ranked = sorted(
            by_semester[semester],
            key=lambda r: (-r["cpi"], -r["average"], r["enrollment"])
        )
        output.append(f"Semester {semester}: " +
                      " ".join(r["enrollment"] for r in ranked[:k]))

    # Keep every enrollment tied for the highest mark.
    for subject in range(m):
        highest = max(r["marks"][subject] for r in records)
        toppers = sorted(
            r["enrollment"] for r in records if r["marks"][subject] == highest
        )
        output.append(f"S{subject + 1}: " + " ".join(toppers))

    return "\n".join(output)


def main() -> None:
    try:
        print(solve(sys.stdin.read()))
    except (ValueError, IndexError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
