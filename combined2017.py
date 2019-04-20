import sys, os, pandas
import uproot
# import HDFStore
import matplotlib.pyplot as plt

filename = "/scratch/mmarcheg/lumi_data/clusters_V1_Run2017C_Fill6061.root"
#plot_dir = "../ntuplesPixel/plots/" + (filename.split("/")[-1]).split(".")[-2] + "/"
#os.mkdir(plot_dir)
#print("Plots will be saved in " + plot_dir)
print("Opening %s" % filename)
file = uproot.open(filename)
tree = file[b'a/tree;1']
print(str(tree.name) + " contains " + str(len(tree)) + " entries")

entrystop = 53605236
nentries = len(tree)
read_entry = 0
i = 0
while read_entry < nentries:
	print("Reading entries between %d and %d" % (read_entry, read_entry + entrystop))
	df = tree.pandas.df([b'pos_x', b'pos_y', b'size', b'cols', b'rows', b'x', b'y', b'global_eta', b'global_phi', b'instaLumi', b'bx'], entrystart=read_entry, entrystop=read_entry + entrystop)
	print("Saving chunk number %d of dataframe" % (i+1))
	filename = "/scratch/mmarcheg/csv_files/combined2017_0" + str(i+1) + ".csv"
	df.to_csv(filename, index=False)
	read_entry += entrystop
	i += 1
print("Readed dataframe in %d chunks" % i)
