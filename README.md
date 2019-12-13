# HONto
Extracting Concept Hierarchies from Textbooks, based on the paper to be published at [LeDAM Workshop 2018](https://sites.google.com/site/legaldam2018/programme)

The folder ContextSelection contains the implementation for a follow-up paper "Context Selection in a Heterogeneous Legal Ontology", accepted by the BigDS Workshop at [BTW '19](https://btw.informatik.uni-rostock.de/index.php/de/). More information on this can be found within the folder.

In the folder reference_linking you find code for the paper "ERST: Leveraging Topic Features for Context-Aware Legal Reference Linking", presented at the JURIX 2019 conference.

Please find the code for the paper "ERST: Leveraging Topic Features for Context-Aware Legal Reference Linking" in the reference_linking folder.

*HONto* is a project which aims for: 

* Information extraction from textbooks (*hon* means "book" in Japanese, and we transform its content *to* knowledge ) 
* Modeling this knowledge in a heterogeneous (h) ontology (onto)
* Having a reliable source for domain knowledge (*honto* means "really, seriously" in Japanese)

This work uses the [Concept Formation library for python](https://github.com/cmaclell/concept_formation).

We added (averaged) Precision and Recall support.

For copyright reasons, we did not add the raw text file from the book we based our experiments on. However, example files for the subsequent steps are included.

## Prerequisites

* [pdftotext](http://www.xpdfreader.com/)
* [GATE 8.4.1](https://gate.ac.uk/) with the [plugins](https://gate.ac.uk/gate/doc/plugins.html) listed in *LeDAM_wehnert_extended.pdf* 
* Python 3 with additional libraries, such as scikit-learn, numpy, matplotlib, csv and concept_formation with our additional files (see concept_formation folder).
* Some text editor with search and replace functions (scite, notepad++,...)

## Quick Start Guide

We used a pdf file of selected subchapters from the book [Handbuch zum deutschen und europäischen Bankrecht](https://www.springer.com/de/book/9783540766452). If you want to apply the process on another book, the JAPE rules for the table of contents may need to be adapted.

1. Given the first subchapter, place it in your current working directory and rename it to *1_Grundlagen.pdf*. Then run the following command:

``pdftotext -enc utf-8 1_Grundlagen.pdf 1_Grundlagen_raw.txt``

Hint: It may be helpful for reference and reason for citing detection if you execute *removeHyphens.py* afterwards to join separated words at line breaks. However, it may impact your table of contents detection, which is why we leave this step optional for simplicity.


2. Then load the file into GATE and follow the instructions in the appendix of the extended paper version. As indicated, the order of the JAPE files matters, so the correct order is:

* toc_ref.jape
* rfc.jape
* rfc_rel.jape

3. As for the configurable exporter, two .conf files are available.
Select 
* toc.conf 

for the output file for the table of contents annotation, select *Token* as the instance name and name the file with the following suffix:
* _toc.txt

and 
* rel.conf

for the output file for the rfc and relationship annotation, select *RFC_NE* as the instance name and name the file with the following suffix:
* _rel.txt

Those suffixes are important. Both files and the *\_raw.txt* file shall be in the same folder as the python script 
* gate_postprocess.py

4. Run this script. It will output a file with the ending *\_features.json*

5. The file shall be modified by inserting a linebreak (\n) after each curly brace. Replace "}," with "},\n" for the subsequent steps.

6. Now, you have the input for the clustering script 
* concept_formation.py

and for the classification script
* concept_prediction.py

and after running either of them, you are done.

