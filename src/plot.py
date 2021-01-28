import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
from matplotlib.lines import Line2D

# font and fig size for images
small = 8
large = 2*small
fgsz_confusion = (10,5)
fgsz = (15, 7)
fgsz_dendrogram=(25, 5)
sns.set(font_scale=0.8)

def plotDendrogram(n_clusters, link, aff, cdict, title, X, output, names, **kwargs):
    '''
    Plot dendrograms
    '''
    # initialize image
    plt.figure(figsize=fgsz_dendrogram)
    ax = plt.gca()
    # calculate distances between the data points
    dist = shc.linkage(X, method=link, metric=aff, optimal_ordering=True)
    # select color threshold - used to color the dendrogram links in n_cluster-colors
    ct=dist[-(n_clusters-1), 2]
    # get labels - either specified cluster labels or just the index (running numbers from 0 to len(X)
    lbl = X.index
    # do the dendrogram
    dend = shc.dendrogram(dist, labels=lbl, leaf_font_size=3, leaf_rotation=0, ax=ax, color_threshold=ct, distance_sort=False, show_leaf_counts=True, count_sort=False)
    # set yscale to logarithmic
    ax.set_yscale('symlog', nonposy='clip', linthreshy=0.01)
    # set the ytick labels to the logarithmic
    ax.set_yticklabels(ax.get_yticks())
    # set the ylabel
    plt.ylabel("Distance")
    # color the leaves and if names have been specified, add legend
    
    if str(kwargs.get('cluster_column', False)):
        # we need to write the labels for the legend manually 
        # initialize the lists needed
        custom_lines = []
        custom_names = []
        for l in lbl.unique():
            custom_lines.append(Line2D([0], [0], marker='o', color=cdict[str(l)], markersize=8))
            if names.get(l, False):
                custom_names.append(names[l]) 
        ax.legend(custom_lines, custom_names, frameon=False, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1) # add the legends
        # the leaf colors need to be written manually
        xlbls = ax.get_xmajorticklabels() # get the tick labels
        labels = ['\u25cf'] * len(xlbls) # the labels are colored balls
        for lbl in xlbls:
            lbl.set_color(cdict[lbl.get_text()])
        ax.set_xticklabels(labels)
    
    # now, save the dendogram image
    plt.title("n_Clusters: {}, Linkage: {}, Affinity: {}".format(n_clusters, link, aff))
    file = output + title + "_" + link + "_" + aff + '_Dendrogram.png'
    plt.savefig(file)
    plt.close()

def plotConfusionMatrix(df_clust, names, title, output, **kwargs):
    '''
    Plot confusion matrix
    '''
    las = df_clust["link-aff"].unique() # list link-affs   
    df_clust = df_clust.replace({"True": names}) # if names are given, replace the cluster numbers with names
    for i, la in enumerate(las): # go through link-affs
        fig, ax = plt.subplots(1, 1, figsize=fgsz_confusion)  # initialize plot   
        df_crosstab = df_clust.loc[df_clust["link-aff"] == la, :] # filter data
        df_crosstab = pd.crosstab(df_crosstab["True"], df_crosstab['Predicted']+1) # perform crosstab for confusion matrix
        sns.heatmap(df_crosstab, annot=True, fmt='.0f', ax=ax, annot_kws={'size': small}, mask=(df_crosstab==0)) # plot crosstab as heatmap, don't show zeros
        ax.set_title(la) # set title for the image
        plt.savefig(output + title +"_"+ la + "_ConfusionMatrix.png") # save that image

def plotScores(df, clust_col, output, **kwargs):
    '''
    Plot cluster test scores
    '''
    # display the results in an image
    fig, ax = plt.subplots(1, len(df.columns), figsize=fgsz)  
    # set title
    fig.suptitle("Cluster scores", fontsize=large)
    # plot the lines
    legend = ""
    # go through the scores 
    for i, score in enumerate(clust_col):
        df_plot = df[score].reset_index().copy() # get the values for the score
        df_plot['la'] = df_plot['links'] + ", " + df_plot['affs'] # get the legend - "links, affs"
        df_plot = df_plot.drop(columns=["links", "affs"]).pivot(index='k', columns='la', values=score) # pivot the table
        legend = df_plot.columns.values # get the legend
        df_plot.plot(kind="line", ax=ax[i], legend=False) # save the plot to the corresponding axis
        ax[i].set_title(score) # set the title
    # save the image in a file
    fig.legend(legend, frameon=False, loc='center right', borderpad=0, fontsize=small)
    plt.savefig(output + "ClusterScores.png")
