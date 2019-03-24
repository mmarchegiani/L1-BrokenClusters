import sys, os, pandas
import uproot
import matplotlib.pyplot as plt
import numpy as np

def splitprob(df_full, df_broken, nfull, nbroken, bins=100, varname="", output=True, plot_dir="./"):
	splitmode = "(" + str(nfull) + "->" + str(nbroken) + ")"
	print("Plotting histograms " + splitmode + " " + varname + "...")
	n_full, bins_full, patches_full = plt.hist(df_full[varname], bins=bins, color="yellow", ec="black", histtype="stepfilled", log=True)
	plt.title(varname + " cols=" + str(nfull))

	n_broken, bins_broken, patches_broken = plt.hist(df_broken[varname], bins=bins, color="orange", ec="black", histtype="stepfilled", log=True)
	plt.title(varname + " cols=" + str(nfull) + " size=" + str(nbroken))
	
	if output == True:
		plt.savefig(plot_dir + "cols" + str(nfull) + "_size" + str(nbroken) + "_" + varname + ".png", format="png", dpi=300)
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
	plt.title("prob splitting " + splitmode + " vs " + varname)

	if output == True:
		plt.savefig(plot_dir + "prob_" + varname + str(nfull) + str(nbroken) + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()

	return