# -*- coding: utf8 -*-

# Program to process the features from GATE annotation export files
# Requires the following files in the current working directory:
    # _raw.txt
    # _toc.txt
    # _rel.txt
# TODO Add support for more than one set of files in cwd
import os
import csv
import re
import json
from collections import OrderedDict

# Defining regular expressions to match extracted annotations with PDF content
number = re.compile(r"[1-9]")
whitespace = re.compile(r"\s")
capital = re.compile(r"([A-Z])")
roman = "([IXV])+"

# GATE works on a Token basis, so that we are potentially obfuscating original whitespace
# when not only single tokens are extracted.
# Therefore, we define a pattern how usually the parts of a regulation citation are formatted
# Use lookahead (?=foo) and lookbehind (?<=foo) syntax to remove only selected whitespace in between those two
refs = re.compile(r"(\s)*(?<=[\W\D\a-z])(\s)(?!der)(?=[ac-eg-tv-z\W]|[fb]{1}\s)")


# Defining a function which determines section boundaries, with start and end row number
def pairwise(lst):
    """ yield item i and item i+1 in lst. e.g.
        (lst[0], lst[1]), (lst[1], lst[2]), ..., (lst[-1], None)
    """
    if not lst:
        return
    for l in range(len(lst)-1):
        yield lst[l], lst[l+1]


# Function to perform a regex search within the document for TOC components
# This is for dividing the PDF in chunks
# to later match the REFs to each chunk they belong to
def doc_parser(raw_doc, searchstring, alt_searchstring, max_lines):
    matches = []
    tempmatches = []
    with open(raw_doc, 'r', encoding="utf8") as doc:
        for num, line in enumerate(doc, 1):
            if searchstring:
                try:
                    if re.findall(searchstring, line, re.M):
                        tempmatches.append([num, line])
                    elif re.findall(alt_searchstring, line, re.M):
                        tempmatches.append([num, line])
                except Exception as e:
                        pass
            if max_lines:
                if num == max_lines:
                    tempmatches.append([num, line])

        # Sometimes there is more than one match (when the TOC is also fits the search string)
        # We only want the passage within the text body, no TOC elements
        if len(tempmatches) == 1:
            matches.append(tempmatches[0])
        if len(tempmatches) >= 2:
            matches.append(tempmatches[1])
        del tempmatches[:]
        return matches


# This function used the chunks from the doc_parser output and looks up
# whether a reference is present within a text chunk
def get_match(r, chunks, some_string):
    some_list = []

    # enable multiline matches by removing newline characters
    for p in range(0, len(chunks)):
        o = re.sub('\n', '', str(chunks.get(p)), re.S| re.M | re.U)
        o_n = "".join(chunks.get(p))
        o_new =str(re.sub('\n\r', ' ', o_n,  re.M | re.U))
        if re.search(str(r), o, re.M | re.S | re.U):
            some_list.append([r, str(some_string.get(p))])
            continue
        else:
            if re.search(str(r), o_new, re.M | re.S | re.U):
                some_list.append([r, str(some_string.get(p))])
                continue
    if len(some_list) == 0:
        some_list.append([r, ""])
    return some_list


