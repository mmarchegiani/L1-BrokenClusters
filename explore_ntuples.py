
# coding: utf-8

# In[47]:

import sys, pandas
import uproot
# import HDFStore
import matplotlib.pyplot as plt


# In[48]:

if(len(sys.argv) < 3):
	sys.argv.append("-nooutput")

output = False
if (sys.argv[2] == "-o") | (sys.argv[2] == "-output"):
	output = True

filename = sys.argv[1]
#filename = "../ntuplesPixel/debugHits_MC_ZMM_CluRefFull_BIS.root"
plot_dir = "../ntuplesPixel/plots/" + filename.split("_")[-2] + "/"
if output == True:
	print("Plots will be saved in " + plot_dir)
file = uproot.open(filename)


# In[49]:

file.allkeys()


# In[50]:

tree = file[b'clusterInfo/tree;9']


# In[51]:

tree.keys()


# In[52]:

# tree.pandas.df().to_pickle("debugHits_MC_ZMM_CluRefFull_BIS.pkl")
print("%s in %s contains %d ntuples." % (tree.name, filename, len(tree)))

# In[53]:
print("Plotting track_eta...")
plt.hist(tree[b'track_eta'].array(), facecolor='yellow', ec='black', histtype='stepfilled')
plt.xlabel('track $\eta$')
plt.ylabel('entries')
plt.title('Track $\eta$')
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
#plt.rc('axes', axisbelow=True)
#plt.grid(True)
if output == True:
	#plt.savefig(plot_dir + "track_eta.pdf", format="pdf")
	plt.savefig(plot_dir + "track_eta.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting track_local_Dx...")
plt.hist(tree[b'track_local_Dx'].array(), bins=50, facecolor='blue', alpha=0.5, ec='black', histtype='stepfilled')
plt.xlabel('track_local_Dx')
plt.ylabel('entries')
plt.title('track_local_Dx')
if output == True:
	#plt.savefig(plot_dir + "track_eta.pdf", format="pdf")
	plt.savefig(plot_dir + "track_local_Dx.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting track_local_Dy...")
