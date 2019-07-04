import sys, os
import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import splitlib as sp

filename = "/scratch/mmarcheg/lumi_data/Run305064.root"
plot_dir = "../ntuplesPixel/plots/lumivstime/"
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
	df = tree.pandas.df([b'instaLumi', b'bx', b'orbit'], entrystart=read_entry, entrystop=read_entry + entrystop)
	df_list.append(df)
	print("Saving chunk number %d of dataframe" % (i+1))
	#filename = "/scratch/mmarcheg/csv_files/combined2017_0" + str(i+1) + ".csv"
	#df.to_csv(filename, index=False)
	read_entry += entrystop
	i += 1
print("Readed dataframe in %d chunks" % i)
instaLumi = np.array([])
orbit = np.array([])
for (i, df) in enumerate(df_list):
	print("Dataframe number %d contains %d clusters" % (i+1, len(df)))
	print("Deleting duplicates...")
	df.drop_duplicates(subset=None, keep='first', inplace=True)
	print("Dataframe number %d contains %d clusters" % (i+1, len(df)))
	instaLumi = np.concatenate((instaLumi, df['instaLumi'].values))
	orbit = np.concatenate((orbit, df['orbit'].values))

print("The vector called 'instaLumi' contains %d elements" % len(instaLumi))

plt.grid(True, linestyle='-')
plt.scatter(0.0000889*orbit, instaLumi, marker='.', color='blue', s=3)
plt.text(35000, 13000, "8b4e bunch fill", bbox=dict(facecolor='yellow', alpha=0.75))
plt.xlabel('time [s]')
plt.ylabel('instaLumi [$10^{30}$ $cm^{-2} s^{-1}$]')
plt.title('Instantaneous luminosity')
print("Saving " + plot_dir + "lumi_vs_time_8b4e.png")
plt.savefig(plot_dir + "lumi_vs_time_8b4e.png", format="png", dpi=300)
plt.close()
