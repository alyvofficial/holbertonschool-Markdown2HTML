#!/usr/bin/python3
"""
This script converts Markdown to HTML.
"""

import os
import sys
import re

# Ensure the script is executable
os.chmod(__file__, 0o755)

if __name__ == '__main__':
    # Test if the number of arguments passed is 2
    if len(sys.argv) != 3:
        print('Usage: ./markdown2html.py README.md README.html', 
              file=sys.stderr)
        sys.exit(1)

    # Store the arguments into variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the markdown file exists and is a file
    if not os.path.isfile(input_file):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    # Read the markdown file
    with open(input_file, 'r', encoding='utf-8') as file_1:
        html_content = []
        for line in file_1:
            line = line.rstrip()  # Remove trailing newlines
            heading = re.match(r'^(#{1,6}) (.*)', line)  # Match headings

            if heading:
                h_level = len(heading.group(1))  # Number of #
                content = heading.group(2)  # Heading content
                html_content.append(
                    f'<h{h_level}>{content}</h{h_level}>\n'
                )
            else:
                # Add paragraph or other content
                html_content.append(f'<p>{line}</p>\n')

    # Write the converted HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as file_2:
        file_2.writelines(html_content)

    # Ensure a newline at the end of the file
    file_2.write('\n')

    sys.exit(0)
