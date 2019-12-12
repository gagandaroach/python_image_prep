# python_image_prep

Collection of python data processing ETL tools and jupyter notebooks I use to prepare image data for neural network training and research.

## augmentor.py

This will take an input directory of images and augment them into a dataset 8x larger (in image count).

```bash
usage: Image Dataset Auto Augmentor [-h] --input INPUT --output OUTPUT
                                    [--ext EXT] [--size SIZE] [--flip FLIP]

Increase dataset size by 8x. Perform 4x rotations, flip image, then 4x more
rotations.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Path to input dataset directory.
  --output OUTPUT, -o OUTPUT
                        Path to augmented dataset dump directory.
  --ext EXT             File extension of input images. (currently ignored)
  --size SIZE           Size of valid image to import.
  --flip FLIP           Flip images (left-right) and perform 4x more
                        augmentations

```
## research folder

this is where I experiment with python and image data preprocessing 

### clustering filter

I created this project to create tiles from Whole Slide Images. I use K-Means clustering on a downsampled version of a input TIFF to create 1024x1024 png tiles. See `WSI AutoTiler.ipynb` for the code.

### histogram filter

deprecated project. I was trying to classify WSI image tiles as good or bad. Good means the tile is of tissue. Bad means the tile is of background nonsense. This filter was aimed to work on images after already tiling the whole slide image.

I found approaching this approach not robust enough. After these experiments I switched to using the clustering filter above.

There is more data available in the complete whole slide image then the tiles.