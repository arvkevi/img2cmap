from pathlib import Path

import numpy as np
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


@pytest.mark.parametrize("test_image_input", images)
def test_cmap_optimal_plot(test_image_input):
    imageconverter = ImageConverter(test_image_input)
    cmaps, _, _ = imageconverter.generate_optimal_cmap(random_state=42)
    for _, cmap_ in cmaps.items():

        assert not np.any(np.all(np.isclose(cmap_.colors, 1, atol=1e-9)))
        assert not np.any(np.all(np.isclose(cmap_.colors, 0, atol=1e-9)))


# TODO: Mock these!
# def test_url():
#     with open(THIS_DIR.joinpath("urls/nba-logos.txt"), "r") as f:
#         for line in f:
#             if "miami" in line:
#                 url = line.strip()
#                 break
#     converter = ImageConverter(url)
#     cmap = converter.generate_cmap(2, "miami", 42)
#     assert cmap.name == "miami"


# @pytest.mark.parametrize("test_remove_transparent", [True, False])
# def test_remove_transparent(test_remove_transparent):
#     """This image should not have any black pixels."""
#     with open(THIS_DIR.joinpath("urls/nba-logos.txt"), "r") as f:
#         for line in f:
#             if "atlanta" in line:
#                 url = line.strip()
#     converter = ImageConverter(url, remove_transparent=test_remove_transparent)
#     cmap = converter.generate_cmap(3, 42)
#     hex_codes = [mpl.colors.rgb2hex(c) for c in cmap.colors]
#     black_not_in_colors = not any(["#000000" in c for c in hex_codes])
#     assert black_not_in_colors == test_remove_transparent


def test_generate_optimal():
    imageconverter = ImageConverter(THIS_DIR.joinpath("images/south_beach_sunset.jpg"))
    _, best_n_colors, _ = imageconverter.generate_optimal_cmap(random_state=42)
    assert best_n_colors == 5


def test_resize():
    imageconverter = ImageConverter(THIS_DIR.joinpath("images/south_beach_sunset.jpg"))
    imageconverter.resize(size=(512, 512))
    # thumbnail preserves the aspect ratio
    assert imageconverter.image.size == (512, 361)
