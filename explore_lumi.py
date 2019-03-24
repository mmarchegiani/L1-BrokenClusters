import sys, os, pandas
import uproot
# import HDFStore
import matplotlib.pyplot as plt

if(len(sys.argv) < 3):
	sys.argv.append("-nooutput")

output = False
if (sys.argv[2] == "-o") | (sys.argv[2] == "-output"):
	output = True

filename = sys.argv[1]
#filename = "/scratch/mmarcheg/lumi_data/Run300806.root"
plot_dir = "../ntuplesPixel/plots/" + (filename.split("/")[-1]).split(".")[-2] + "/"
#os.mkdir(plot_dir)
if output == True:
	print("Plots will be saved in " + plot_dir)
print("Opening %s" % filename)
file = uproot.open(filename)


#file.allkeys()
tree = file[b'a/tree;1']
#tree.keys()
print(str(tree.name) + " contains " + str(len(tree)) + " entries")

"""
print("Plotting global_eta histogram...")
plt.hist(tree[b'global_eta'].array(), bins=100, facecolor='yellow', ec='black', histtype='stepfilled')
plt.xlabel('global $\eta$')
plt.ylabel('entries')
plt.title('Global $\eta$')

if output == True:
	plt.savefig(plot_dir + "global_eta.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting global_phi histogram...")
plt.hist(tree[b'global_phi'].array(), bins=100, facecolor='blue', ec='black', histtype='stepfilled')
plt.xlabel('global $\phi$')
plt.ylabel('entries')
plt.title('Global $\phi$')
if output == True:
	#plt.savefig(plot_dir + "track_eta.pdf", format="pdf")
	plt.savefig(plot_dir + "global_phi.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()
"""
entrystop_ = None
if len(tree) > 1.1e8:
	entrystop_ = 1.1e8
	print("Dataframe truncated to 1.1e8 events")
else:
	print("Dataframe keeped with all the events")
df_grid = tree.pandas.df([b'pos_x', b'pos_y', b'size', b'cols', b'rows', b'x', b'y', b'global_eta', b'global_phi', b'instaLumi', b'bx'], entrystop=entrystop_)
print(df_grid.head())

#df_grid['pos_x']


import numpy as np
print("Dataframe query...")
df_grid7 = df_grid.query('cols == 7')
df_grid76 = df_grid7.query('size == 6')
df_grid75 = df_grid7.query('size == 5')
df_grid74 = df_grid7.query('size == 4')
df_grid73 = df_grid7.query('size == 3')
plt.figure(figsize=[8.0,6.0])
bins76 = [np.linspace(-0.5,7.5, 9), np.linspace(-0.5,df_grid76['y'].max()+0.5, df_grid76['y'].max()+2)]
bins75 = [np.linspace(-0.5,7.5, 9), np.linspace(-0.5,df_grid75['y'].max()+0.5, df_grid75['y'].max()+2)]
bins74 = [np.linspace(-0.5,7.5, 9), np.linspace(-0.5,df_grid74['y'].max()+0.5, df_grid74['y'].max()+2)]
bins73 = [np.linspace(-0.5,7.5, 9), np.linspace(-0.5,df_grid73['y'].max()+0.5, df_grid73['y'].max()+2)]

print("Plotting grid (7->5) hist2d...")
h = plt.hist2d(df_grid75['x'], df_grid75['y'], bins=bins75)
for y in h[2]:
    plt.axhline(y, h[1][0], h[1][-1], color="white")
for x in h[1]:
    plt.axvline(x, h[2][0], h[2][-1], color="white")
