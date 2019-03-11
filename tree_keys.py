import os, sys, pandas
import uproot
# import HDFStore
import matplotlib.pyplot as plt

filename = "/scratch/mmarcheg/lumi_data/Run300806.root"
#filename = sys.argv[1]
#plot_dir = "../ntuplesPixel/plots/" + filename.split(".")[-2] + "/"
#os.mkdir(plot_dir)
print("Opening %s" % filename)
file = uproot.open(filename)
tree = file[b'a/tree;1']
f = open(filename.split(".")[-2] + "_keys.txt", 'w')
f.write(str(tree.name) + " contains " + str(len(tree)) + " entries" + '\n' + '\n')
f.write("tree.keys()" + '\n')
for item in tree.keys():
	f.write(str(item) + "\n")
	print(str(item))
f.close()
