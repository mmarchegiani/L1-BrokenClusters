import sys, os, pandas
import shutil
import uproot
import matplotlib.pyplot as plt
import numpy as np

# Function to plot the histograms of #clusters(variable) where variable is called 'varname'
def splitprob(df_full, df_broken, bins=100, varname="", output=True, plot_dir="./"):
	# To complete: evaluate nfull, nbroken directly from data instead of passing them as parameters
	index_list = df_broken.index.values		# List of indices of selected data
	nfull = df_full['cols'][index_list[0]]
	nbroken = df_full['size'][index_list[0]]
	nrows = df_full['rows'][index_list[0]]
	bx_low = 1980
	bx_high = 2050

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
		plt.axis([bx_low, bx_high, 0, 10*df_full_bx['bx'].max()])
		#plt.xlim(bx_low, bx_high)
	
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
		plt.axis([bx_low, bx_high, 0, 1.05*df_full_bx['bx'].max()])
		#plt.xlim(bx_low, bx_high)

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
		plt.axis([bx_low, bx_high, 0, 1.05*df_broken_bx['bx'].max()])
		#plt.xlim(bx_low, bx_high)

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
	sigma = []
	for i in range(len(prob)):
		if ((n_broken[i] == 0) | (n_full[i] == 0)):
			sigma.append(np.nan)
		else:
				sigma.append(float(prob[i]*np.sqrt(1./n_broken[i] + 1./n_full[i])))		# We propagate the error on the ratio assuming poissonian uncertainties

	plt.errorbar(bins_broken, prob, yerr=np.array(sigma), fmt='o', ecolor='r', c='r', label="data")

	plt.title("prob splitting " + splitmode + "(rows=" + str(nrows) + ") vs " + varname)
	plt.xlabel(varname)
	plt.ylabel("prob" + splitmode)
	if varname == "bx":
		plt.xlim(bx_low, bx_high)

	if output == True:
		plt.savefig(plot_dir + "prob_rows" + str(nrows) + "_" + varname + str(nfull) + str(nbroken) + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

	return

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
