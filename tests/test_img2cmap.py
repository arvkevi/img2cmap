from pathlib import Path

import pytest

from img2cmap import ImageConverter

THIS_DIR = Path(__file__).parent


class Test_Imageconverter_local:
    @pytest.fixture()
    def imageconverter(self):
        return ImageConverter(THIS_DIR.joinpath("images/south_beach_sunset.jpg"))

    def test_generate_cmap_1(self, imageconverter):
        cmap = imageconverter.generate_cmap(4, "miami", 42)
        assert cmap.name == "miami"

    def test_generate_cmap_2(self, imageconverter):
        cmap = imageconverter.generate_cmap(4, "miami", 42)
        assert cmap.N == 4

    def test_generate_cmap_3(self, imageconverter):
        cmap = imageconverter.generate_cmap(4, None, 42)
        assert cmap.name == "south_beach_sunset"

    def test_generate_cmap_4(self, imageconverter):
        with pytest.raises(ValueError):
            imageconverter.generate_cmap(-100, "miami", 42)


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
