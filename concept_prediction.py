# -*- coding: utf-8 -*-

#Program to predict Chapter based on features
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
import os
import sys
import json
from random import shuffle
import numpy as np
from random import seed

import matplotlib.pyplot as plt
from concept_formation.examples.examples_utils import avg_lines
from concept_formation.own_evaluation import incremental_evaluation
# trying to find precision and recall here
from concept_formation.own_evaluation import probability
#
from concept_formation.owncobweb3 import Cobweb3Tree
from concept_formation.owndummy import DummyTree
from concept_formation.datasets import _load_json

# A file ending with _features.json is required to be present in the current working directory
# The _features.json file is obtained after exporting from GATE
# and running gate_postprocess.py on the _toc.txt and _rel.txt files
cwd = os.getcwd()
print('Do you want to process the features of all corresponding "_toc.txt" files in the current working directory? ' + cwd + ' (y/n)')
parseAllFlag = "y"
filePaths = []
layoutFilePaths = []
relFilePaths = []
if parseAllFlag == "y":
    for file in os.listdir('.'):
        if file.endswith("_features.json"):
            filePath = os.path.join(cwd , file)
            filePaths.append(filePath)

    print("The following file paths have been found:")
    print(filePaths)

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
        if not i.endswith("_features.json"):
            print("The file " + i + ". is not compatible with the required file format suffix '_ToC.txt'")
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
    for i in filePaths:
        print(i)
        print("Continue predicting...")
        seed(0)

        # set number of runs and examples
        num_runs = 10
        num_examples = 300
        # set target attribute (to be predicted)
        attr = "classification"

        instances = _load_json(i)
        classlist = set([])
        for i, instance in enumerate(instances):
            if instance[attr] not in classlist:
                classlist.add(instance[attr])

        cobweb_dataset = incremental_evaluation(Cobweb3Tree(), instances, classlist, attr,
                                             run_length=num_examples,
                                             runs=num_runs)

        # We obtain precision and recall values from our modified Cobweb3Tree script
        precision_data = []
        recall_data = []
        for l in range(len(classlist)):
            cobweb_data = cobweb_dataset[l]
            precision_data.append(cobweb_data[0])
            print("precision_data")
            print(precision_data)
            recall_data.append(cobweb_data[1])
            print("recall_data")
            print(recall_data)
        precision_x, precision_y = [], []
        recall_x, recall_y = [], []
        for opp in range(len(precision_data[0])):
                for run in range(len(precision_data)):
                    precision_x.append(opp)
                    precision_y.append(precision_data[run][opp])
        for opp in range(len(recall_data[0])):
                for run in range(len(recall_data)):
                    recall_x.append(opp)
                    recall_y.append(recall_data[run][opp])
        precision_x = np.array(precision_x)
        precision_y = np.array(precision_y)
        recall_x = np.array(recall_x)
        recall_y = np.array(recall_y)
        precision_y_smooth, precision_lower_smooth, precision_upper_smooth = avg_lines(precision_x, precision_y)
        recall_y_smooth, recall_lower_smooth, recall_upper_smooth = avg_lines(recall_x, recall_y)
        plt.fill_between(precision_x, precision_lower_smooth, precision_upper_smooth, alpha=0.5, facecolor="skyblue")
        plt.fill_between(recall_x, recall_lower_smooth, recall_upper_smooth, alpha=0.5, facecolor="salmon")
        plt.plot(precision_x, precision_y_smooth, label="Precision", color="dodgerblue")
        plt.plot(recall_x, recall_y_smooth, label="Recall", color="darkred")
        plt.gca().set_ylim([0.00, 1.0])
        plt.gca().set_xlim([0, max(recall_x) - 1])
        plt.title("Incremental Reference Class Prediction (Chapter)")
        plt.xlabel("# of Training Examples")
        plt.ylabel("Average Score")
        plt.legend(loc=4)
        plt.show()