# opening all input text files
def toc_extractor(toc_doc, raw_doc, rel_doc):
    # opening the _rel.txt file and cleaning RFC, REL, REG and DBp features
    with open(rel_doc, 'r', encoding="utf8") as doc1:
        doc_reader1 = csv.reader(doc1, delimiter=',', quotechar='"', skipinitialspace=True)
        doc_data1 = list(doc_reader1)
        references = []
        relationships = []
        rfc = []
        dbp = []
        reg = []

        for row in doc_data1:
            if row:

                #REF
                replaced_ref = row[4].strip()
                if replaced_ref:
                    ref = re.sub(refs, "", replaced_ref)
                    if ref:
                        references.append(ref)
                    else:
                        references.append(replaced_ref)
                else:
                    replaced_ref1 = row[5].strip()
                    if replaced_ref1:
                        ref = re.sub(refs, "", replaced_ref1)
                        if ref:
                            references.append(ref)
                        else:
                            references.append(replaced_ref1)
                    else:
                        references.append(row[5])

                # REL
                relationships.append(row[3])

                # RFC
                rfcstring=row[1].strip()
                if rfcstring:
                    rfc.append(rfcstring)
                else:
                    rfcstring1 = row[2].strip()
                    rfc.append(rfcstring1)

                # REG
                regstr=row[12].strip()
                if regstr:
                    reg.append(regstr)

                # DBp
                if row[9]:
                        replaced_url = (str(row[9]).split('/')[-1:])[0]
                        if replaced_url:
                            url= re.sub(r'Schweizerische_Volkspartei', "Bürgerliches_Gesetzbuch", replaced_url)
                            if url:
                                dbp.append(url)
                            else:
                                dbp.append(replaced_url)

                elif row[7]:
                    replaced_url=(str(row[7]).split('/')[-1:])[0]
                    if replaced_url:
                        # Replacing a DBpedia mismatch regarding German civil code
                        url = re.sub(r'Schweizerische_Volkspartei', "Bürgerliches_Gesetzbuch", replaced_url)
                        if url:
                            dbp.append(url)
                        else:
                            dbp.append(replaced_url)
                else:
                    dbp.append(row[7])

    # Getting TOC components from the annotation file
    with open(toc_doc, "r", encoding="utf8") as doc2:
        doc_reader2 = csv.reader(doc2, delimiter=',', quotechar='"', skipinitialspace=True)
        doc_data2 = list(doc_reader2)
       # print(doc_data1)
        chapter_dict = {}
        part_dict = OrderedDict()
        part_order = []
        subchapter_dict = {}
        subchapter_order = []
        subsubchapter_dict = {}
        subsubchapter_order = []
        part_num=[]
        chapter_name=""
        for row in doc_data2:
            if row:
                # Chapter (= classification attribute)
                if number.search(row[1]):
                    chapter_dict[row[1]] = row[2]
                    chapter_name=row[2]
                    chapter_name = re.sub(whitespace,  "-", chapter_name.strip())
                # Part
                if capital.search(row[4]):
                    part_dict[row[4]] = row[5]
                # Subchapter
                if number.search(row[9]):
                    if row[8] not in subchapter_dict:
                        subchapter_order.append(row[8])
                        subchapter_dict[row[8]] = row[9]
                # Subsubchapter
                if number.search(row[13]):
                    if row[12] not in subsubchapter_dict:
                        subsubchapter_dict[row[12]] = row[13]
                        subsubchapter_order.append(row[12])
        # preserving part order
        for x in range(len(part_dict)):
            part_order.append(list(part_dict.values())[x])
            part_num.append(list(part_dict.keys())[x])
        part_matches = []
        subchapter_matches = []
        subsubchapter_matches = []

        # finding last line in a document for chunking
        def last_line(doc):
            num_lines = 0
            with open(doc, "r", encoding="utf8") as document:
                num_lines += sum(1 for l in document)
                return num_lines

        numlines = last_line(raw_doc)
        #Lookup of TOC components in raw_doc (pdftotext of original PDF)
        # Part Lookup
        for p in part_order:
            searchstring = "^([0-9]*[\s]*[A-H][.]\s)" + p.strip()
            alt_searchstring = "^([0-9]*[\s]*[A-H][.]\s)" + p[0:-8].strip()
            part_matches.append(doc_parser(raw_doc, searchstring, alt_searchstring, None))
        part_matches.append(doc_parser(raw_doc, None, None, numlines))
        # Subchapter Lookup
        subsubchapter_prefix = []
        for s in subchapter_order:
            searchstring = "^([0-9]*[\s]*(%s)[.]\s)" % roman + (s.replace('\(\)', '')).strip()
            alt_searchstring = "^([0-9]*[\s]*(%s)[.]\s)" % roman + (s[0:-8].replace('\(\)', '')).strip()
            subsubchapter_prefix.append(searchstring)
            subchapter_matches.append(doc_parser(raw_doc, searchstring, alt_searchstring, None))
            if len(subchapter_matches) > 0:
                continue
        subchapter_matches.append(doc_parser(raw_doc, None, None, numlines))
        # Subsubchapter Lookup
        for ss in subsubchapter_order:
            searchstring = "(^([0-9]*[\s]*(%s)[.]\s([A-Za-z0-9\s])+[.]\s)?[0-9]*[\s]*[0-9][.]\s)" % roman + ss.strip() + "([.]\s([A-Za-z0-9])+)"
            alt_searchstring = "(^([0-9]*[\s]*(%s)[.]\s([A-Za-z0-9\s])+[.]\s)?[0-9]*[\s]*[0-9][.]\s)" % roman +  ss[0:-8].strip()
            subsubchapter_matches.append(doc_parser(raw_doc, searchstring, alt_searchstring, None))
            if len(subchapter_matches) > 0:
                continue
        subsubchapter_matches.append(doc_parser(raw_doc, None, None, numlines))

        # get boundaries of part
        part_boundaries=[]
        for p in part_matches:
            for num, line in p:
                part_boundaries.append(num)
        # get boundaries of subchapter
        subchapter_boundaries = []
        for p in subchapter_matches:
            for num, line in p:
                subchapter_boundaries.append(num)
        # get boundaries of subsubchapter
        subsubchapter_boundaries = []
        for p in subsubchapter_matches:
            for num, line in p:
                subsubchapter_boundaries.append(num)

    # part extraction
    reference_part=[]
    reference_pn = []
    i=0
    chunks={}
    part_name={}
    pn={}
    for n, m in pairwise(part_boundaries):
        chunk=[]
        with open(raw_doc, 'r', encoding="utf8") as reference_doc:
            for l, chunkline in enumerate(reference_doc):
                if n <= l < m:
                    chunk.append(chunkline)
                else:
                    continue
        part_name[i] = (part_order[i]).strip()
        pn[i] = (part_num[i]).strip()
        chunks[i] = chunk
        i += 1

    for r in references:
        reference_part.append(get_match(r, chunks, part_name))
    for r in references:
        reference_pn.append(get_match(r, chunks, pn))

    # subchapter extraction
    reference_subchapter = []
    i = 0
    chunks = {}
    subchapter_name = {}
    for n, m in pairwise(subchapter_boundaries):
        chunk = []
        with open(raw_doc, 'r', encoding="utf8") as reference_doc:
            for l, chunkline in enumerate(reference_doc):
                if n <= l < m:
                    chunk.append(chunkline)
                else:
                    continue
        subchapter_name[i] = (subchapter_order[i]).strip()
        chunks[i] = chunk
        i += 1
    for r in references:
        reference_subchapter.append(get_match(r, chunks, subchapter_name))
    print(reference_subchapter)

    # subsubchapter extraction
    reference_subsubchapter=[]
    i = 0
    chunks = {}
    subsubchapter_name = {}
    for n, m in pairwise(subsubchapter_boundaries):
        chunk = []
        with open(raw_doc, 'r', encoding="utf8") as reference_doc:
            for l, chunkline in enumerate(reference_doc):
                if n <= l < m:
                    chunk.append(chunkline)
                else:
                    continue
        subsubchapter_name[i] = (subsubchapter_order[i]).strip()
        chunks[i] = chunk
        i += 1
    for r in references:
            reference_subsubchapter.append(get_match(r, chunks, subsubchapter_name))

    #now use all extracted information to create cluster instances, where references are the instances
    # and part, subchapter, subsubchapter, and dbpedia concepts are features
    reference_features=[]
    parts = []
    pn = []
    for inner_l in reference_part:
        for item in inner_l:
            parts.append(item[1])

    for inner_l in reference_pn:
        for item in inner_l:
            pn.append(item[1])

    subchapters = []
    sc = []
    for inner_l in reference_subchapter:
        for item in inner_l:
            subchapters.append(item[1])
            sc.append(item[0])
    subsubchapters = []
    ssc = []
    for inner_l in reference_subsubchapter:
        for item in inner_l:
            subsubchapters.append(item[1])
            ssc.append(item[0])
    '''
    print(len(references))
    print(len(relationships))
    print(len(rfc))
    print(len(dbp))
    print(len(reference_part))
    print(len(reference_subchapter))
    print(len(reference_subsubchapter))
    print(references)
    print(relationships)
    print(rfc)
    print(dbp)
    '''

    # Construct format of instances with features
    for r in range(len(references)):
        features = {}
        features["ref"] = str(references[r])
        #features["chapter"] = chapter_name
        features["rfc"] = str(rfc[r])
        features["rel"] = str(relationships[r])
        features["part"] = str(parts[r])
        features["dbp"] = str(dbp[r])
        features["reg"] = str(reg[r])
        features["sc"] = str(subchapters[r])
        features["ssc"] = str(subsubchapters[r])
        features["classification"] = chapter_name
        #features["classification"] = str(rfc[r])
        #features["classification"] = str(references[r])

        reference_features.append(features)
    print(reference_features)
    return reference_features

