import sys, os
#import shutil
import uproot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import splitlib as sp

if(len(sys.argv) < 2):
	sys.exit("'graphdata' path required as first argument.\t(e.g. '~/ntuplesPixel/graphdata/Run03/Run300806')")

#if(len(sys.argv) < 3):
#	sys.exit("'rows' required as second arguments.")

if(len(sys.argv) < 3):
	sys.argv.append("-nooutput")

graph_dir = sys.argv[1]
#nrows = sys.argv[2]
#nfull = sys.argv[2]
#nbroken = sys.argv[3]
plot_dir = graph_dir.replace("graphdata", "plots")
if plot_dir[-1] != "/":
	plot_dir = plot_dir + "/"

output = False
if (sys.argv[2] == "-o") | (sys.argv[2] == "-output"):
	output = True

axlimits = []
varlist = ["global_eta", "global_phi", "instaLumi", "bx", "tres"]
# Colors valid for 75, 64, 53, 42 cases
colors = ["red", "green", "blue", "magenta"]
#index = ['global_eta','n_broken','n_full','prob','sigma','sigma_uncorr']
bx_low = 1980
bx_high = 2050
fileread = None
rows_max = 5

# Code valid for rows < 10
for varname in varlist:
	for nrows in range(1, rows_max):
		sub_dir = graph_dir + "/rows0" + str(nrows) + "/"
		ls = os.listdir(sub_dir)
		caselist = [7, 6, 5, 4]
		for nfull in caselist:
			nbroken = nfull - 2
			df_buffer = pd.DataFrame()
			for file in ls:
				string = varname + str(nfull) + str(nbroken)
				if string in file:
					filename = sub_dir + file
					#print(filename)
					#df_buffer = df_buffer.append(pd.read_csv(filename))
					df_buffer = pd.read_csv(filename)
					fileread = filename
					#print(df_buffer.head())

			#print(df_buffer)
			plt.errorbar(df_buffer[varname], df_buffer['prob'], yerr=df_buffer['sigma'], fmt='.', ecolor=colors[max(caselist)-nfull], c=colors[max(caselist)-nfull], label=str(nfull) + "->" + str(nbroken))

			#s = (((filread.split("/")[-1]).split(".")[0]).split("rows0" + str(nrows))[1]).replace(varname,'')
			#nfull = s[0]
			#nbroken = s[1]
			splitmode = "(" + str(nfull) + "->" + str(nbroken) + ")"
			plt.title("prob splitting " + splitmode + " " + varname)
			plt.xlabel(varname)
			plt.ylabel("prob" + splitmode)
			plt.grid(True)
			plt.legend(loc="upper left")
			if varname == "bx":
				plt.axis([1000, 1100, 0, 1.0])
			#plt.axis(axlimits)

		if output == True:
			sub_dir = sub_dir.replace("graphdata", "plots")
			dest_file = sub_dir + "prob_multicases_" + "rows0" + str(nrows) + "_" + varname + ".png"
			print("Saving " + dest_file)
			plt.savefig(dest_file, format="png", dpi=300)
			plt.close()
		else:
			plt.show()