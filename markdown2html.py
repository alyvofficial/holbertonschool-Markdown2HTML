#!/usr/bin/python3
"""Some script to convert Markdown to HTML"""

import os
import sys
import re
import hashlib


# Ensure the script is executable
os.chmod(__file__, 0o755)


def convert_bold_and_emphasis(text):
    """Convert markdown bold and emphasis to HTML."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text


def convert_md5(text):
    """Convert text inside [[ ]] to its MD5 hash."""
    return re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), text)


def remove_c(text):
    """Remove all 'c' (case insensitive) from text inside (( ))."""
    return re.sub(r'\(\((.*?)\)\)', lambda match: match.group(1).replace('c', '').replace('C', ''), text)


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
    in_ul = False
    in_ol = False

    for line in lines:
        stripped_line = line.strip()
        stripped_line = convert_bold_and_emphasis(stripped_line)
        stripped_line = convert_md5(stripped_line)
        stripped_line = remove_c(stripped_line)

        # Process headings
        if stripped_line.startswith("#"):
            level = stripped_line.count("#")
            text = stripped_line.strip("#").strip()
            html = f"<h{level}>{text}</h{level}>\n"
            lines_in_html.append(html)

        # Process unordered lists
        elif stripped_line.startswith("-"):
            if in_ol:
                lines_in_html.append("</ol>\n")
                in_ol = False
            if not in_ul:
                lines_in_html.append("<ul>\n")
                in_ul = True
            text = stripped_line.strip("-").strip()
            lines_in_html.append(f"<li>{text}</li>\n")

        # Process ordered lists
        elif stripped_line.startswith("*"):
            if in_ul:
                lines_in_html.append("</ul>\n")
                in_ul = False
            if not in_ol:
                lines_in_html.append("<ol>\n")
                in_ol = True
            text = stripped_line.strip("*").strip()
            lines_in_html.append(f"<li>{text}</li>\n")

        # Process empty lines (indicating end of a paragraph)
        elif not stripped_line:
            if current_paragraph:
                lines_in_html.append("<p>\n")
                lines_in_html.append("<br />\n".join(current_paragraph))
                lines_in_html.append("</p>\n")
                current_paragraph = []
            if in_ul:
                lines_in_html.append("</ul>\n")
                in_ul = False
            if in_ol:
                lines_in_html.append("</ol>\n")
                in_ol = False

        # Process regular text
        else:
            current_paragraph.append(stripped_line)

    # Close any remaining paragraph
    if current_paragraph:
        lines_in_html.append("<p>\n")
        lines_in_html.append("<br />\n".join(current_paragraph))
        lines_in_html.append("</p>\n")
    if in_ul:
        lines_in_html.append("</ul>\n")
    if in_ol:
        lines_in_html.append("</ol>\n")

    with open(sys.argv[2], 'w') as file:
        file.writelines(lines_in_html)

    # Optional: write a newline at the end of the file for good measure
    with open(sys.argv[2], 'a') as file:
        file.write('\n')
