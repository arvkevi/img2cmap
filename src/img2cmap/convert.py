from pathlib import Path
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen

import matplotlib as mpl
import numpy as np
from PIL import Image
from sklearn.cluster import MiniBatchKMeans


class ImageConverter:
    """Converts an image to numpy array of RGB values.

    Args:
        image_path str: The path to the image. Can be a local file or a URL.

    Attributes:
        image_path (str): The path to the image. Can be a local file or a URL.
        image (PIL.Image): The image object.
        pixels (numpy.ndarray): A numpy array of RGB values.
    """

    def __init__(self, image_path):
        self.image_path = image_path
        # try to open the image
        try:
            self.image = Image.open(self.image_path)
        except FileNotFoundError as fnf_error:
            try:
                self.image = Image.open(urlopen(self.image_path))
            except (URLError, HTTPError) as url_error:
                raise URLError(f"Could not open {self.image_path} {url_error}") from url_error

            raise FileNotFoundError(f"File {self.image_path} not found {fnf_error}") from fnf_error

        # convert the image to a numpy array
        self.pixels = np.array(self.image.getdata())

    def generate_cmap(self, n_colors=4, palette_name=None, random_state=None):
        """Generates a matplotlib ListedColormap from an image.

        Args:
            n_colors (int, optional): The number of colors in the ListedColormap. Defaults to 4.
            palette_name (str, optional): A name for your created palette. If None, defaults to the image name.
                Defaults to None.
            random_state (int, optional): A random seed for reproducing ListedColormaps.
                The k-means algorithm has a random initialization step and doesn't always converge on the same
                solution because of this. If None will be a different seed each time this method is called.
                Defaults to None.

        Returns:
            matplotlib.colors.ListedColormap: A matplotlib ListedColormap object.
        """
        # create a kmeans model
        kmeans = MiniBatchKMeans(n_clusters=n_colors, random_state=random_state)
        # fit the model to the pixels
        kmeans.fit(self.pixels)
        # get the cluster centers
        centroids = kmeans.cluster_centers_ / 255
        # return the palette
        if palette_name is None:
            palette_name = Path(self.image_path).stem
        cmap = mpl.colors.ListedColormap(centroids, name=palette_name)

        return cmap
