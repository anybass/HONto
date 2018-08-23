# HONto
Extracting Concept Hierarchies from Textbooks, based on the paper to be published at LeDAM Workshop 2018 (https://sites.google.com/site/legaldam2018/programme)

This work uses the following Concept Formation python library: https://github.com/cmaclell/concept_formation
We added (averaged) Precision and Recall support

For copyright reasons, we did not add the raw text file from the book we based our experiments on. However, example files for the subsequent steps are included.

Quick Start Guide

We used a pdf file of selected subchapters from the book (Handbuch zum deutschen und europäischen Bankrecht) https://www.springer.com/de/book/9783540766452. If you want to apply the process on another book, the JAPE rules for the table of contents may need to be adapted.

Given the first subchapter run on a command prompt:
pdftotext -enc utf-8 1_Grundlagen.pdf 1_Grundlagen_raw.txt

Then load the file into GATE and follow the instructions in the appendix of the extended paper version. As indicated, the order of the JAPE files matters, so the correct order is:
toc_ref.jape
rfc.jape
rfc_rel.jape

As for the configurable exporter, two .conf files are available.
Select 
toc.conf 
for the output file for the table of contents annotation, select Token as the instance name and name the file with the following suffix:
_toc.txt

and 
rel.conf
for the output file for the rfc and relationship annotation, select RFC_NE as the instance name and name the file with the following suffix:
_rel.txt

Those suffixes are important. Both files and the "\_raw.txt" file shall be in the same folder as the python script 
gate_postprocess.py

This script will output a file with the ending "\_features.json"

The file shall be modified by inserting a linebreak (\n) after each curly brace. Replace "}," with "},\n" for the subsequent steps.

Now, you have the input for the clustering script 
concept_formation.py

and for the classification script
concept_prediction.py

and you are done.

