"""
Q2 - Optimized Password Audit using Aho-Corasick
Python 3.10+
"""

from collections import deque
import re
import sys


class AhoCorasick:
    def __init__(self, words):
        self.next = [{}]
        self.fail = [0]
        self.output = [False]

        for word in words:
            node = 0
            for ch in word.lower():
                if ch not in self.next[node]:
                    self.next[node][ch] = len(self.next)
                    self.next.append({})
                    self.fail.append(0)
                    self.output.append(False)
                node = self.next[node][ch]
            self.output[node] = True

        queue = deque()
        for child in self.next[0].values():
            queue.append(child)

        while queue:
            node = queue.popleft()
            for ch, child in self.next[node].items():
                queue.append(child)
                f = self.fail[node]
                while f and ch not in self.next[f]:
                    f = self.fail[f]
                self.fail[child] = self.next[f].get(ch, 0)
                self.output[child] |= self.output[self.fail[child]]

    def contains_banned(self, text):
        node = 0
        for ch in text.lower():
            while node and ch not in self.next[node]:
                node = self.fail[node]
            node = self.next[node].get(ch, 0)
            if self.output[node]:
                return True
        return False


def repeated_more_than_three(password):
    count = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1
            if count > 3:
                return True
        else:
            count = 1
    return False


def classify(password, matcher):
    # Classification precedence follows the assignment categories:
    # length -> pattern -> compromised -> strong.
    if not 6 <= len(password) <= 12:
        return "WEAK_LENGTH"

    pattern_ok = (
        re.search(r"[a-z]", password) is not None
        and re.search(r"[A-Z]", password) is not None
        and re.search(r"\d", password) is not None
        and re.search(r"[$#@]", password) is not None
    )
    if not pattern_ok or repeated_more_than_three(password):
        return "WEAK_PATTERN"

    if matcher.contains_banned(password):
        return "COMPROMISED"

    return "STRONG"


def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        raise ValueError("Input is empty.")

    pos = 0
    b = int(lines[pos].strip())
    pos += 1
    banned = [lines[pos + i].strip() for i in range(b)]
    pos += b

    n = int(lines[pos].strip())
    pos += 1
    if len(lines) - pos < n:
        raise ValueError("Not enough password lines.")

    passwords = lines[pos:pos + n]
    matcher = AhoCorasick(word for word in banned if word)

    for i, password in enumerate(passwords, 1):
        print(f"{i}: {classify(password, matcher)}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, IndexError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
