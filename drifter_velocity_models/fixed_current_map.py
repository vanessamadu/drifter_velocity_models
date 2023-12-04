# import packages
import pandas as pd
import numpy as np

# calculate drifter speed from data and add the corresponding column to the data
def new_col_drifter_speed(u_array,v_array,data):
    drifter_speed = np.array([u**2+v**2 for u,v in zip(u_array,v_array)])
    data["Drifter Speed"] = drifter_speed







# load data
data = pd.read_hdf("ocean_data.h5")
# add drifter speed column to data




