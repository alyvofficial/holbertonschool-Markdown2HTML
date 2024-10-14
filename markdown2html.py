#!/usr/bin/python3
"""some script to start"""

import os
import sys

os.chmod(__file__, 0o755)  # Ensure the script is executable

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        sys.stderr.write(f"Missing {sys.argv[1]}\n")
        sys.exit(1)

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    lines_in_html = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # headings
        if line.startswith("#"):
            level = line.count("#")
            text = line.strip("#").strip()
            html = f"<h{level}>{text}</h{level}>\n"
            lines_in_html.append(html)
            i += 1

        # unordered lists
        elif line.startswith("-"):
            lines_in_html.append("<ul>\n")
            while i < len(lines) and lines[i].strip().startswith("-"):
                text = lines[i].strip("-").strip()
                html = f"<li>{text}</li>\n"
                lines_in_html.append(html)
                i += 1
            lines_in_html.append("</ul>\n")

        # ordered lists
        elif line.startswith("*"):
            lines_in_html.append("<ol>\n")
            while i < len(lines) and lines[i].strip().startswith("*"):
                text = lines[i].strip("*").strip()
                html = f"<li>{text}</li>\n"
                lines_in_html.append(html)
                i += 1
            lines_in_html.append("</ol>\n")

        else:
            lines_in_html.append(f"{line}\n")  # Ensure there's a newline after each line
            i += 1

    with open(sys.argv[2], 'w') as file:
        file.writelines(lines_in_html)

    # Optional: write a newline at the end of the file for good measure
    with open(sys.argv[2], 'a') as file:
        file.write('\n')
