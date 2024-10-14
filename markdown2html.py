#!/usr/bin/python3
"""Some script to convert Markdown to HTML"""

import os
import sys

# Ensure the script is executable
os.chmod(__file__, 0o755)

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
    current_paragraph = []

    for line in lines:
        stripped_line = line.strip()

        # Process headings
        if stripped_line.startswith("#"):
            level = stripped_line.count("#")
            text = stripped_line.strip("#").strip()
            html = f"<h{level}>{text}</h{level}>\n"
            lines_in_html.append(html)

        # Process unordered lists
        elif stripped_line.startswith("-"):
            if current_paragraph:
                # Close current paragraph if it exists
                lines_in_html.append("<p>\n")
                lines_in_html.append("<br />\n".join(current_paragraph))
                lines_in_html.append("</p>\n")
                current_paragraph = []
            lines_in_html.append("<ul>\n")
            text = stripped_line.strip("-").strip()
            lines_in_html.append(f"<li>{text}</li>\n")

        # Process ordered lists (if needed, you can extend this)
        elif stripped_line.startswith("*"):
            if current_paragraph:
                lines_in_html.append("<p>\n")
                lines_in_html.append("<br />\n".join(current_paragraph))
                lines_in_html.append("</p>\n")
                current_paragraph = []
            lines_in_html.append("<ol>\n")
            text = stripped_line.strip("*").strip()
            lines_in_html.append(f"<li>{text}</li>\n")

        # Process empty lines (indicating end of a paragraph)
        elif not stripped_line:
            if current_paragraph:
                lines_in_html.append("<p>\n")
                lines_in_html.append("<br />\n".join(current_paragraph))
                lines_in_html.append("</p>\n")
                current_paragraph = []

        # Process regular text
        else:
            current_paragraph.append(stripped_line)

    # Close any remaining paragraph
    if current_paragraph:
        lines_in_html.append("<p>\n")
        lines_in_html.append("<br />\n".join(current_paragraph))
        lines_in_html.append("</p>\n")

    with open(sys.argv[2], 'w') as file:
        file.writelines(lines_in_html)

    # Optional: write a newline at the end of the file for good measure
    with open(sys.argv[2], 'a') as file:
        file.write('\n')
