import sys, os, pandas
import uproot
import matplotlib.pyplot as plt
import numpy as np

# Function to plot the histograms of #clusters(variable) where variable is called 'varname'
def splitprob(df_full, df_broken, bins=100, varname="", output=True, plot_dir="./"):
	# To complete: evaluate nfull, nbroken directly from data instead of passing them as parameters
	index_list = df_grid75.index.values		# List of indices of selected data
	nfull = df_full['cols'][index_list[0]]
	nbroken = df_full['size'][index_list[0]]
	nrows = df_full['rows'][index_list[0]]

	varlist = ["global_eta", "global_phi", "instaLumi", "bx", "tres"]
	colors = ["yellow", "blue", "green", "red", "darkturquoise"]
	colors2 = ["darkorange", "deepskyblue", "lawngreen", "tomato", "cornflowerblue"]

	index = varlist.find(varname)

	splitmode = "(" + str(nfull) + "->" + str(nbroken) + ")"
	print("Plotting histograms " + splitmode + " " + varname + "...")
	plt.hist(df_full[varname], bins=bins, color=colors[index], ec="black", histtype="stepfilled", log=True, stacked=True)

	plt.hist(df_broken[varname], bins=bins, color=colors2[index], ec="black", histtype="stepfilled", log=True, stacked=True)
	plt.title(varname + " cols=" + str(nfull) + " size=" + str(nbroken) + " rows=" + str(nrows) + " stacked")
	
	if output == True:
		plt.savefig(plot_dir + "cols" + str(nfull) + "_size" + str(nbroken) + "_rows" + str(nrows) + "_" + varname + "stacked.png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()
	
	n_full, bins_full, patches_full = plt.hist(df_full[varname], bins=bins, color=colors[index], ec="black", histtype="stepfilled")
	plt.title(varname + " cols=" + str(nfull) + " rows=" + str(nrows))

	if output == True:
		plt.savefig(plot_dir + "cols" + str(nfull) + "_rows" + str(nrows) + "_" + varname + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

	n_broken, bins_broken, patches_broken = plt.hist(df_broken[varname], bins=bins, color=colors2[index], ec="black", histtype="stepfilled")
	plt.title(varname + " cols=" + str(nfull) + " size=" + str(nbroken) + " rows=" + str(nrows))

	if output == True:
		plt.savefig(plot_dir + "cols" + str(nfull) + "_size" + str(nbroken) + "_rows" + str(nrows) + "_" + varname + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

	prob = []
	print("Plotting scatter plot of prob" + splitmode + " " + varname + "...")

	bin_size = bins_broken[1] - bins_broken[0]
	bins_broken = np.linspace(start=bins_broken[0] + 0.5*bin_size, stop=bins_broken[-2] + 0.5*bin_size, num=len(bins_broken) - 1, endpoint=True)

	mylist = range(len(bins_broken))
	for i in mylist:
		if n_full[i] == 0:
			bins_broken = np.delete(bins_broken, i)
			n_broken = np.delete(n_broken, i)
			bins_full = np.delete(bins_full, i)
			n_full = np.delete(n_full, i)
		else:
			prob.append(n_broken[i]/n_full[i])

	#bins_broken = np.delete(bins_broken, -1)
	#plt.scatter(bins_broken, prob, marker='.', color='blue', s=3)
	sigma = []
	for i in range(len(prob)):
		sigma.append(float(prob[i]*np.sqrt(1./n_broken[i] + 1./n_full[i])))		# We propagate the error on the ratio assuming poissonian uncertainties

	plt.errorbar(bins_broken, prob, yerr=np.array(sigma), fmt='o', ecolor='r', c='r', label="data")

	plt.xlabel(varname)
	plt.ylabel("prob" + splitmode)
	plt.title("prob splitting " + splitmode + "(rows=" + str(nrows) + ") vs " + varname)

	if output == True:
		plt.savefig(plot_dir + "prob_rows" + str(nrows) + "_" + varname + str(nfull) + str(nbroken) + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

	return

# Function which reads the tree and store the data in 3 dataframes: complete data, cols=nfull data and cols=nfull size=nbroken data
# The 3 dataframes are returned by the function
def select(tree, nfull, nbroken, nrows):
	entrystop_ = None
	if len(tree) > 1.1e8:
		entrystop_ = 1.1e8
		print("Dataframe truncated to 1.1e8 events")
	else:
		print("Dataframe keeped with all the events")
	df_grid = tree.pandas.df([b'size', b'cols', b'rows', b'x', b'y', b'global_eta', b'global_phi', b'instaLumi', b'bx', b'tres'], entrystop=entrystop_)
	print(df_grid.head())

	print("Dataframe query...")
	df_grid_full = df_grid.query('cols == ' + str(nfull) + '& rows == ' + str(nrows))
	df_grid_broken = df_grid7.query('size == ' + str(nbroken))

	return df_grid, df_grid_full, df_grid_broken
