import sys, os
#import shutil
import uproot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import splitlib as sp

if(len(sys.argv) < 2):
	sys.exit("'graphdata' path required as first argument.\t(e.g. '~/ntuplesPixel/graphdata/combined2017/')")

if(len(sys.argv) < 3):
	sys.argv.append("-nooutput")

mode = ""
graph_dir = sys.argv[1]
plot_dir = graph_dir.replace("graphdata", "plots")
if plot_dir[-1] != "/":
	plot_dir = plot_dir + "/"

for mod in ["8b4e", "combined2017"]:
	if mod in graph_dir:
		mode = mod

output = False
if (sys.argv[2] == "-o") | (sys.argv[2] == "-output"):
	output = True

varlist = ["global_eta", "ti"]
colors = ["darkorange", "limegreen", "cornflowerblue", "purple", "darkgrey", "red", "green", "blue", "magenta", "cyan"]
nbins_eta = 16
bins = [np.linspace(-3.2, -1, nbins_eta + 1).tolist() + np.linspace(+1, +3.2, nbins_eta + 1).tolist(), np.linspace(-0.5, 8.5, 10).tolist()]
fileread = None
ls = os.listdir(graph_dir)
ls.sort()
poplist = []

while int(ls[-1].replace("lumi", "")) < 10000:
	ls = [ls[-1]] + ls[:-1]


file_exists = False
for varname in varlist:
	index = varlist.index(varname)
	n_broken = []
	n_full = []
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
						file_exists = True
						filename = sub_dir + file
						df_buffer = pd.read_csv(filename)
						fileread = filename
						n_broken = sp.list_sum(n_broken, df_buffer['n_broken'].tolist())
						n_full = sp.list_sum(n_full, df_buffer['n_full'].tolist())
						plt.errorbar(df_buffer[varname], df_buffer['prob'], yerr=df_buffer['sigma'], fmt='.', ecolor=colors[i], c=colors[i], label=dir[:4] + " = " + dir[4:])
			
			if not file_exists:
				continue
			splitmode = "(" + str(nfull) + "->" + str(nbroken) + ")"
			plt.title("prob splitting " + splitmode + " " + varname)
			plt.xlabel(varname)
			if varname == "global_eta":
				plt.xlabel("$\\eta$")
				plt.axvline(-1, 0., 1.05, linestyle='--')
				plt.axvline(+1, 0., 1.05, linestyle='--')
				#plt.axvline(-1, 0., 1.05, linestyle='--', label ="central bin")
				plt.legend(loc="upper center")
				plt.text(-3.0, 0.85, ladder + " modules", bbox=dict(facecolor='yellow', alpha=0.75))
				plt.text(-3.0, 0.95, mode + " data", bbox=dict(facecolor='yellow', alpha=0.75))
				axlimits = [-3.2, 3.2, 0., 1.05]
			if varname == "ti":
				plt.xlabel("Bunch Train Index")
				plt.legend(loc="upper left")
				plt.text(0., 0.85, ladder + " modules", bbox=dict(facecolor='yellow', alpha=0.75))
				plt.text(0., 0.95, mode + " data", bbox=dict(facecolor='yellow', alpha=0.75))
				axlimits = [-0.5, 8.5, 0., 0.2]

			plt.ylabel("prob" + splitmode)
			plt.grid(True)
			plt.axis(axlimits)

			if output == True:
				dest_file = plot_dir + "prob_multilumi_" + ladder + "_" + varname + str(nfull) + str(nbroken) + ".png"
				print("Saving " + dest_file)
				plt.savefig(dest_file, format="png", dpi=300)
				plt.close()
			else:
				plt.show()

			if varname == "ti":
				sp.splitprob_n(n_full, n_broken, nfull, nbroken, ladder, bins[index], varname=varname, luminame="inclusive", output=True, plot_dir=plot_dir, mode=mode)

