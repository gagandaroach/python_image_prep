# python_image_prep
Collection of jupyter notebooks I use to prepare image data for neural network training. 

## clustering filter

I created this project to create tiles from Whole Slide Images. I use K-Means clustering on a downsampled version of a input TIFF to create 1024x1024 png tiles. See `WSI AutoTiler.ipynb` for the code.

## augmentor.py

This will take an input directory of images and augment them into 8x larger size.

Saving 4 rotations of an image, flipping, and then saving 4 rotations of the flipped image.