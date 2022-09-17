import warnings
from io import BytesIO

import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

import streamlit as st
from annotated_text import annotated_text

from img2cmap import ImageConverter

def colorpicker(color):
    """https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color/3943023#3943023"""
    
    red, green, blue = mpl.colors.to_rgb(color)
    newrgb = []
    for c in red, green, blue:
        c = c / 255.0
        if c <= 0.04045:
            newrgb.append(c/12.92)
        else:
            newrgb.append(((c+0.055)/1.055) ^ 2.4)
    L = 0.2126 * newrgb[0] + 0.7152 * newrgb[1] + 0.0722 * newrgb[2]
    # why did I have to use 179 instead of 0.179?
    if L > 0.179 / 1000:
        return "#000000"
    else:
        return "#ffffff"


# @profile
def main():
    warnings.filterwarnings("ignore")
    st.set_option("deprecation.showfileUploaderEncoding", False)

    st.set_page_config(
        page_title="img2cmap web",
        layout="wide",
    )

    st.title("Convert images to a colormap")
    st.markdown(
        """
        This app converts images to colormaps using the Python
        library [img2cmap](https://github.com/arvkevi/img2cmap).
        Try your own image on the left. **Scroll down to generate an optimal colormap.**
        """
    )

    st.sidebar.markdown("### Image settings")
    file_or_url = st.sidebar.radio("Upload an image file or paste an image URL", ("file", "url"))

    if file_or_url == "file":
        user_image = st.sidebar.file_uploader("Upload an image file")
        if user_image is not None:
            user_image = BytesIO(user_image.getvalue())
    elif file_or_url == "url":
        user_image = st.sidebar.text_input("Paste an image URL", "https://static1.bigstockphoto.com/3/2/3/large1500/323952496.jpg")
    else:
        st.warning("Please select an option")

    # default image to use
    if user_image is None:
        user_image = "https://raw.githubusercontent.com/arvkevi/img2cmap/main/tests/images/south_beach_sunset.jpg"

    # user settings
    st.sidebar.markdown("### User settings")
    n_colors = st.sidebar.number_input(
        "Number of colors", min_value=2, max_value=20, value=5, help="The number of colors to return in the colormap"
    )
    n_colors = int(n_colors)
    remove_transparent = st.sidebar.checkbox(
        "Remove transparency", False, help="If checked, remove transparent pixels from the image before clustering."
    )
    random_state = st.sidebar.number_input("Random state", value=42, help="Random state for reproducibility")
    random_state = int(random_state)

    @st.cache(allow_output_mutation=True)
    def get_image_converter(user_image, remove_transparent):
        converter = ImageConverter(user_image)
        if remove_transparent:
            converter.remove_transparent()
        return converter

    converter = get_image_converter(user_image, remove_transparent)
    converter.resize()

    with st.spinner("Generating colormap..."):
        cmap = converter.generate_cmap(n_colors=n_colors, palette_name="", random_state=random_state)

    # plot the image and colorbar
    fig1, ax1 = plt.subplots(figsize=(8, 8))

    ax1.axis("off")
    img = converter.image
    im = ax1.imshow(img, cmap=cmap)

    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="10%", pad=0.05)

    cb = fig1.colorbar(im, cax=cax, orientation="vertical", label=cmap.name)
    cb.set_ticks([])
    st.pyplot(fig1)

    colors1 = [mpl.colors.rgb2hex(c) for c in cmap.colors]
    
    # determine whether to show the text in white or black
    bw_mask = [colorpicker(c) for c in colors1]

    st.header("Hex Codes")
    annotated_text(*[(hexcode, "", hexcode, text_color) for hexcode, text_color in zip(colors1, bw_mask)])
    st.code(colors1)
    st.caption("Click copy button on far right to copy hex codes to clipboard.")

    st.header("Detect optimal number of colors")
    max_colors = st.number_input("Max number of colors in cmap (more colors = longer runtime)", min_value=2, max_value=20, value=10)
    optimize = st.button("Optimize")
    if optimize:
        with st.spinner("Optimizing... (this can take up to a minute)"):
            cmaps, best_n_colors, ssd = converter.generate_optimal_cmap(max_colors=max_colors, palette_name="", random_state=random_state)

        figopt, ax = plt.subplots(figsize=(7, 5))

        ymax = max_colors + 1
        xmax = max_colors
        ax.set_ylim(2, ymax)
        ax.set_xlim(0, max_colors)

        # i will be y axis
        for y, cmap_ in cmaps.items():
            # Fix small
            colors = sorted([mpl.colors.rgb2hex(c) for c in cmap_.colors])
            intervals, width = np.linspace(0, xmax, len(colors) + 1, retstep=True)
            # j will be x axis
            for j, color in enumerate(colors):
                rect = patches.Rectangle((intervals[j], y), width, 1, facecolor=color)
                ax.add_patch(rect)

        ax.set_yticks(np.arange(2, ymax) + 0.5)
        ax.set_yticklabels(np.arange(2, ymax))
        ax.set_ylabel("Number of colors")
        ax.set_xticks([])

        # best
        rect = patches.Rectangle((0, best_n_colors), ymax, 1, linewidth=1, facecolor="none", edgecolor="black", linestyle="--")
        ax.add_patch(rect)

        # minus 2, one for starting at 2 and one for 0-indexing
        ax.get_yticklabels()[best_n_colors - 2].set_color("red")
        st.pyplot(figopt)
        st.metric("Optimal number of colors", best_n_colors)
        st.text("Hex Codes of optimal colormap (click to copy on far right)")
        st.code(sorted([mpl.colors.rgb2hex(c) for c in cmaps[best_n_colors].colors]))

        st.text("Sum of squared distances by number of colors:")
        st.write(ssd)


if __name__ == "__main__":
    main()
