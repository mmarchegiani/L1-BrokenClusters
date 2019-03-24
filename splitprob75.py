import sys, os, pandas
import uproot
import matplotlib.pyplot as plt
import numpy as np
import splitprob as sp

if(len(sys.argv) < 3):
	sys.argv.append("-nooutput")

output = False
if (sys.argv[2] == "-o") | (sys.argv[2] == "-output"):
	output = True

filename = sys.argv[1]
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
print(str(tree.name) + " contains " + str(len(tree)) + " entries")

entrystop_ = None
if len(tree) > 1.1e8:
	entrystop_ = 1.1e8
	print("Dataframe truncated to 1.1e8 events")
else:
	print("Dataframe keeped with all the events")
df_grid = tree.pandas.df([b'size', b'cols', b'rows', b'x', b'y', b'global_eta', b'global_phi', b'instaLumi', b'bx', b'tres'], entrystop=entrystop_)
print(df_grid.head())

print("Dataframe query...")
df_grid7 = df_grid.query('cols == 7')
df_grid75 = df_grid7.query('size == 5')

varlist = ["global_eta", "global_phi", "instaLumi", "bx", "tres"]
bins = [100, 100, 20, df_grid7['bx'].max() - df_grid7['bx'].min(), 100]
for i in range(len(varlist)):
	sp.splitprob(df_grid7, df_grid75, 7, 5, bins=bins[i], varname=varlist[i], output=output, plot_dir=plot_dir)