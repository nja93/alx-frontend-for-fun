#!/usr/bin/python3
"""Markdown to HTML"""

import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    # Args handling
    # confirming the correct number of arguments
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    # confirm that the file exists 
    # if empty display a stderr and exit
    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    # FILE PROCESSING SECTION
    # CONTENTS read line by line 
    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            unordered_start, ordered_start, paragraph = False, False, False
            # bold Markdown to html
            for line in read:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # Find content inside double square brackets
                content_in_brackets = re.findall(r'\[\[(.+?)\]\]', line)
                if content_in_brackets:
                # Calculate the MD5 hash of the content inside brackets
                    hashed_content = hashlib.md5(content_in_brackets[0].encode()).hexdigest()
                    line = line.replace('[[' + content_in_brackets[0] + ']]', hashed_content)

                # Removing occurrences of the letter 'C' within double parentheses
                parentheses_content = re.findall(r'\(\(.+?\)\)', line)
                content_to_modify = re.findall(r'\(\((.+?)\)\)', line)

                if parentheses_content:
                    modified_content = ''.join(
                        char for char in content_to_modify[0] if char.lower() != 'c'
                    )
                    line = line.replace(parentheses_content[0], modified_content)


                length = len(line)
                headings = line.lstrip('#')
                heading_num = length - len(headings)
                unordered = line.lstrip('-')
                unordered_num = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_num = length - len(ordered)
                

                # headings and lists
                if 1 <= heading_num <= 6:
                    line = '<h{}>'.format(
                        heading_num) + headings.strip() + '</h{}>\n'.format(
                        heading_num)

                if unordered_num:
                    if not unordered_start:
                        html.write('<ul>\n')
                        unordered_start = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if unordered_start and not unordered_num:
                    html.write('</ul>\n')
                    unordered_start = False

                if ordered_num:
                    if not ordered_start:
                        html.write('<ol>\n')
                        ordered_start = True
                    line = '<li>' + ordered.strip() + '</li>\n'
                if ordered_start and not ordered_num:
                    html.write('</ol>\n')
                    ordered_start = False

                # if line does not match headings,lists, paragrahs,
                # it gets written as is into html file
                if not (heading_num or unordered_start or ordered_start):
                    if not paragraph and length > 1:
                        html.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        html.write('<br/>\n')
                    elif paragraph:
                        html.write('</p>\n')
                        paragraph = False

                if length > 1:
                    html.write(line)
            # CLOSE at end of processing
            if unordered_start:
                html.write('</ul>\n')
            if ordered_start:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')
    exit(0)