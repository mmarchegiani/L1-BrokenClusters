import sys, os, pandas
import uproot
import matplotlib.pyplot as plt
import numpy as np
import splitlib as sp

if(len(sys.argv) < 2):
	sys.exit("File name required as first argument.")

if(len(sys.argv) < 4):
	sys.exit("'nfull' and 'nbroken' required as second, third arguments.")

if(len(sys.argv) < 5):
	sys.argv.append("-nooutput")

filename = sys.argv[1]
nfull = sys.argv[2]
nbroken = sys.argv[3]

output = False
if (sys.argv[4] == "-o") | (sys.argv[4] == "-output"):
	output = True

#filename = "/scratch/mmarcheg/lumi_data/Run300806.root"
plot_dir = "../ntuplesPixel/plots/" + (filename.split("/")[-1]).split(".")[-2] + "/"
#os.mkdir(plot_dir)
if output == True:
	print("Plots will be saved in " + plot_dir)
print("Opening %s" % filename)
file = uproot.open(filename)

#file.allkeys()
tree = file[b'a/tree;1']
#tree.keys()
print(str(tree.name) + " contains %d (%.1E) entries" % (len(tree), len(tree)))

df_grid, df_grid_full, df_grid_broken = sp.select_cols(tree, nfull, nbroken)		# Function still to be tested
varlist = ["global_eta", "global_phi", "instaLumi", "bx", "tres"]
bins = [100, 100, 20, df_grid_full['bx'].max() - df_grid_full['bx'].min(), 50]

# Iteration over 5 variables and over all possible rows
#rows_max = df_grid_full['rows'].max()
rows_max = 11
rows = range(1, rows_max)
for nrows in rows:
	df_grid_full_rows = sp.select_rows(df_grid_full, nrows)
	df_grid_broken_rows = sp.select_rows(df_grid_broken, nrows)
	for i in range(len(varlist)):
		if varlist[i] == "tres":
			df_grid_full_rows = df_grid_full_rows.query('tres < 5e6')
			df_grid_broken_rows = df_grid_broken_rows.query('tres < 5e6')
		sp.splitprob(df_grid_full_rows, df_grid_broken_rows, bins=bins[i], varname=varlist[i], output=output, plot_dir=plot_dir)
