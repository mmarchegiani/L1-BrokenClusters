import sys, os
import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import splitlib as sp

filename = "/scratch/mmarcheg/lumi_data/clusters_V1_Run2017C_Fill6061.root"
plot_dir = "../ntuplesPixel/plots/combined2017_Run05/"
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
instaLumi = np.array([])
for (i, df) in enumerate(df_list):
	print("Dataframe number %d contains %d clusters" % (i+1, len(df)))
	instaLumi = np.concatenate((instaLumi, df['instaLumi'].values))

#df = concat(df_list)
#print("Concat dataframe contains %d clusters" % len(df))
#print(df.head())
print("The vector called 'instaLumi' contains %d elements" % len(instaLumi))

nbins=500
#plt.hist(df['instaLumi'], bins=nbins, facecolor='green', ec='black', histtype='stepfilled')
plt.hist(instaLumi, bins=nbins, facecolor='green', ec='black')
plt.xlabel('instaLumi')
plt.ylabel('entries')
plt.title('instaLumi')
print("Saving " + plot_dir + "instaLumi.png")
plt.savefig(plot_dir + "instaLumi.png", format="png", dpi=300)
plt.close()

nbins=10
lumi_bins = np.quantile(instaLumi, np.linspace(0, 1, nbins+1))
print(lumi_bins)

#plt.hist(df['instaLumi'], bins=nbins, facecolor='green', ec='black', histtype='stepfilled')
plt.hist(instaLumi, bins=lumi_bins, facecolor='green', ec='black')
plt.xlabel('instaLumi')
plt.ylabel('entries')
plt.title('instaLumi | quantiles')
print("Saving " + plot_dir + "instaLumi_quantiles.png")
plt.savefig(plot_dir + "instaLumi_quantiles.png", format="png", dpi=300)
plt.close()

luminame = []
for (i, l) in enumerate(lumi_bins[:-1]):
	luminame.append(str(int(0.5*(lumi_bins[i+1] + lumi_bins[i]))))

