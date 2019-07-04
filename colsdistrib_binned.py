import sys, os
import uproot
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np
import splitlib as sp

# To launch script with all the arguments:
# python colsdistrib_binned.py

filename = "/scratch/mmarcheg/lumi_data/clusters_V1_Run2017C_Fill6061.root"
plot_dir = "../ntuplesPixel/plots/colsdistrib/"
if not os.path.exists(plot_dir):
	os.makedirs(plot_dir)
print("Plots will be saved in " + plot_dir)
print("Opening %s" % filename)
file = uproot.open(filename)
tree = file[b'a/tree;1']
print(str(tree.name) + " contains " + str(len(tree)) + " entries")

entrystop = 53605236
nentries = len(tree)
read_entry = 0
i = 0
df_list = []
while read_entry < nentries:
	print("Reading entries between %d and %d" % (read_entry, read_entry + entrystop))
	df = tree.pandas.df([b'ladder', b'pos_x', b'pos_y', b'size', b'cols', b'rows', b'global_eta', b'global_phi', b'instaLumi', b'bx', b'tres'], entrystart=read_entry, entrystop=read_entry + entrystop)
	df_list.append(df)
	print("Saving chunk number %d of dataframe" % (i+1))
	#filename = "/scratch/mmarcheg/csv_files/combined2017_0" + str(i+1) + ".csv"
	#df.to_csv(filename, index=False)
	read_entry += entrystop
	i += 1

print("Readed dataframe in %d chunks" % i)
lumi_bins = [] # Luminosity quantiles

bins_cols = np.linspace(0.5, 20.5, 21)
centroids = np.linspace(1, 20, 20)
eta_list = ['abs(global_eta) < 1', '(abs(global_eta) > 1) & (abs(global_eta) < 2)', 'abs(global_eta) > 2']
eta_range = ['|$\\eta$| < 1', '1 < |$\\eta$| < 2', '|$\\eta$| > 2']
colors = ['red', 'blue', 'green']
n_tot_eta = []
for (j, eta_query) in enumerate(eta_list):
	n_tot = []
	for (i, df) in enumerate(df_list):
		df_eta = df.query(eta_query)
		n, bins, patches = plt.hist(df_eta['cols'], bins=bins_cols)
		n_tot = sp.list_sum(n_tot, n)
		plt.close()
	n_tot_eta.append(n_tot)

for (j, eta_query) in enumerate(eta_list):
	plt.hist(centroids, bins=bins_cols, weights=n_tot_eta[j], color=colors[j], ec=colors[j], histtype='step', label=eta_range[j])

plt.xlabel("cols")
plt.ylabel("# clusters")
plt.legend(loc="upper right")
plt.title("length of clusters")
plt.xticks(centroids)
ax = plt.gca()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.savefig(plot_dir + "cols_distribution.png", format="png", dpi=300)
plt.close()

for (j, eta_query) in enumerate(eta_list):
	plt.hist(centroids, bins=bins_cols, weights=n_tot_eta[j], color=colors[j], ec=colors[j], histtype='step', label=eta_range[j], log=True)

plt.xlabel("cols")
plt.ylabel("# clusters")
plt.legend(loc="upper right")
plt.title("length of clusters")
plt.xticks(centroids)
ax = plt.gca()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.savefig(plot_dir + "cols_distribution_log.png", format="png", dpi=300)
plt.close()
