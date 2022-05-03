import os
from pathlib import Path

import pytest

from img2cmap import ImageConverter

THIS_DIR = Path(__file__).parent


class Test_Imageconverter_local:
    @pytest.fixture()
    def get_images(self):

        return os.listdir(THIS_DIR.joinpath("images"))

    @pytest.fixture()
    def image_converters(self, get_images):

        return [ImageConverter(THIS_DIR.joinpath(f"images/{i}")) for i in get_images]

    def test_generate_cmap_1(self, image_converters, get_images):

        for imageconverter in image_converters:
            cmap = imageconverter.generate_cmap(4, "miami", 42)
            assert cmap.name == "miami"

    def test_generate_cmap_2(self, image_converters):
        for imageconverter in image_converters:
            cmap = imageconverter.generate_cmap(4, "miami", 42)
            assert cmap.N == 4

    def test_generate_cmap_3(self, image_converters, get_images):
        cmap_default_names = [i[:-4] for i in get_images]
        for count, imageconverter in enumerate(image_converters):
            cmap = imageconverter.generate_cmap(4, None, 42)
            assert cmap.name == cmap_default_names[count]

    def test_generate_cmap_4(self, image_converters):
        with pytest.raises(ValueError):
            for imageconverter in image_converters:
                imageconverter.generate_cmap(-100, "miami", 42)

    def test_cmap_color_dimension(self, image_converters):
        for imageconverter in image_converters:
            cmap = imageconverter.generate_cmap(4, "Miami Yeaaaa", 42)
            assert cmap.colors.shape[1] == 3


# class Test_Imageconverter_url:
#     @pytest.fixture()
#     def imageconverter(self):
#         return ImageConverter("data/test_img2cmap.png")

#     def test_generate_cmap_1(self, imageconverter):
#         cmap = imageconverter.generate_palette(4, "", 42)

#     def test_generate_cmap_2(self, imageconverter):
#         imageconverter.generate_palette(4, "", 42)

#     def test_generate_cmap_3(self, imageconverter):
#         imageconverter.generate_palette(-100, "1.0.0", 42)
