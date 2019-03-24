import sys, os, pandas
import uproot
# import HDFStore
import matplotlib.pyplot as plt

filename = sys.argv[1]
#print("Opening %s" % filename)
file = uproot.open(filename)


#file.allkeys()
tree = file[b'a/tree;1']
#tree.keys()
print(str(tree.name) + " in " + filename + " contains " + str(len(tree)) + " entries")

