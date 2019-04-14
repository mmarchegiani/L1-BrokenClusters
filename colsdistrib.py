import sys, os
import uproot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import splitlib as sp

# To launch script with all the arguments:
# python3.6 splitprob.py /scratch/mmarcheg/lumi_data/Run300806.root 7 5 -o -s Run99

if (len(sys.argv) < 2):
	sys.exit("File name required as first argument.")

if (len(sys.argv) < 4):
	sys.exit("'nfull' and 'nbroken' required as second, third arguments.")

if (len(sys.argv) < 5):
	sys.argv.append("-nooutput")

if (len(sys.argv) < 6):
	sys.argv.append("-noselection")

if (len(sys.argv) < 7):
	sys.argv.append("test")

if (len(sys.argv) < 8):
	sys.argv.append(None)

if (len(sys.argv) < 9):
	sys.argv.append(None)

filename = sys.argv[1]
nfull = sys.argv[2]
nbroken = sys.argv[3]

output = False
if (sys.argv[4] == "-o") | (sys.argv[4] == "-output"):
	output = True

selection = False
if (sys.argv[5] == "-s") | (sys.argv[5] == "-selection"):
	selection = True

run = sys.argv[6]
if run[-1] != "/":
	run = run + "/"


#filename = "/scratch/mmarcheg/lumi_data/Run300806.root"
plot_dir = "../ntuplesPixel/plots/" + run + (filename.split("/")[-1]).split(".")[-2] + "/"

if not os.path.exists(plot_dir):
	os.makedirs(plot_dir)
#else:
#	print(plot_dir + " already exists in memory. Overwrite it? (y/n)")
#	line = sys.stdin.readline()
#	if not ((line == "y\n") | (line == "y") | (line == "yes\n") | (line == "yes")):
#		sys.exit("Aborting the process. Exit.")

if output == True:
	print("Plots will be saved in " + plot_dir)
print("Opening %s" % filename)
file = uproot.open(filename)

#file.allkeys()
tree = file[b'a/tree;1']
#tree.keys()
print(str(tree.name) + " contains %d (%.1E) entries" % (len(tree), len(tree)))

entrystop_ = None
if len(tree) > 53605236:		# HARDCODED
	entrystop_ = 53605236
	print("Dataframe truncated to %.1E events" % entrystop_)
else:
	print("Dataframe keeped with all %d events" % len(tree))
df_grid = tree.pandas.df([b'ladder', b'rows', b'cols', b'global_eta', b'instaLumi'], entrystop=entrystop_)

nbins_lumi = 5
lumi_n, lumi_bins, patches = plt.hist(df_grid['instaLumi'], bins=nbins_lumi)
plt.close()


for ladder in ["inner", "outer"]:
	# Ladder selection after choosing the binning: in this way either in case "inner" or "outer", we'll have same binning
	df_ladder = sp.select_ladder(df_grid, ladder)
	for j in range(len(lumi_bins) - 1):
		sp.cols_distrib(df_ladder, 2.5, lumi_bins, ladder, output=output, plot_dir=plot_dir)
