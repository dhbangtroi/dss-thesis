# Libraries to visualize data
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from MulticoreTSNE import MulticoreTSNE as TSNE
import umap.umap_ as umap
import seaborn as sns
import matplotlib.cm as cm

# Libraries for monitoring operation process
from datetime import datetime


def compute_cluster_visualization(X, pca=True, compute_umap=True, tsne=True, seed=6886, metric='euclidean', perplexity=50):
    if not (pca or compute_umap or tsne):
        raise Exception("At least 1 visualization method is selected!")

    if pca and metric == 'precomputed':
        raise Exception(
            'PCA cannot be computed with precomputed distance matrix!')

    if pca:
        # Visualize clusters by PCA
        start_pca_time = datetime.now()
        print("Start PCA", start_pca_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

        pca = PCA(n_components=2, random_state=seed).fit(X)
        pca_datapoint = pca.transform(X)
        #         centroidpoint = pca.transform(centroids)

        end_pca_time = datetime.now()
        print("End PCA", end_pca_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
        print("PCA duration", end_pca_time - start_pca_time)

    if compute_umap:
        # Visualize clusters by UMAP
        start_umap_time = datetime.now()
        print("Start UMAP", start_umap_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

        umap_reducer = umap.UMAP(
            n_neighbors=perplexity, random_state=seed, verbose=True)
        umap_datapoint = umap_reducer.fit_transform(X)

        end_umap_time = datetime.now()
        print("End UMAP", end_umap_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
        print("UMAP duration", end_umap_time - start_umap_time)

    if tsne:
        # Visualize clusters by t-SNE
        start_tsne_time = datetime.now()
        print("Start t-SNE", start_tsne_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

        tsne = TSNE(n_components=2, random_state=seed, perplexity=perplexity,
                    method="barnes_hut", metric=metric, n_jobs=-1, verbose=1)
        # tsne = TSNE(n_components=2, perplexity=30.0, n_iter=100,
        #             random_state=seed, metric=metric)
        tsne_datapoint = tsne.fit_transform(X)

        end_tsne_time = datetime.now()
        print("End t-SNE", end_tsne_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
        print("t-SNE duration", end_tsne_time - start_tsne_time)

    if pca and compute_umap and tsne:
        return pca_datapoint, umap_datapoint, tsne_datapoint
    elif pca and tsne:
        return pca_datapoint, None, tsne_datapoint
    elif pca and compute_umap:
        return pca_datapoint, umap_datapoint, None
    elif compute_umap and tsne:
        return None, umap_datapoint, tsne_datapoint
    elif pca:
        return pca_datapoint, None, None
    elif compute_umap:
        return None, umap_datapoint, None
    elif tsne:
        return None, None, tsne_datapoint
    else:
        return None, None, None


def visualize_cluster(plot_title, figsize, colors, palette, dot_size, pca_datapoint, tsne_datapoint, umap_datapoint, pca=True, tsne=True, compute_umap=True, save_plots=True, plot_file='visualization_plots.png'):
    if pca and compute_umap and tsne:
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=figsize)
    elif pca and tsne:
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=figsize)
    elif pca and compute_umap:
        fig, (ax1, ax3) = plt.subplots(nrows=2, ncols=1, figsize=figsize)
    elif compute_umap and tsne:
        fig, (ax2, ax3) = plt.subplots(nrows=2, ncols=1, figsize=figsize)
    elif pca:
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    elif tsne:
        fig, ax2 = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    elif compute_umap:
        fig, ax3 = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    else:
        raise Exception("At least 1 visualization method is selected!")

    if pca:
        # Visualize clusters by PCA
        start_pca_time = datetime.now()
        print("Start PCA", start_pca_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

        ax1.set_title("PCA", fontweight="extra bold",
                      fontsize="x-large", color="brown")
        ax1.scatter(
            pca_datapoint[:, 0], pca_datapoint[:, 1], c=colors, alpha=0.7, cmap=palette, s=dot_size
        )
        # ax1.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker="^", c="#ff0000")
        ax1.axis('off')
        end_pca_time = datetime.now()
        print("End PCA", end_pca_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
        print("PCA duration", end_pca_time - start_pca_time)
        print()

    if tsne:
        # Visualize clusters by t-SNE
        start_tsne_time = datetime.now()
        print("Start t-SNE", start_tsne_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

        ax2.set_title("t-SNE", fontweight="extra bold",
                      fontsize="x-large", color="brown")
        ax2.scatter(
            tsne_datapoint[:, 0], tsne_datapoint[:, 1], marker=".", c=colors, alpha=0.7, cmap=palette, s=dot_size
        )
        ax2.axis('off')
        end_tsne_time = datetime.now()
        print("End t-SNE", end_tsne_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
        print("t-SNE duration", end_tsne_time - start_tsne_time)
        print()

    if compute_umap:
        # Visualize clusters by UMAP
        start_umap_time = datetime.now()
        print("Start UMAP", start_umap_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

        ax3.set_title("UMAP", fontweight="extra bold",
                      fontsize="x-large", color="brown")
        ax3.scatter(
            umap_datapoint[:, 0], umap_datapoint[:, 1], marker=".", c=colors, alpha=0.7, cmap=palette, s=dot_size
        )
        ax3.axis('off')
        end_umap_time = datetime.now()
        print("End UMAP", end_umap_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
        print("UMAP duration", end_umap_time - start_umap_time)
        print()

    if pca or tsne or compute_umap:
        fig.suptitle(plot_title, fontsize="xx-large",
                     fontweight="extra bold", color="blue")

    plt.tight_layout()

    if save_plots:
        fig.savefig(plot_file)

    plt.show()
