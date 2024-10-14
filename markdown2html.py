#!/usr/bin/python3
import sys
import os

if __name__ == "__main__":
    # Check if the number of arguments is less than 3 (script name + 2 arguments)
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    # Assign the arguments to variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # No errors, so exit successfully
    sys.exit(0)
