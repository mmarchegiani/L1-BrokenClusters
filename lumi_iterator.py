import sys, os
#import shutil
import uproot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import splitlib as sp

if(len(sys.argv) < 2):
	sys.exit("'graphdata' path required as first argument.\t(e.g. '~/ntuplesPixel/graphdata/combined2017/')")

if(len(sys.argv) < 3):
	sys.argv.append("-nooutput")

graph_dir = sys.argv[1]
plot_dir = graph_dir.replace("graphdata", "plots")
if plot_dir[-1] != "/":
	plot_dir = plot_dir + "/"

output = False
if (sys.argv[2] == "-o") | (sys.argv[2] == "-output"):
	output = True

varname = "global_eta"
# Colors valid for rows_max=5
colors = ["darkorange", "limegreen", "cornflowerblue", "purple", "darkgrey", "red", "green", "blue", "magenta", "cyan"]
#index = ['global_eta','n_broken','n_full','prob','sigma','sigma_uncorr']
axlimits = [-3.2, 3.2, 0., 1.05]
fileread = None
ls = os.listdir(graph_dir)
ls.sort()
while int(ls[-1].replace("lumi", "")) < 10000:
	ls = [ls[-1]] + ls[:-1]

for nfull in [10, 9, 8, 7, 6, 5, 4]:
	nbroken = nfull - 2
	for ladder in ["inner", "outer"]:
		df_buffer = pd.DataFrame()
		string = ladder + "_" + varname + str(nfull) + str(nbroken)
		for (i, dir) in enumerate(ls):
			sub_dir = graph_dir + "/" + dir + "/"
			ls_files = os.listdir(sub_dir)
			for file in ls_files:
				if string in file:
					filename = sub_dir + file
					df_buffer = pd.read_csv(filename)
					fileread = filename
					plt.errorbar(df_buffer[varname], df_buffer['prob'], yerr=df_buffer['sigma'], fmt='.', ecolor=colors[i], c=colors[i], label=dir)
		
		splitmode = "(" + str(nfull) + "->" + str(nbroken) + ")"
		plt.title("prob splitting " + splitmode + " " + varname)
		plt.xlabel(varname)
		plt.ylabel("prob" + splitmode)
		plt.grid(True)
		plt.legend(loc="upper left")
		#plt.axvline(-1, 0., 1.05, linestyle='--', label ="central bin")
		plt.axvline(-1, 0., 1.05, linestyle='--')
		plt.axvline(+1, 0., 1.05, linestyle='--')
		plt.axis(axlimits)
		plt.legend(loc="upper center")
		plt.text(-3.0, 0.85, ladder + " modules", bbox=dict(facecolor='yellow', alpha=0.75))
		plt.text(-3.0, 0.95, "2017 combined data", bbox=dict(facecolor='yellow', alpha=0.75))

		if output == True:
			dest_file = plot_dir + "prob_multilumi_" + ladder + "_" + varname + str(nfull) + str(nbroken) + ".png"
			print("Saving " + dest_file)
			plt.savefig(dest_file, format="png", dpi=300)
			plt.close()
		else:
			plt.show()

