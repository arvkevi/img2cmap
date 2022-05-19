import colorsys
from pathlib import Path
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen

import matplotlib as mpl
import numpy as np
from kneed import KneeLocator
from PIL import Image
from sklearn.cluster import MiniBatchKMeans


class ImageConverter:
    """Converts an image to numpy array of RGB values.

    Args:
        image_path str: The path to the image. Can be a local file or a URL.
        remove_transparent bool: If True, will not consider any transparent pixels. Defaults to False.

    Attributes:
        image_path (str): The path to the image. Can be a local file or a URL.
        image (PIL.Image): The image object.
        pixels (numpy.ndarray): A numpy array of RGB values.
    """

    def __init__(self, image_path, remove_transparent=False):
        self.image_path = image_path
        # try to open the image
        try:
            self.image = Image.open(self.image_path)
        except FileNotFoundError:
            try:
                self.image = Image.open(urlopen(self.image_path))
            except (URLError, HTTPError, FileNotFoundError) as error:
                raise URLError(f"Could not open {self.image_path} {error}") from error

        # convert the image to a numpy array
        self.image = self.image.convert("RGBA")
        self.pixels = np.array(self.image.getdata())
        if remove_transparent:
            self.pixels = self.pixels[self.pixels[:, 3] != 0]
        self.pixels = self.pixels[:, :3]
        self.kmeans = None

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
        self.kmeans = MiniBatchKMeans(n_clusters=n_colors, random_state=random_state)
        # fit the model to the pixels
        self.kmeans.fit(self.pixels)
        # get the cluster centers
        centroids = self.kmeans.cluster_centers_ / 255
        # return the palette
        if palette_name is None:
            palette_name = Path(self.image_path).stem

        cmap = mpl.colors.ListedColormap(centroids, name=palette_name)

        # Handle 4 dimension RGBA colors
        cmap.colors = cmap.colors[:, :3]

        # Sort colors by hue
        cmap.colors = sorted(cmap.colors, key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
        # Handle cases where all rgb values evaluate to 1 or 0. This is a temporary fix
        cmap.colors = np.where(np.isclose(cmap.colors, 1), 1 - 1e-6, cmap.colors)
        cmap.colors = np.where(np.isclose(cmap.colors, 0), 1e-6, cmap.colors)

        return cmap

    def generate_optimal_cmap(self, max_colors=10, palette_name=None, random_state=None):
        """Generates an optimal matplotlib ListedColormap from an image by finding the optimal number of clusters using the elbow method.

        Useage:
            >>> img = ImageConverter("path/to/image.png")
            >>> cmaps, best_n_colors, ssd = img.generate_optimal_cmap()
            >>> # The optimal colormap
            >>> cmaps[best_n_colors]


        Args:
            max_colors (int, optional): _description_. Defaults to 10.
            palette_name (_type_, optional): _description_. Defaults to None.
            random_state (_type_, optional): _description_. Defaults to None.
            remove_background (_type_, optional): _description_. Defaults to None.

        Returns:
            dict: A dictionary of matplotlib ListedColormap objects.
            Keys are the number of colors (clusters). Values are ListedColormap objects.
            int: The optimal number of colors.
            dict: A dictionary of the sum of square distances from each point to the cluster center.
            Keys are the number of colors (clusters) and values are the SSD value.
        """
        ssd = dict()
        cmaps = dict()
        for n_colors in range(2, max_colors + 1):
            cmap = self.generate_cmap(n_colors=n_colors, palette_name=palette_name, random_state=random_state)
            cmaps[n_colors] = cmap
            ssd[n_colors] = self.kmeans.inertia_

        best_n_colors = KneeLocator(list(ssd.keys()), list(ssd.values()), curve="convex", direction="decreasing").knee

        return cmaps, best_n_colors, ssd

    def resize(self, size=(512, 512)):
        """Resizes the image to the specified size.

        Args:
            size (tuple): The new size of the image.

        Returns:
            None
        """
        try:
            resampling_technique = Image.Resampling.LANCZOS
        # py36
        except AttributeError:
            resampling_technique = Image.LANCZOS

        self.image.thumbnail(size, resampling_technique)
