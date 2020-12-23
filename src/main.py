import matplotlib as mpl
import argparse
import os

import plot
import load
import cluster

import warnings
warnings.filterwarnings("ignore")

def main():
    parser = argparse.ArgumentParser(description='Hierachical Clustering')
    parser.add_argument('file', help='Choose data file', type=str)
    parser.add_argument('--output', help='Output folder for the results', default='results')
    parser.add_argument('--class_column', help='Column in file which contains the classes', default="")
    parser.add_argument('--n_plots', help='Number of plotted images', type=int, default=3)
    
    args = parser.parse_args()
    
    # go through given data files
    # go through given class columns
    cols = str(args.class_column).replace(" ", "").split(",") 
    files = str(args.file).replace(" ", "").split(",")
    # if less class_column values given, assume that the same column is used for all data files
    for i in range(len(files) - len(cols)):
        cols.append(cols[-1])
    output = args.output
    for i, file in enumerate(files):
        args.X, args.class_column, args.names = load.loadDataFile(file, cols[i])
        print("Size of the datafile: {}\n\t(Note: the more data there are, the longer the algorithm takes to run.)".format(args.X.shape[0]))  
        # create output folder: optionally specified folder + name of the data file
        title = str(file.split("/")[-1].split(".")[-2])
        args.title = (
            title + "_" + str(args.class_column) if str(args.class_column)
            else title
        )
        args.output = output + "/" + args.title + "/"   
        if not os.path.exists(args.output):            
            print("Generating folder {}".format(args.output))
            os.makedirs(args.output)        
        #save the dataframe    
        args.X.to_csv(args.output + "DATA.csv")
        
        # run model
        run_model(**vars(args))
        print("")

def run_model(**kwargs):
    '''
    clustering methods for the data
    '''      
    idx = kwargs.get('X', False).index.unique() # select classes 
    # the number of classes for clustering - if the classes are predefined, pass their number; otherwise 
    n_clusters = (
         len(idx) if str(kwargs.get('class_column', False))
        else min(int(len(idx)/5), 5)
    )

    print("Number of classes: {}".format(len(idx)))
    
    # get unified colors for the classes
    cmap = mpl.cm.get_cmap('nipy_spectral') # selecting the nipy_spectral -colormap  
    norm = mpl.colors.Normalize(vmin=min(idx), vmax=max(idx)) # the colors values are normalized, so the colors we get are as different as possible
    cdict = {}   
    for i in range(n_clusters): # generate the unique colors for each color --> select a color using 
        color = cmap(norm(idx[i]))
        cdict[str(idx[i])] = color # save the generated color to a dictionary

    # initialize hierachical linkage and affinity
    # options seen on https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
    links = ['ward', 'complete', 'average', 'single']
    affs = ['euclidean', 'cityblock', 'cosine']
    
    
    # testing different cluster numbers
    cluster.clusterNumberTest(n_clusters, affs, links, cdict, **kwargs)
    
if __name__ == '__main__':
    main()