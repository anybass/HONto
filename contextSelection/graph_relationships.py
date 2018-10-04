# -*- coding: utf8 -*-

# Program to process the features from GATE annotation export files
# Requires files with the following endings in the current working directory:
    # _features.json


import json
import os
import csv
import re


def load_json(filename):
    """
    Loads a json file and returns a python object generated from parsing the
    json.
    """
    module_path = os.path.dirname(__file__)
    output = []
    with open(os.path.join(module_path, 'data_files', filename)) as dat:
        for idx, lin in enumerate(dat):
            output.append(json.loads(lin.strip('[],\n')))
    return output


def main():
    # Outputs which files will be processed. For debugging, the parseAllFlag shall be modified.
    cwd = os.getcwd()
    print('Do you want to convert all corresponding "_features.json" files in the current working directory ' + cwd + ' to csv? (y/n)')
    parseAllFlag = "y"
    filePaths = []
    if parseAllFlag == "y":
        for file in os.listdir('.'):
            if file.endswith("_features.json"):
                filePath = os.path.join(cwd, file)
                filePaths.append(filePath)
    print("The following file paths have been found:")
    print(filePaths)

    for f in filePaths:
        # initialize variables
        output_file = os.path.splitext(f)[0][:] + '_entities.csv'
        rel_output_file = os.path.splitext(f)[0][:] + '_relationships.csv'
    # get data from API, parse to JSON
        data = load_json(f)
        data_to_file = open(output_file, 'w', newline='', encoding='utf-8')
        data_to_relfile = open(rel_output_file, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(data_to_file, delimiter=",")
        csv_writer.writerow(["id:ID", "type", "fieldstring", "property_1", "property_2", ":LABEL"])
        csv_writer_rel = csv.writer(data_to_relfile, delimiter=",")
        csv_writer_rel.writerow([":START_ID", ":END_ID", "SOURCE", "TARGET", ":TYPE"])
        book = "Handbuch zum deutschen und europäischen Bankrecht"
        csv_writer.writerow([str(0) + str(0), "Book", book , None , None , "Node"])
        sscdict = {}
        scdict={}
        pdict = {}
        cdict = {}
        for c, i in enumerate(data):
            pre_ref = re.sub(r",", "", i['ref'])
            ref = re.sub(r'"', '', pre_ref)
            pre_rfc = re.sub(r",", "", i['rfc'])
            rfc = re.sub(r'"', '', pre_rfc)
            pre_rel = re.sub(r",", "", i['rel'])
            rel = re.sub(r'"', '', pre_rel)
            pre_part = re.sub(r",", "", i['part'])
            part = re.sub(r'"', '', pre_part)
            pre_dbp = re.sub(r",", "", i['dbp'])
            dbp = re.sub(r'"', '', pre_dbp)
            pre_reg = re.sub(r",", "", i['reg'])
            reg = re.sub(r'"', '', pre_reg)
            pre_sc = re.sub(r",", "", i['sc'])
            sc = re.sub(r'"', '', pre_sc)
            pre_ssc = re.sub(r",", "", i['ssc'])
            ssc= re.sub(r'"', '', pre_ssc)
            pre_chapter = re.sub(r",", "", i['classification'])
            chapter = re.sub(r'"', '', pre_chapter)

            csv_writer.writerow([str(1) + str(c), "Reference", ref, rel, rfc, "Node"])
            csv_writer.writerow([str(2) + str(c), "RFC", rfc, reg, dbp, "Node"])
            if  chapter not in cdict.keys():
                csv_writer.writerow([str(6) + str(c), "Chapter", chapter,None,None, "Node"])
                cdict[chapter] = str(6) + str(c)
                csv_writer_rel.writerow([str(6) + str(c), str(0) + str(0), str(6) + str(c), str(0) + str(0), 'partOf'])
            if  part not in pdict.keys() and part!="":
                csv_writer.writerow([str(5) + str(c), "Part", part,None,None, "Node"])
                pdict[part] = str(5) + str(c)
                csv_writer_rel.writerow([str(5) + str(c), cdict[chapter], str(5) + str(c), cdict[chapter], 'partOf'])
            if  sc not in scdict.keys() and sc!="":
                csv_writer.writerow([str(4) + str(c), "Subchapter", sc,None,None, "Node"])
                scdict[sc] = str(4) + str(c)
                if part!="":
                    csv_writer_rel.writerow([str(4) + str(c), pdict[part], str(4) + str(c), pdict[part], 'partOf'])
                else:
                    csv_writer_rel.writerow([str(4) + str(c), cdict[chapter], str(4) + str(c), cdict[chapter], 'partOf'])
            if not ssc in sscdict.keys() and ssc!="":
                csv_writer.writerow([str(3) + str(c), "Subsubchapter", ssc, None, None, "Node"])
                sscdict[ssc]=str(3) + str(c)
                if sc != "":
                    csv_writer_rel.writerow([str(3) + str(c), scdict[sc], str(3) + str(c), scdict[sc], 'partOf'])
                elif part != "":
                    csv_writer_rel.writerow([str(3) + str(c), pdict[part], str(3) + str(c),pdict[part], 'partOf'])
                else:
                    csv_writer_rel.writerow([str(3) + str(c), cdict[chapter], str(3) + str(c),cdict[chapter], 'partOf'])
            if ssc != "":
                csv_writer_rel.writerow([str(2) + str(c), sscdict[ssc],  str(2) + str(c), sscdict[ssc], 'partOf'])
            elif sc != "":
                csv_writer_rel.writerow([str(2) + str(c), scdict[sc], str(2) + str(c), scdict[sc], 'partOf'])
            elif part != "":
                csv_writer_rel.writerow([str(2) + str(c), pdict[part], str(2) + str(c), pdict[part], 'partOf'])

            csv_writer_rel.writerow([str(1) + str(c), str(2) + str(c), str(1) + str(c), str(2) + str(c), 'partOf'])

        data_to_file.close()
        data_to_relfile.close()

        print("Finished writing to:")
        print(output_file)
        print(rel_output_file)

if __name__ == "__main__":
    main()