#for nfull in [10, 9, 8, 7, 6, 5, 4]:
for nfull in [8, 7, 6, 5, 4]:
	nbroken = nfull - 2
	df_full_list = []
	df_broken_list = []
	for (i, df) in enumerate(df_list):
		print("Selecting chunk %d of dataframe" % (i+1))
		df_grid, df_grid_full, df_grid_broken = sp.select_cols_df(df, nfull, nbroken, selection=True)
		#df_grid_full = df_grid_full.query('tres < 1e7')			# Preliminary selection on tres
		#df_grid_broken = df_grid_broken.query('tres < 1e7')
		df_full_list.append(df_grid_full)
		df_broken_list.append(df_grid_broken)

	for ladder in ["inner", "outer"]:
		# Ladder selection after choosing the binning: in this way either in case "inner" or "outer", we'll have same binning
		n_broken_sum_list = []
		n_full_sum_list = []
		n_broken_tres_sum_list = []
		n_full_tres_sum_list = []
		for (i, item) in enumerate(df_full_list):
			print("---------------------------------------------------")
			print("Selecting chunk %d of dataframe" % (i+1))
			df_grid_full_ladder = pd.DataFrame()
			df_grid_broken_ladder = pd.DataFrame()
			df_grid_full_ladder = sp.select_ladder(df_full_list[i], ladder)
			print("FULL")
			df_grid_broken_ladder = sp.select_ladder(df_broken_list[i], ladder)
			print("BROKEN")
			varlist = ["global_eta", "global_phi", "instaLumi", "bx", "tres"]
			axlist = []
			nbins_eta = 16
			nbins_tres = 20
			#bins = [100, 100, 4, df_grid_full_ladder['bx'].max() - df_grid_full_ladder['bx'].min(), 50]
			bins = [np.linspace(-3.2, -1, nbins_eta + 1).tolist() + np.linspace(+1, +3.2, nbins_eta + 1).tolist(), 100, 4, df_grid_full_ladder['bx'].max() - df_grid_full_ladder['bx'].min(), nbins_tres]
			n_broken_lumi_list = []
			n_full_lumi_list = []
			n_broken_lumi_tres_list = []
			n_full_lumi_tres_list = []
			bins_tres_list = []
			n_broken_sum = []
			n_full_sum = []
			for j in range(len(lumi_bins) - 1):
				df_grid_full_lumi = pd.DataFrame()
				df_grid_broken_lumi = pd.DataFrame()
				df_grid_full_lumi = sp.select_lumi(df_grid_full_ladder, [lumi_bins[j], lumi_bins[j+1]])
				print("FULL")
				df_grid_broken_lumi = sp.select_lumi(df_grid_broken_ladder, [lumi_bins[j], lumi_bins[j+1]])
				print("BROKEN")
				#index_list = df_grid_broken_lumi.index.values		# List of indices of selected data
				#if not df_grid_broken_lumi.shape[0] > 0:
				#	print("Dataframe is empty")
				#	print("No operations will be performed. Continue.")
				#	continue
				# Operation pursued only for var = global_eta
				axlimits, n_broken_lumi, n_full_lumi = sp.splitprob_lumi(df_grid_full_lumi, df_grid_broken_lumi, bins=bins[0], axlimits=[], varname=varlist[0], luminame=luminame[j], output=False, plot_dir=plot_dir)
				bins_tres, n_broken_lumi_tres, n_full_lumi_tres = sp.splitprob_lumi(df_grid_full_lumi, df_grid_broken_lumi, bins=bins[-1], axlimits=[], varname=varlist[-1], luminame=luminame[j], output=False, plot_dir=plot_dir)
				#sp.splitprob_lumi(df_grid_full_lumi, df_grid_broken_lumi, bins=bins[-2], axlimits=[], varname=varlist[-2], luminame=luminame[j] + "_0" + str(i+1), output=True, plot_dir=plot_dir)
				#if (n_broken_lumi != []) & (n_full_lumi != []):
				n_broken_lumi_list.append(n_broken_lumi)
				n_full_lumi_list.append(n_full_lumi)
				n_broken_lumi_tres_list.append(n_broken_lumi_tres)
				n_full_lumi_tres_list.append(n_full_lumi_tres)
				bins_tres_list.append(bins_tres)
				#else:
				#	n_broken_lumi_list.append(np.array([0]*(len(bins[0]) - 1)))
				#	n_full_lumi_list.append(np.array([0]*len((bins[0]) - 1)))
			print(bins_tres_list)
			
			for (j, item) in enumerate(n_broken_lumi_list):
				if i == 0:
					n_broken_sum_list.append(sp.list_sum([], n_broken_lumi_list[j]))
					n_full_sum_list.append(sp.list_sum([], n_full_lumi_list[j]))
				else:
					n_broken_sum_list[j] = sp.list_sum(n_broken_sum_list[j], n_broken_lumi_list[j])
					n_full_sum_list[j] = sp.list_sum(n_full_sum_list[j], n_full_lumi_list[j])

			for (j, item) in enumerate(n_broken_lumi_tres_list):
				if i == 0:
					n_broken_tres_sum_list.append(sp.list_sum([], n_broken_lumi_tres_list[j]))
					n_full_tres_sum_list.append(sp.list_sum([], n_full_lumi_tres_list[j]))
				else:
					n_broken_tres_sum_list[j] = sp.list_sum(n_broken_tres_sum_list[j], n_broken_lumi_tres_list[j])
					n_full_tres_sum_list[j] = sp.list_sum(n_full_tres_sum_list[j], n_full_lumi_tres_list[j])

		for (j, item) in enumerate(n_broken_sum_list):
			print("lumi" + luminame[j])
			bins_eta = np.linspace(-3.2, -1, nbins_eta + 1).tolist() + np.linspace(+1, +3.2, nbins_eta + 1).tolist()
			sp.splitprob_n(n_full_sum_list[j], n_broken_sum_list[j], nfull, nbroken, ladder, bins=bins_eta, varname="global_eta", luminame=luminame[j], output=True, plot_dir=plot_dir)
			sp.splitprob_n(n_full_tres_sum_list[j], n_broken_tres_sum_list[j], nfull, nbroken, ladder, bins=bins_tres_list[j], varname="tres", luminame=luminame[j], output=True, plot_dir=plot_dir)