plt.hist(tree[b'track_local_Dy'].array(), bins=50, facecolor='red', alpha=0.5, ec='black', histtype='stepfilled')
plt.xlabel('track_local_Dy')
plt.ylabel('entries')
plt.title('track_local_Dy')
if output == True:
	#plt.savefig(plot_dir + "track_eta.pdf", format="pdf")
	plt.savefig(plot_dir + "track_local_Dy.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()


    
# In[54]:
print("Plotting scatter plots hit_sizeX, hit_sizeY vs track_eta...")
plt.subplot(1,2,1)
plt.scatter(tree[b'track_eta'].array(),tree[ b'hit_sizeX'].array(), marker='.', color='blue', s=1)
plt.xlabel('track $\eta$')
plt.ylabel('hit_sizeX')
plt.title('Hit X size vs $\eta$')
plt.subplot(1,2,2)
plt.scatter(tree[b'track_eta'].array(),tree[ b'hit_sizeY'].array(), marker='.', color='red', s=1)
plt.xlabel('track $\eta$')
plt.ylabel('hit_sizeX')
plt.title('Hit Y size vs $\eta$')
plt.tight_layout()
plt.subplots_adjust(bottom=0.0, top= 1.0, left=0.1, right=2.0)

if output == False:
	plt.show()
plt.close()


# Hit X size seems to be close to zero, while hit Y size seems to correlate with $\eta$.
# We expect in fact "longer" clusters with the increasing of $\eta$ since we are getting far from the IP.
# 
# Some events at around $|\eta| \in [2,3]$ are strange because they have an extremely high hit size in x direction. We try to exclude them to see the behavior of hit X size for small size.

# In[55]:

df_all = tree.pandas.df([b'track_eta',b'hit_sizeX',b'hit_sizeY', b'hit_charge'])
df_all.head()

threshold = 3e5
print("Selecting events with hit_sizeX < %f" % threshold)
df_all = df_all.query('abs(hit_sizeX) < 3e5')

#plt.subplot(1,2,1)
print("Plotting scatter plots hit_sizeX, hit_sizeY vs track_eta with hit_sizeX < 1e6...")
plt.scatter(df_all['track_eta'],df_all['hit_sizeX'], marker='.', color='blue', s=1)
plt.xlabel('track $\eta$')
plt.ylabel('hit_sizeX')
plt.title('Hit X size vs $\eta$')
#plt.savefig(plot_dir + "hit_sizeX_vs_track_eta.pdf", format="pdf")
if output == True:
	plt.savefig(plot_dir + "hit_sizeX_vs_track_eta.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

#plt.subplot(1,2,2)
plt.scatter(df_all['track_eta'],df_all['hit_sizeY'], marker='.', color='red', s=1)
plt.xlabel('track $\eta$')
plt.ylabel('hit_sizeY')
plt.title('Hit Y size vs $\eta$')
#plt.tight_layout()
#plt.subplots_adjust(bottom=0.0, top= 1.0, left=0.1, right=2.0)
#plt.savefig(plot_dir + "hit_sizeY_vs_track_eta.pdf", format="pdf")
if output == True:
	plt.savefig(plot_dir + "hit_sizeY_vs_track_eta.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print(df_all.corr())


# In[56]:

#plt.subplot(1,2,1)
print("Plotting hisograms of hit_sizeX, hit_sizeY...")
plt.hist(df_all['hit_sizeX'], bins=40, facecolor='blue', ec='black', log=True)
plt.xlabel('hit_sizeX')
plt.ylabel('entries')
plt.title('Hit size X')
if output == True:
	plt.savefig(plot_dir + "hit_sizeX.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()
#plt.subplot(1,2,2)
plt.hist(df_all['hit_sizeY'], bins=40, facecolor='red', ec='black', log=True)
plt.xlabel('hit_sizeY')
plt.ylabel('entries')
plt.title('Hit size Y')
if output == True:
	plt.savefig(plot_dir + "hit_sizeY.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting scatter plot of hit_sizeX vs hit_charge...")
plt.scatter(df_all['hit_charge'],df_all['hit_sizeX'], marker='.', color='blue', s=1)
plt.xlabel('hit_charge')
plt.ylabel('hit_sizeX')
plt.title('Hit X size vs hit_charge')
if output == True:
	plt.savefig(plot_dir + "hit_sizeX_vs_hit_charge.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting scatter plot of hit_sizeY vs hit_charge...")
plt.scatter(df_all['hit_charge'],df_all['hit_sizeY'], marker='.', color='red', s=1)
plt.xlabel('hit_charge')
plt.ylabel('hit_sizeY')
plt.title('Hit Y size vs hit_charge')
if output == True:
	plt.savefig(plot_dir + "hit_sizeY_vs_hit_charge.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()

print("Plotting scatter plot of hit_charge vs track_eta...")
plt.scatter(df_all['track_eta'],df_all['hit_charge'], marker='.', color='yellow', s=1)
plt.xlabel('track $\eta$')
plt.ylabel('hit_charge')
plt.title('hit_charge vs track $\eta$')
if output == True:
	plt.savefig(plot_dir + "hit_charge_vs_track_eta.png", format="png", dpi=300)
	plt.close()
else:
	plt.show()


# In[63]:
print("Assigning dataframe of hits variables...")
df_hit = tree.pandas.df([b'All_hits_charge', b'All_hits_Px', b'All_hits_Py', 
                         b'cluster_center_x', b'cluster_center_y', 
                         b'hit_sizeX', b'hit_sizeY',
                         b'track_eta',b'track_phi',
                         b'track_local_x', b'track_local_y',
                         b'track_exp_sizeX', b'track_exp_sizeY', b'track_exp_charge',

                         ])
count_hit = df_hit.count()
#print(count_hit[0]/len(tree))
print(count_hit)
# df_sel = df_all.loc[(df_all['hit_sizeX'] < 1e6) ]


# In[58]:
plt.hist(df_hit['All_hits_Px'], color= 'blue', ec='black', histtype='stepfilled')
if output == False:
	plt.show()
plt.hist(df_hit['All_hits_Py'], color= 'red', ec='black', histtype='stepfilled')
if output == False:
	plt.show()


# In[59]:
plt.hist(df_hit['cluster_center_x'], color='blue', ec='black', histtype='stepfilled')
if output == False:
	plt.show()
plt.hist(df_hit['cluster_center_y'], color='red', ec='black', histtype='stepfilled')
if output == False:
	plt.show()


# In[60]:
for i in range(5):
	print("Plotting scatter plot of (Px, Py) hits positions for cluster number %d with cluster center..." % i)
	plt.figure()
	plt.scatter(df_hit['All_hits_Px'][i],df_hit['All_hits_Py'][i])
	plt.xlabel('All_hits_Px')
	plt.ylabel('All_hits_Py')
	plt.title('All_hits_Py vs All_hits_Px')
	plt.scatter(df_hit['cluster_center_x'][i],df_hit['cluster_center_y'][i])
	if output == True:
		plt.savefig(plot_dir + "Py_vs_Px" + str(i) + ".png", format="png", dpi=300)
		plt.close()
	else:
		plt.show()


# In[ ]:
print("Plotting histogram of All_hits_charge...")
plt.hist(df_hit['All_hits_charge'], color='yellow', ec='black', histtype='stepfilled')
plt.xlabel('All_hits_charge')
plt.ylabel('entries')
plt.title('All_hits_charge')
#plt.rc('axes', axisbelow=True)
#plt.grid(True)
#plt.savefig(plot_dir + "track_eta.pdf", format="pdf")
if output == True:
	plt.savefig(plot_dir + "All_hits_charge.png", bins=20, format="png", dpi=300)
	plt.close()
else:
	plt.show()

# In[ ]:

#print(df_hit['All_hits_charge'][0])
for i in range(5):
	print("Plotting scatter plot of All_hits_charge vs All_hits_Px for cluster number %d..." % i)
	plt.scatter(df_hit['All_hits_Px'][i], df_hit['All_hits_charge'][i])
	plt.xlabel('All_hits_Px')
	plt.ylabel('All_hits_charge')
	plt.title('All_hits_charge vs All_hits_Px')
	if output == True:
		plt.savefig(plot_dir + "charge_vs_Px"+ str(i) + ".png", bins=20, format="png", dpi=300)
		plt.close()
	else:
		plt.show()

for i in range(5):
	print("Plotting scatter plot of All_hits_charge vs cluster_center_x for cluster number %d..." % i)
	plt.scatter(df_hit['cluster_center_x'][i], df_hit['All_hits_charge'][i])
	plt.xlabel('cluster_center_x')
	plt.ylabel('All_hits_charge')
	plt.title('All_hits_charge vs cluster_center_x')
	if output == True:
		plt.savefig(plot_dir + "charge_vs_centerx" + str(i) + ".png", bins=20, format="png", dpi=300)
		plt.close()
	else:
		plt.show()
       



