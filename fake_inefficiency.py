import sys, os
import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import splitlib as sp

filename = "/scratch/mmarcheg/lumi_data/Run300806.root"
plot_dir = "../ntuplesPixel/plots/fake_inefficiency/"
if not os.path.exists(plot_dir):
	os.makedirs(plot_dir)
print("Plots will be saved in " + plot_dir)
print("Opening %s" % filename)
file = uproot.open(filename)
tree = file[b'a/tree;1']
print(str(tree.name) + " contains " + str(len(tree)) + " entries")

df = tree.pandas.df([b'ladder', b'x', b'y', b'pos_x', b'pos_y', b'size', b'cols', b'rows', b'global_eta', b'global_phi', b'instaLumi', b'bx', b'tres'])

nfull = 7
nbroken = 5
df_grid, df_grid_full, df_grid_broken = sp.sp.select_cols_df(df, nfull, nbroken, selection=False)
df_grid_full = sp.select_rows(df_grid_full, 1)
df_grid_broken = sp.select_rows(df_grid_broken, 1)



