import sys, os
#import shutil
import uproot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import splitlib as sp

if(len(sys.argv) < 2):
	sys.exit("'graphdata' path required as first argument.\t(e.g. '~/ntuplesPixel/graphdata/Run300806')")

if(len(sys.argv) < 3):
	sys.argv.append("-nooutput")

graph_dir = sys.argv[1]
plot_dir = graph_dir.replace("graphdata", "plots")

output = False
if (sys.argv[2] == "-o") | (sys.argv[2] == "-output"):
	output = True

rows_max = 5
df_list = []
axlimits = []
varlist = ["global_eta", "global_phi", "instaLumi", "bx", "tres"]
# Colors valid for rows_max=5
colors = ["red", "green", "blue", "magenta", "cyan"]
bx_low = 1980
bx_high = 2050
fileread = None

# Code valid for rows < 10
for varname in varlist:
	for nrows in range(1, rows_max+1):
		sub_dir = graph_dir + "/rows0" + str(nrows) + "/"
		ls = os.listdir()
		for file in ls:
			if varname in file:
				filename = sub_dir + filename
				df_list.append(pd.read_csv(filename))
				fileread = filename

		"""if nrows < 2:
			prob_array = df_list[nrows]['prob'].values
			sigma = df_list[nrows]['sigma'].values
			maxy = np.nanmax(prob_array)
			imax = np.nanargmax(prob_array)
			maxy = 1.05*(maxy + sigma[imax])

			#axlimits = []
			minx = df_list[nrows][varname].min()
			maxx = df_list[nrows][varname].max()
			rangex = maxx - minx
			gapx = 0.025*rangex
			gapy = 0.025*maxy
			bins_full = df_list[nrows][varname].values.tolist()
			if varname == "bx":
				ilow = list(bins_full).index(bx_low)
				ihigh = list(bins_full).index(bx_high)
				prob_array_cut = np.take(prob_array, range(ilow, ihigh+1))	# cut the array between bx_low, bx_high
				sigma_cut = np.take(sigma, range(ilow, ihigh+1))
				maxy = np.nanmax(prob_array_cut)
				imax = np.nanargmax(prob_array_cut)
				maxy = 1.05*(maxy + sigma_cut[imax])
				rangex = bx_high - bx_low
				gapx = 0.025*rangex
				gapy = 0.025*maxy
				axlimits = [bins_full[ilow] - gapx, bins_full[ihigh] + gapx, -gapy, maxy]
			else:
				axlimits = [bins_full[0] - gapx, bins_full[-1] + gapx, -gapy, maxy]
"""
		plt.errorbar(df_list[nrows][varname], df_list[nrows]['prob'], yerr=df_list[nrows]['sigma'], fmt='o', ecolor=colors[nrows], c=colors[nrows], label="rows="+str(nrows))

		s = (((filread.split("/")[-1]).split(".")[0]).split("rows0" + str(nrows))[1]).replace(varname,'')
		nfull = s[0]
		nbroken = s[1]
		splitmode = "(" + str(nfull) + "->" + str(nbroken) + ")"
		plt.title("prob splitting " + splitmode + "(rows=" + str(nrows) + ") vs " + varname)
		plt.xlabel(varname)
		plt.ylabel("prob" + splitmode)
		plt.grid(True)
		#plt.axis(axlimits)

	if output == True:
		plt.savefig(plot_dir + "prob_multirows_" + varname + str(nfull) + str(nbroken) + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