# Outputs which files will be processed. For debugging, the parseAllFlag shall be modified.
cwd = os.getcwd()
print('Do you want to process the features of all corresponding "_toc.txt" files in the current working directory? ' + cwd + ' (y/n)')
parseAllFlag = "y"
filePaths = []
rawFilePaths = []
relFilePaths = []
if parseAllFlag == "y":
    for file in os.listdir('.'):
        if file.endswith("_toc.txt"):
            filePath = os.path.join(cwd , file)
            filePaths.append(filePath)
        if file.endswith("_raw.txt"):
            filePath = os.path.join(cwd , file)
            rawFilePaths.append(filePath)
        if file.endswith("_rel.txt"):
            filePath = os.path.join(cwd, file)
            relFilePaths.append(filePath)

    print("The following file paths have been found:")
    print(filePaths)
    print(rawFilePaths)
    print(relFilePaths)

else:
    continueFlag = True
    while continueFlag == True:
        print("Do you want to specify (a) filepath(s) from the current working directory  " + cwd + ' (y/n)')
        parseCwdFlag = input()
        if parseCwdFlag == "y":
            print("Please write the file name (with extension): ")
            filePaths.append(cwd + "/" + input())
        else:
            print("Please write the full file path (with extension): ")
            filePaths.append(input())
        print("You want to extract the following file(s): " + str(filePaths))
        print("Is there more to add? (y/n)")
        finishFlag = input()
        if finishFlag == "n":
            continueFlag = False
    delFlag = False
    for i in filePaths:
        if not os.path.exists(i):
            print("Searching for " + i + ". No match in directory.. Try again")
            delFlag = True
        if not i.endswith("_raw.txt"):
            print("The file " + i + ". is not compatible with the required file format suffix '_toc.txt'")
            delFlag = True

        if delFlag == True:
            print("From the following list, the wrong path will be deleted: ")
            print(filePaths)
            del(filePaths[-1])
            delFlag = False
            print("This is the correct list now: ")
            print(filePaths)

if not filePaths:
    print("No valid path given. Program will terminate.")
    exit()
else:
    for j in range(len(filePaths)):
        for i in filePaths:
            final_toc = toc_extractor(i, rawFilePaths[j], relFilePaths[j])

            print("File " + i)
            print(final_toc)
            if final_toc:
                outfile = os.path.splitext(i)[0][:-4] + '_features.json'
                print("File will be written to " + outfile + ". Ok? (y/n)")
                writeFlag = "y"
                if writeFlag == "y":
                    with open(outfile, "w", encoding="utf8") as file:
                        json.dump(final_toc, file)
                        file.close()
                else:
                    print("Program will not write this file.")
                    continue
            else:
                print("No ToC could be detected. Program will skip this file.")