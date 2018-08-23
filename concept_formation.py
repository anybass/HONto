# -*- coding: utf-8 -*-

# Program to cluster the instances based on their features from json file ending with _features.json
# The code is based on the examples provided by the concept_formation python package
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
import os
from random import shuffle
from random import seed

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import adjusted_rand_score
from concept_formation.owncobweb import CobwebTree
from concept_formation.cluster import cluster
from concept_formation.datasets import _load_json
from _collections import defaultdict


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
            filePath = os.path.join(cwd, file)
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
        # print(i)
        print("Continue clustering now...")
        seed(0)
        instances = _load_json(i)
        shuffle(instances)

        # invoking CobwebTree
        tree = CobwebTree()

        # The _features.json file contains one attribute called "classification"
        # This is the ground truth
        # In our case, we chosoe each CHAPTER name as the classification value
        # Thereby, similar instances (from the same chapter) shall be grouped together
        instances_no_class = [{a: instance[a] for a in instance
                               if a != 'classification'} for instance in instances]
        clusters = cluster(tree, instances_no_class)[0]
        instance_class = [instance[a] for instance in instances for a in instance
                          if a == 'classification']
        ari = adjusted_rand_score(clusters, instance_class)

        dv = DictVectorizer(sparse=False)
        instance_X = dv.fit_transform(instances_no_class)

        # Prinicpal Component Analysis to reduce dimensionality
        pca = PCA(n_components=2)
        instance_2d_x = pca.fit_transform(instance_X)

        # Plotting the result
        colors=['dodgerblue','darkred','teal', "silver", "pink", "y"]
        clust_set = {v: i for i, v in enumerate(list(set(clusters)))}
        class_set = {v: i for i, v in enumerate(list(set(instance_class)))}
        legend_color=[]
        for class_idx, class_label in enumerate(class_set):
            print("class_label")
            print(class_label)
            x = [v[0] for i, v in enumerate(instance_2d_x) if instance_class[i] == class_label]
            y = [v[1] for i, v in enumerate(instance_2d_x) if instance_class[i] == class_label]
            c = [colors[clust_set[clusters[i]]] for i, v in enumerate(instance_2d_x) if
                 instance_class[i] == class_label]

            # Selecting cluster colors
            colordict=defaultdict(int)
            for j in c:
                colordict[j]+=1
            color=max(colordict, key=colordict.get)
            legend_color.append(color)
            # print(color)
            # print(colordict.items())
            plt.scatter(x, y, color=c, marker=r"$ {} $".format(class_label[0]), label=class_label)

        plt.title("COBWEB Clustering (ARI w/ Hidden Part Labels = %0.2f)" % (ari))
        plt.xlabel("PCA Dimension 1")
        plt.ylabel("PCA Dimension 2")
        leg = plt.legend(loc=2)
        leg.legendHandles[0].set_color(legend_color[0])
        leg.legendHandles[1].set_color(legend_color[2])
        leg.legendHandles[2].set_color(legend_color[1])
        plt.show()