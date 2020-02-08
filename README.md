# python_image_prep

Collection of python data processing ETL tools and jupyter notebooks I use to prepare image data for neural network training and research.

> Gagan Daroach <gagandaroach@gmail.com>
> github.com/gagandaroach/python_image_prep

## tile_nucleoid_classifier.py

This program is used to solve data cleaning problems with whole slide images. When slicing a large WSI into many tiles, lazy algorithms will include white backgrounds tiles from the edges of the WSI in addition to the tiles covering tissue samples in the center.

This script will take an input directory of H&E stained tiles, and output the tiles into groups based on the number of nucleoids in each tile.

Thanks to the HistomicsTK python team for an open source nucleoid classifier algorithem.

**Input**

H&E stained tissue samples. Can apply different color stainings by updating color threshold map in script. Any skimage compatible image type.

**Output**

In output folder, default config is to bin tiles into 4 groupings. 

 * 0 nucleoids
 * 1-20 nucleoids
 * 21-100 nucleoids
 * 100+ nucleoids

**Example Usage**

```bash
$ python tile_nucleoid_classifier.py -i /research/input_image_dir -o /research/output_image_dir
```
From tiling 20 WSI prostate images, 130k 1024x1024 png tiles were generated. This script was then used to clean that dataset. Yielded 87k tiles with 100+ nucleoids. Good for GAN training.

## augmentor.py

This will take an input directory of images and augment them into a dataset 8x larger (in image count).

**Example Usage**

```bash
$ python augmentor.py -i /research/input_image_dir -o /research/output_image_dir
```

**Program Command Line Arguments**
|Argument|Description|Default|
|---|---|---|
|`-h, --help` |show help message and exit|n/a|
|`--input,-i INPUT`|Path to input dataset directory.|required|
|`--output,-o OUTPUT` |Path to augmented dataset dump directory.|required|
|`--ext EXT` |File extension of input images.|.png|
|`--size SIZE` |Size of valid image to import.|(1024,1024,3)|
|`--flip FLIP` |Flip images (left-right) and perform 4x more augmentations|True

## Research Folder

this is where I experiment with python and image data preprocessing

### Clustering Filter

I created this project to create tiles from Whole Slide Images. I use K-Means clustering on a downsampled version of a input TIFF to create 1024x1024 png tiles. See `WSI AutoTiler.ipynb` for the code.

### Histogram Filter

deprecated project. I was trying to classify WSI image tiles as good or bad. Good means the tile is of tissue. Bad means the tile is of background nonsense. This filter was aimed to work on images after already tiling the whole slide image.

I found approaching this approach not robust enough. After these experiments I switched to using the clustering filter above.

There is more data available in the complete whole slide image then the tiles.
