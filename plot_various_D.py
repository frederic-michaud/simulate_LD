import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

cwd = os.getcwd()
print(cwd)
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

simulation_subfolder = ""
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd,simulation_subfolder)
thetas = [100,1000,10000,100000, 1000000]
thetas = [100,1000]
allTime = []
for theta in thetas:
    distanceFile = os.path.join(simulation_subfolder,f'theta_{theta}.txt')
    distances1  = np.loadtxt(distanceFile)
    distanceFile = os.path.join(simulation_subfolder,f'theta_{theta}_without_linkage_removale.txt')
    distances2  = np.loadtxt(distanceFile)
    for i in range(len(distances1)):
        allTime.append((theta,distances1[i],distances2[i]))


allTime = np.array(allTime)
dico = {"Theta": allTime[:,0], "distance_pruned" :allTime[:,1],"distance_not_pruned" :allTime[:,2]}
all_dist = pd.DataFrame(data = dico)
all_dist["Theta"] = all_dist["Theta"].astype("int").astype('category')
mean_dist_by_L = all_dist.groupby("Theta").mean()
print(all_dist)
ax = sns.violinplot(x = "Theta", y="distance_pruned",data = all_dist,scale="width",
                     inner="quartiles", color = colors[0], alpha =.5,
                     linewidth=0.)
ax.plot(range(len(thetas)),  mean_dist_by_L.values[:,0],"_",color = colors[0],markersize=7, label = "Distance removing linkage")

sns.violinplot(x = "Theta", y="distance_not_pruned",data = all_dist,scale="width",
                     inner="quartiles", color = colors[2], alpha =.5,
                     linewidth=0.)
plt.setp(ax.collections, alpha=.5)

ax.plot(range(len(thetas)),  mean_dist_by_L.values[:,1],"_",color = colors[2],markersize=7, label = "Distance without removing linkage")
plt.axhline(y=1.1, c = "k", lw = 0.5)
plt.legend()
plt.show()
#plt.savefig("compare_pca_mds.pdf")