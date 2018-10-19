# -*- coding: utf-8 -*-

# program that opens all txt files in specified working directory and deletes trailing hyphens
import re
import os
import sys
import fileinput
from collections import defaultdict

#removes whitespace in beginning of line
whitespacePattern = re.compile(r'^(\s)+', re.M)

# specifies the greedy trailing hyphen pattern with a whitespacecharacter in the end
greedyPattern = re.compile(r'(-\n(\s)*)', re.M)
pattern = re.compile(r'(-(\s)+(\d)+(\n)(\s)?)', re.M)

screen = sys.stdout


def parser(doc):
    for line in doc:
        match1 = whitespacePattern.search(line)
        match2 = greedyPattern.search(line)
        match3 = pattern.search(line)

        # Test this condition always to avoid string conversions from "ge-    hen" to  "ge    hen"
        if match1:
            try:
                replacedline = (re.sub(whitespacePattern, r'', line, re.M))
                line = replacedline
            except UnicodeDecodeError:
                pass
            except Exception as e:
                print(e)

        if match2:
            try:
                replacedline = (re.sub(greedyPattern, r'', line, re.M))
            except UnicodeDecodeError:
                pass
            except Exception as e:
                print(e)
        elif match3:
            try:
                replacedline = (re.sub(pattern, r'', line, re.M))
            except UnicodeDecodeError:
                pass
            except Exception as e:
                print(e)
        else:
            replacedline = line
        sys.stdout.write(replacedline)
        yield replacedline


cwd = os.getcwd()
print('Do you want to modify all txt files in the current working directory? ' + cwd + ' (y/n)')
parseAllFlag = input()
if parseAllFlag == "y":
    filePaths = []
    for file in os.listdir('.'):
        if file.endswith(".txt"):
            filePath = os.path.join(".", file)
            filePaths.append(filePath)

    matches = {}
    print(filePaths)
    input()
    for i in range(len(filePaths)):
        print(filePaths[i])

        txtDoc = fileinput.input(filePaths[i], inplace=True)

        print("We got the following matches: ")
        for line in parser(txtDoc):
            screen.write(line + '\n')


elif parseAllFlag == "n":
    print('Do you want to use a specific file from the current working directory (default is 1_Grundlagen_layout.txt): ' + cwd + ' (y/n)')
    ownDoc = input()
    if ownDoc == "y":
        while True:
            print("Please specify just the filename (with extension): ")
            document = input()
            if os.path.join(".", document) in cwd:
                print("Document found. It will be modified now.")
            else:
                print("Document not found, try again.")
                break
    else:
        document = "1_Grundlagen_raw.txt"

    matches = {}
    txtDoc = fileinput.input(document, inplace=True)
    print("We got the following matches: ")
    for line in parser(txtDoc):
        screen.write(line + '\n')
    txtDoc.close()

else:
    print("No valid answer given, program terminates.")
    exit()
