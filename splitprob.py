import sys, os
import uproot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import splitlib as sp

# To launch script with all the arguments:
# python3.6 splitprob.py /scratch/mmarcheg/lumi_data/Run300806.root 7 5 -o -s Run99 inner -l

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

ladder = sys.argv[7]
if not ((ladder == "inner") | (ladder == "outer") | (ladder == None) ):
	sys.exit("Ladder name not recognised. Options: ('inner'/'outer')")

lumibinned = False
if (sys.argv[8] == "-l") | (sys.argv[8] == "-lumi"):
	lumibinned = True

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

df_grid, df_grid_full, df_grid_broken = sp.select_cols(tree, nfull, nbroken, selection)

nbins_lumi = 0
lumi_bins = []
if lumibinned == True:
	nbins_lumi = 5
	lumi_n, lumi_bins, patches = plt.hist(df_grid_full['instaLumi'], bins=nbins_lumi)
	plt.close()

luminame = []
for i in range(nbins_lumi):
	luminame.append(str(int(0.5*(lumi_bins[i+1] + lumi_bins[i]))))

# Ladder selection after choosing the binning: in this way either in case "inner" or "outer", we'll have same binning
df_grid_full = sp.select_ladder(df_grid_full, ladder)
print("FULL")
df_grid_broken = sp.select_ladder(df_grid_broken, ladder)
print("BROKEN")
varlist = ["global_eta", "global_phi", "instaLumi", "bx", "tres"]
axlist = []
if lumibinned == True:
	nbins_eta = 16
	#bins = [100, 100, 4, df_grid_full['bx'].max() - df_grid_full['bx'].min(), 50]
	bins = [np.linspace(-3.2, -1, nbins_eta + 1).tolist() + np.linspace(+1, +3.2, nbins_eta + 1).tolist(), 100, 4, df_grid_full['bx'].max() - df_grid_full['bx'].min(), 50]
	for j in range(len(lumi_bins) - 1):
		df_grid_full_lumi = pd.DataFrame()
		df_grid_broken_lumi = pd.DataFrame()
		df_grid_full_lumi = sp.select_lumi(df_grid_full, [lumi_bins[j], lumi_bins[j+1]])
		print("FULL")
		df_grid_broken_lumi = sp.select_lumi(df_grid_broken, [lumi_bins[j], lumi_bins[j+1]])
		print("BROKEN")
		index_list = df_grid_broken_lumi.index.values		# List of indices of selected data
		if not index_list.size > 0:
			print("Dataframe is empty")
			print("No operations will be performed. Continue.")
			continue
		for i in range(len(varlist)):
			sp.splitprob_lumi(df_grid_full_lumi, df_grid_broken_lumi, bins=bins[i], axlimits=[], varname=varlist[i], luminame=luminame[j], output=output, plot_dir=plot_dir)
else:
# Iteration over 5 variables and over all possible rows
#rows_max = df_grid_full['rows'].max()
	bins = [100, 100, 20, df_grid_full['bx'].max() - df_grid_full['bx'].min(), 50]
	rows_max = 8
	rows = range(1, rows_max+1)
	for nrows in rows:
		df_grid_full_rows = pd.DataFrame()
		df_grid_broken_rows = pd.DataFrame()
		df_grid_full_rows = sp.select_rows(df_grid_full, nrows)
		print("FULL")
		df_grid_broken_rows = sp.select_rows(df_grid_broken, nrows)
		print("BROKEN")
		index_list = df_grid_broken_rows.index.values		# List of indices of selected data
		if not index_list.size > 0:
			print("Dataframe is empty")
			break
		for i in range(len(varlist)):
			#if varlist[i] == "tres":
			#	df_grid_full_rows = df_grid_full_rows.query('tres < 5e6')
			#	df_grid_broken_rows = df_grid_broken_rows.query('tres < 5e6')
			if nrows == 1:
				plotlimits = sp.splitprob(df_grid_full_rows, df_grid_broken_rows, bins=bins[i], axlimits=[], varname=varlist[i], output=output, plot_dir=plot_dir)
				axlist.append(plotlimits)	
			else:
				sp.splitprob(df_grid_full_rows, df_grid_broken_rows, bins=bins[i], axlimits=axlist[i], varname=varlist[i], output=output, plot_dir=plot_dir)