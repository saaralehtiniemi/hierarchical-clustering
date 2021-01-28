import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import calinski_harabasz_score, silhouette_score, normalized_mutual_info_score

import plot

def clusterNumberTest(n_clusters, affs, links, cdict, **kwargs):
    print("--- TESTING DIFFERRENT CLUSTER SIZES ---")
    # generate the dataframe where scores are stored
    # data for scores: initialize index, where index is
    # k=number of clusters, links=linkage, affs=distance measure
    n = min(kwargs["X"].shape[0]-1, n_clusters+10)
    iterables = [range(2, n), links, affs]
    clust_idx = pd.MultiIndex.from_product(iterables, names=['k', 'links', 'affs'])
    # if class_column is specified, we can calculate NMI (also CHS and SS), otherwise calculate only CHS and SS
    clust_col = (
         ['NMI', "CHS", "SS"] if str(kwargs.get('class_column', False))
        else ["CHS", "SS"]
    )
    # initialize dataframes where scores (df_scores) and predicted labels (df_clust) are saved
    df_scores = pd.DataFrame(columns=clust_col, index=clust_idx)
    df_clust = pd.DataFrame()
    for k in range(2, n): # go through possible n_clusters 
        print("\tTesting: amount of clusters is {}".format(k))
        df_hier, df_hier_clust = HierarchicalClustering(k, links, affs, clust_col, **kwargs) # select fit for the type of clustering
        # save results to df_clust and df_scores
        df_clust = df_clust.append(df_hier_clust)
        df_scores.loc[pd.IndexSlice[k, :, :]] = df_hier.values
    plot.plotScores(df_scores, clust_col, **kwargs) # plot score lines for cluster testing
    df_scores = df_scores.sort_values(by=clust_col, ascending=False) # sort for best values
    # only best are saved as images:
    save_num = int(kwargs["n_plots"])
    print("\t---Saving only top {}---".format(save_num))
    for best_scores in df_scores.iloc[:save_num, :].index:
        k, l, a = best_scores
        kwargs["title"] = str(k)
        plot.plotDendrogram(k, l, a, cdict, **kwargs)
        # do a confusion matrix only if cluster labels are used
        if str(kwargs.get('class_column', False)):
            df_b_clust = df_clust[np.logical_and(df_clust["n_clusters"] == k, df_clust["link-aff"] == l + "_" + a)]
            plot.plotConfusionMatrix(df_b_clust, **kwargs)
    # save the scores and labels 
    df_scores.to_csv(kwargs["output" ] + "ClusterScores.txt")
    df_clust.to_csv(kwargs["output"] + "PredictedLabels.txt")
    
def HierarchicalClustering(n_clusters, links, affs, clust_col, X, **kwargs):
    # initialize df_scores and df_clust
    df_scores = pd.DataFrame(columns = clust_col, index=pd.MultiIndex.from_product([links, affs], names=['links', 'affs']))
    df_clust = pd.DataFrame()
    # go through the possible links and affs
    for aff in affs:
        for link in links:
            # ward can only be used with euclidean
            if link == 'ward' and aff != 'euclidean':
                continue
            print("\t\tlink: {}, aff: {}".format(link, aff))
            # do the clustering
            fit = AgglomerativeClustering(n_clusters=n_clusters, affinity=aff, linkage=link)
            # get the predicted labels
            labels = fit.fit_predict(X)
            df_clust = df_clust.append(pd.DataFrame({'True': X.index.values, 'Predicted': labels, "n_clusters": n_clusters, "link-aff": link+"_"+aff }))
            # save the chs and ss -scores
            df_scores.loc[(link, aff), "CHS"] = calinski_harabasz_score(X, labels)
            df_scores.loc[(link,aff), "SS"] = silhouette_score(X, labels)
            # if class_column is specified, save NMI-score
            if len(clust_col) == 3:
                df_scores.loc[(link,aff), "NMI"] = normalized_mutual_info_score(X.index.values, labels, average_method='geometric')
    return df_scores, df_clust