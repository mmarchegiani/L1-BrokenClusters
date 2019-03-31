import sys, os
import shutil
import uproot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Function to plot the histograms of #clusters(variable) where variable is called 'varname'
def splitprob(df_full, df_broken, bins=100, axlimits=[], varname="", output=True, plot_dir="./"):
	# To complete: evaluate nfull, nbroken directly from data instead of passing them as parameters
	index_list = df_broken.index.values		# List of indices of selected data
	nfull = df_full['cols'][index_list[0]]
	nbroken = df_full['size'][index_list[0]]
	nrows = df_full['rows'][index_list[0]]
	bx_low = 1980
	bx_high = 2050
	axislist = []

	if nrows < 10:
		rowname = "rows0" + str(nrows)
	else:
		rowname = "rows" + str(nrows)

	main_dir = plot_dir[:]
	plot_dir = plot_dir + rowname + "/"
	plt.rcParams['agg.path.chunksize'] = 10000

	if not os.path.exists(plot_dir):
		os.makedirs(plot_dir)

	shutil.copyfile(main_dir + "index.php", plot_dir + "index.php")

	varlist = ["global_eta", "global_phi", "instaLumi", "bx", "tres"]
	colors = ["yellow", "blue", "green", "red", "darkturquoise"]
	colors2 = ["darkorange", "deepskyblue", "lawngreen", "tomato", "cornflowerblue"]

	index = varlist.index(varname)

	splitmode = "(" + str(nfull) + "->" + str(nbroken) + ")"
	print("Plotting histograms " + splitmode + " " + varname + "...")
	n_full, bins_full, patches_full = plt.hist(df_full[varname], bins=bins, color=colors[index], ec="black", histtype="stepfilled", log=True, stacked=True, label="cols=" + str(nfull))

	plt.hist(df_broken[varname], bins=bins_full, color=colors2[index], ec="black", histtype="stepfilled", log=True, stacked=True, label="broken")
	plt.title(varname + " cols=" + str(nfull) + " size=" + str(nbroken) + " rows=" + str(nrows) + " stacked")
	plt.xlabel(varname)
	plt.ylabel("#clusters")
	plt.legend(loc="best")
	if varname == "bx":
		df_full_bx = df_full.query('bx > ' + str(bx_low) + ' & bx < ' + str(bx_high))
		axislist = [bx_low, bx_high, 0, 10*df_full_bx['bx'].max()]
		plt.axis(axislist)

	
	if output == True:
		plt.savefig(plot_dir + "cols" + str(nfull) + "_size" + str(nbroken) + "_rows" + str(nrows) + "_" + varname + "stacked.png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()
	
	n_full, bins_full, patches_full = plt.hist(df_full[varname], bins=bins, color=colors[index], ec="black", histtype="stepfilled")
	plt.title(varname + " cols=" + str(nfull) + " rows=" + str(nrows))
	plt.xlabel(varname)
	plt.ylabel("#clusters")
	if varname == "bx":
		df_full_bx = df_full.query('bx > ' + str(bx_low) + ' & bx < ' + str(bx_high))
		axislist = [bx_low, bx_high, 0, 1.05*df_full_bx['bx'].max()]
		plt.axis(axislist)

	if output == True:
		plt.savefig(plot_dir + "cols" + str(nfull) + "_rows" + str(nrows) + "_" + varname + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

	n_broken, bins_broken, patches_broken = plt.hist(df_broken[varname], bins=bins_full, color=colors2[index], ec="black", histtype="stepfilled")
	plt.title(varname + " cols=" + str(nfull) + " size=" + str(nbroken) + " rows=" + str(nrows))
	plt.xlabel(varname)
	plt.ylabel("#clusters")
	if varname == "bx":
		df_broken_bx = df_broken.query('bx > ' + str(bx_low) + ' & bx < ' + str(bx_high))
		axislist = [bx_low, bx_high, 0, 1.05*df_broken_bx['bx'].max()]
		plt.axis(axislist)

	if output == True:
		plt.savefig(plot_dir + "cols" + str(nfull) + "_size" + str(nbroken) + "_rows" + str(nrows) + "_" + varname + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

	prob = []
	print("Plotting scatter plot of prob" + splitmode + " " + varname + "...")

	bin_size = bins_broken[1] - bins_broken[0]
	bins_broken = np.linspace(start=bins_broken[0] + 0.5*bin_size, stop=bins_broken[-2] + 0.5*bin_size, num=len(bins_broken) - 1, endpoint=True)

	#n = len(n_full)
	#mylist = range(n)
	#for i in mylist:
	for item in n_full:
		if item == 0:
			prob.append(np.nan)
		else:
			i = list(n_full).index(item)
			prob.append(n_broken[i]/item)

	#bins_broken = np.delete(bins_broken, -1)
	#plt.scatter(bins_broken, prob, marker='.', color='blue', s=3)
	#cov = np.cov(n_broken, n_full)[0][1]
	sigma = []
	sigma_uncorr = []
	for i in range(len(prob)):
		if ((n_broken[i] == 0) | (n_full[i] == 0)):
			sigma.append(np.nan)
			sigma_uncorr.append(np.nan)
		else:
			#sigma.append(float(prob[i]*np.sqrt(1./n_broken[i] + 1./n_full[i] - 2*cov/(n_broken[i]*n_full[i]))))		# We propagate the error on the ratio assuming poissonian uncertainties
			sigma.append(np.sqrt(prob[i]*(1 - prob[i])/n_full[i]))
			sigma_uncorr.append(float(prob[i]*np.sqrt(1./n_broken[i] + 1./n_full[i])))		# We propagate the error on the ratio assuming poissonian uncertainties

	# Calculation of axlimits only in the rows=1 case, otherwise axlimits passed as argument is keeped unchanged
	# rows=2, 3, ... will have same axlimits as rows=1 if opportune axlimits is passed as argument
	if nrows < 2:
		prob_array = np.array(prob)
		maxy = np.nanmax(prob_array)
		imax = np.nanargmax(prob_array)
		maxy = 1.05*(maxy + sigma[imax])

		#axlimits = []
		rangex = bins_full[-1] - bins_full[0]
		gapx = 0.025*rangex
		gapy = 0.025*maxy
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

	plt.errorbar(bins_broken, prob, yerr=np.array(sigma), fmt='o', ecolor='r', c='r', label="data")

	plt.title("prob splitting " + splitmode + "(rows=" + str(nrows) + ") vs " + varname)
	plt.xlabel(varname)
	plt.ylabel("prob" + splitmode)
	plt.grid(True)
	plt.axis(axlimits)

	if output == True:
		plt.savefig(plot_dir + "prob_rows" + str(nrows) + "_" + varname + str(nfull) + str(nbroken) + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

	# Save .csv file with DataFrame of splitting probability graph

	# plot_dir = ../ntuplesPixel/plots/Run300806/rows05/
	
	split_dirs = plot_dir.split("/")
	split_dirs[-4] = "graphdata"
	graph_dir = "/".join(split_dirs)

	# graph_dir = ../ntuplesPixel/plots/Run300806/rows05/

	if not os.path.exists(graph_dir):
		os.makedirs(graph_dir)

	d = {'n_broken' : n_broken, 'n_full' : n_full, varname : bins_broken, 'prob' : prob, 'sigma' : sigma, 'sigma_uncorr' : sigma_uncorr}
	df_graph = pd.DataFrame(data=d)
	filename = graph_dir + "prob_rows" + str(nrows) + "_" + varname + str(nfull) + str(nbroken) + ".csv"
	print("Saving graph data as DataFrame in " + filename)
	df_graph.to_csv(filename, index=False)
	df_graph.head()

	return axlimits

# Function which reads the tree and store the data in 3 dataframes: complete data, cols=nfull data and cols=nfull size=nbroken data
# The 3 dataframes are returned by the function
def select_cols(tree, nfull, nbroken):
	entrystop_ = None
	if len(tree) > 53605236:		# HARDCODED
		entrystop_ = 53605236
		print("Dataframe truncated to %.1E events" % entrystop_)
	else:
		print("Dataframe keeped with all the events")
	df_grid = tree.pandas.df([b'size', b'cols', b'rows', b'x', b'y', b'global_eta', b'global_phi', b'instaLumi', b'bx', b'tres'], entrystop=entrystop_)
	print(df_grid.head())

	print("Dataframe query... Selecting cols==" + str(nfull) + " size==" + str(nbroken))
	df_grid_full = df_grid.query('cols == ' + str(nfull))
	df_grid_broken = df_grid_full.query('size == ' + str(nbroken))

	return df_grid, df_grid_full, df_grid_broken

def select_rows(df, nrows):
	print("Dataframe query... Selecting rows==" + str(nrows))
	df_grid_rows = df.query('rows == ' + str(nrows))
	df_grid_rows.head()
	return df_grid_rows
