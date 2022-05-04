from pathlib import Path

import pytest

from img2cmap import ImageConverter

THIS_DIR = Path(__file__).parent

images = list(THIS_DIR.joinpath("images").iterdir())


@pytest.mark.parametrize("test_image_input", images)
def test_generate_cmap_1(test_image_input):
    imageconverter = ImageConverter(test_image_input)
    cmap = imageconverter.generate_cmap(4, "miami", 42)
    assert cmap.name == "miami"


@pytest.mark.parametrize("test_image_input", images)
def test_generate_cmap_2(test_image_input):
    imageconverter = ImageConverter(test_image_input)
    cmap = imageconverter.generate_cmap(4, "miami", 42)
    assert cmap.N == 4


@pytest.mark.parametrize("test_image_input", images)
def test_generate_cmap_3(test_image_input):
    cmap_default_name = test_image_input.stem
    imageconverter = ImageConverter(test_image_input)
    cmap = imageconverter.generate_cmap(4, None, 42)
    assert cmap.name == cmap_default_name


@pytest.mark.parametrize("test_image_input", images)
def test_generate_cmap_4(test_image_input):
    with pytest.raises(ValueError):
        imageconverter = ImageConverter(test_image_input)
        imageconverter.generate_cmap(-100, "miami", 42)


@pytest.mark.parametrize("test_image_input", images)
def test_cmap_color_dimension(test_image_input):
    imageconverter = ImageConverter(test_image_input)
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
