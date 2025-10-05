#!/usr/bin/env python3
"""
Sort an input file (e.g. emoji.dict.yaml) using Unicode CLDR order given in emoji-test.txt.

emoji-test.txt can be downloaded from https://www.unicode.org/Public/emoji/latest/emoji-test.txt

Usage:
  python sort_emoji.py emoji-test.txt emoji.dict.yaml emoji_sorted.dict.yaml
"""
import argparse
import sys

def load_emoji_order(emoji_test_path, encoding="utf-8"):
    """Return {emoji: index} in the order they appear in emoji-test.txt."""
    order = []
    with open(emoji_test_path, encoding=encoding) as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            if "#" in line:
                right = line.split("#", 1)[1].strip()
                if right:
                    first_token = right.split()[0]
                    order.append(first_token)
    return {e: i for i, e in enumerate(order)}

def find_first_emoji_index(line, order_map, maxlen):
    """Scan the line for the first substring (prefer longest) that exists in order_map.
    Returns a numeric index from order_map, or float('inf') if none found."""
    n = len(line)
    if n == 0 or not order_map:
        return float("inf")
    for pos in range(n):
        limit = min(maxlen, n - pos)
        for L in range(limit, 0, -1):
            cand = line[pos:pos + L]
            if cand in order_map:
                return order_map[cand]
    return float("inf")

def sort_file(emoji_test_path, input_path, output_path, encoding="utf-8"):
    order_map = load_emoji_order(emoji_test_path, encoding=encoding)
    maxlen = max((len(k) for k in order_map.keys()), default=0)
    with open(input_path, encoding=encoding) as fh:
        lines = fh.readlines()
    sorted_lines = sorted(lines, key=lambda ln: find_first_emoji_index(ln, order_map, maxlen))
    with open(output_path, "w", encoding=encoding) as fh:
        fh.writelines(sorted_lines)

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="Sort a file using CLDR emoji order from emoji-test.txt")
    p.add_argument("emoji_test", help="Path to emoji-test.txt from Unicode")
    p.add_argument("input", help="Input file to sort (e.g. emoji.dict.yaml)")
    p.add_argument("output", help="Output sorted file")
    p.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")
    args = p.parse_args(argv)
    sort_file(args.emoji_test, args.input, args.output, encoding=args.encoding)

if __name__ == "__main__":
    sys.exit(main())
