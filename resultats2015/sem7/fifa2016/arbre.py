# -*- coding: utf-8 -*-<

import numpy as np
from sklearn.tree import DecisionTreeClassifier
import os
from sklearn import tree

#creation de matrice 100x10
X = np.random.rand(100, 10)

print X.shape
print X
y = np.random.randint(5, size=(100,1))

print y.shape
print y
#Creation de l’arbre
arbre = DecisionTreeClassifier()
#Apprentissage de l’arbre sur une matrice x (chaque ligne un exemple) 
arbre.fit(X,y)
#prediction d’un exemple
print arbre

# nouvel exemple à classifier
exemple = np.random.rand(1,10)
print "exemple a classifier",exemple
predicted_class=arbre.predict(exemple)
print "=>",predicted_class

print arbre
#afficher un arbre
with open("tree.dot","w") as f:
    f = tree.export_graphviz(arbre,out_file=f)
os.system("dot -Tpdf tree.dot -o tree.pdf")