plt.title("cols=7, size=5")
plt.yticks(range(df_grid75['y'].max()+1))
plt.colorbar()
if output == True:
	plt.savefig(plot_dir + "cols7_size5.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()


print("Plotting grid (7->5) events...")
plt.figure(figsize=[8.0,6.0])
index_list = df_grid75.index.values
#print(index_list[0][0])
size = 5
for j in range(6):
    i = index_list[j*size][0]
    plt.subplot(2,3,j+1)
    h = plt.hist2d(df_grid75['x'][i], df_grid75['y'][i], bins=bins75, cmap="Blues", label="event "+str(i))
    plt.yticks(range(df_grid75['y'].max()+1))
    for y in h[2]:
        plt.axhline(y, h[1][0], h[1][-1], color="gray")
    for x in h[1]:
        linewidth_ = 2
        linecolor = "gray"
        if (int(x+0.5)%2) == 0:
            linecolor = "black"
            linewidth_ = 4
        plt.axvline(x, h[2][0], h[2][-1], color=linecolor, linewidth=linewidth_)
    plt.title("cols=7, size=5, event=" + str(i))
    #plt.colorbar()
plt.tight_layout()
plt.subplots_adjust(right=2.0, top=1.5, wspace=0.2)
if output == True:
	plt.savefig(plot_dir + "cols7_size5_events.png", format="png", dpi=300, bbox_inches="tight")
	plt.close()
else:
	plt.show()

print("Plotting grid cols=7 hist...")
plt.figure(figsize=[8.0,6.0])
plt.hist(df_grid76['x'], bins=bins76[0], color="blue", ec="black", label="7->6", log=True)
plt.hist(df_grid75['x'], bins=bins75[0], color="red", ec="black", label="7->5", log=True)
plt.hist(df_grid74['x'], bins=bins74[0], color="green", ec="black", label="7->4", log=True)
plt.hist(df_grid73['x'], bins=bins73[0], color="orange", ec="black", label="7->3", log=True)
plt.title("cols=7")
plt.legend(loc="best")
if output == True:
	plt.savefig(plot_dir + "cols7_hist.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

#df_grid75.head()

print("Plotting grid (7->5) global_eta...")
n_eta7, bins_eta7, patches = plt.hist(df_grid7['global_eta'], bins=100, color="yellow", ec="black", histtype="stepfilled")
plt.close()
n_eta75, bins_eta75, patches = plt.hist(df_grid75['global_eta'], bins=100, color="yellow", ec="black", histtype="stepfilled")
plt.title("Global eta (7->5)")
prob_eta75 = []

if output == True:
	plt.savefig(plot_dir + "cols7_size5_eta.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting scatter plot of prob_eta75...")

step = bins_eta75[1] - bins_eta75[0]
for i in range(len(bins_eta75)-1):
	if n_eta7[i] == 0:
		prob_eta75.append(np.nan)
	else:
		prob_eta75.append(n_eta75[i]/n_eta7[i])
bins_eta75 = np.delete(bins_eta75, -1)
plt.scatter(bins_eta75, prob_eta75, marker='.', color='blue', s=3)
plt.xlabel('eta')
plt.ylabel('prob splitting(7->5)')
plt.title('prob splitting (7->5) vs eta')
if output == True:
	plt.savefig(plot_dir + "prob_eta75.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting grid (7->5) global_phi...")
n_phi7, bins_phi7, patches = plt.hist(df_grid7['global_phi'], bins=100, color="blue", ec="black", histtype="stepfilled")
plt.close()
n_phi75, bins_phi75, patches = plt.hist(df_grid75['global_phi'], bins=100, color="blue", ec="black", histtype="stepfilled")
plt.title("Global phi (7->5)")
if output == True:
	plt.savefig(plot_dir + "cols7_size5_phi.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()
#plt.hist(df_grid75['global_phi'], color="green", ec="black", histtype="stepfilled")

step = bins_phi75[1] - bins_phi75[0]
for i in range(len(bins_phi75)):
	if n_phi7[i] == 0:
		prob_phi75.append(np.nan)
	else:
		prob_phi75.append(n_phi75[i]/n_phi7[i])
bins_phi75 = np.delete(bins_phi75, -1)
plt.scatter(bins_phi75, prob_phi75, marker='.', color='blue', s=3)
plt.xlabel('phi')
plt.ylabel('prob splitting(7->5)')
plt.title('prob splitting (7->5) vs phi')
if output == True:
	plt.savefig(plot_dir + "prob_phi75.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting grid (7->5) instaLumi...")
n_lumi7, bins_lumi7, patches = plt.hist(df_grid7['instaLumi'], bins=20, color="green", ec="black", histtype="stepfilled")
plt.close()
n_lumi75, bins_lumi75, patches = plt.hist(df_grid75['instaLumi'], bins=20, color="green", ec="black", histtype="stepfilled")
plt.title("instaLumi (7->5)")
if output == True:
	plt.savefig(plot_dir + "cols7_size5_instaLumi.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

step = bins_lumi75[1] - bins_lumi75[0]
for i in range(len(bins_lumi75)):
	if n_lumi7[i] == 0:
		prob_lumi75.append(np.nan)
	else:
		prob_lumi75.append(n_lumi75[i]/n_lumi7[i])
bins_lumi75 = np.delete(bins_lumi75, -1)
plt.scatter(bins_lumi75, prob_lumi75, marker='.', color='blue', s=3)
plt.xlabel('lumi')
plt.ylabel('prob splitting(7->5)')
plt.title('prob splitting (7->5) vs lumi')
if output == True:
	plt.savefig(plot_dir + "prob_lumi75.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting grid (7->5) bx...")
n_bx7, bins_bx7, patches = plt.hist(df_grid7['bx'], bins=50, color="red", ec="black", histtype="stepfilled", log=True)
plt.close()
n_bx75, bins_bx75, patches = plt.hist(df_grid75['bx'], bins=50, color="red", ec="black", histtype="stepfilled", log=True)
plt.title("bx (7->5)")
if output == True:
	plt.savefig(plot_dir + "cols7_size5_bx.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

step = bins_bx75[1] - bins_bx75[0]
for i in range(len(bins_bx75)):
	if n_bx7[i] == 0:
		prob_bx75.append(np.nan)
	else:
		prob_bx75.append(n_bx75[i]/n_bx7[i])
bins_bx75 = np.delete(bins_bx75, -1)
plt.scatter(bins_bx75, prob_bx75, marker='.', color='blue', s=3)
plt.xlabel('bx')
plt.ylabel('prob splitting(7->5)')
plt.title('prob splitting (7->5) vs bx')
if output == True:
	plt.savefig(plot_dir + "prob_bx75.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()
