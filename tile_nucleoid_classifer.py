# Tile Nucleoid Classifier
#
# Author: Gagan <gagandaroach@gmail.com>
# Date: Sat 2020-02-01

import os
from os import system
import math
import time
import argparse
import histomicstk as htk
import numpy as np
import scipy as sp
import skimage.io
import skimage.measure
import skimage.color

stainColorMap = {
    'hematoxylin': [0.65, 0.70, 0.29],
    'eosin':       [0.07, 0.99, 0.11],
    'dab':         [0.27, 0.57, 0.78],
    'null':        [0.0, 0.0, 0.0]
}

output_dirs = ['0','1-10','11-100','100+']

def load_img_filenames(directory):
    '''
    input: (string) dir to call
    return: (array[string], string) dir+path, tile_name (no ext)
    '''
    names = []
    print(f'fetching filenames from {directory}')
    start_time = time.time()
    count = 0
    for filename in os.listdir(directory):
        names.append(filename)
    load_time = time.time() - start_time
    print(f'fetched {len(names)} filenames in {load_time} seconds.')

    full_paths = []
    for name in names:
        img_path = os.path.join(directory, name)
        full_paths.append((img_path, os.path.splitext(name)[0]))
    return full_paths

def load_img(img_path):
    '''
    input: (string) img path
    return: (array[string]) dir+path
    '''
    start_time = time.time()
    img = skimage.io.imread(img_path)[:, :, :3]
    run_time = time.time() - start_time
    print(f'loaded img in {run_time} sec')
    return img

def calculate_nucleiod_count(he_img):
    '''
    input: (skimage) he image
    output: nucleoid_count
    '''
    # specify stains of input image
    stain_1 = 'hematoxylin'   # nuclei stain
    stain_2 = 'eosin'         # cytoplasm stain
    stain_3 = 'null'          # set to null of input contains only two stains

    # create stain matrix
    W = np.array([stainColorMap[stain_1],
                  stainColorMap[stain_2],
                  stainColorMap[stain_3]]).T

    # perform standard color deconvolution
    im_stains = htk.preprocessing.color_deconvolution.color_deconvolution(he_img, W).Stains
    
    # get nuclei/hematoxylin channel
    im_nuclei_stain = im_stains[:, :, 0]

    # segment foreground
    foreground_threshold = 60

    im_fgnd_mask = sp.ndimage.morphology.binary_fill_holes(
        im_nuclei_stain < foreground_threshold)

    # run adaptive multi-scale LoG filter
    min_radius = 10
    max_radius = 15

    im_log_max, im_sigma_max = htk.filters.shape.cdog(
        im_nuclei_stain, im_fgnd_mask,
        sigma_min=min_radius * np.sqrt(2),
        sigma_max=max_radius * np.sqrt(2)
    )

    # detect and segment nuclei using local maximum clustering
    local_max_search_radius = 10

    im_nuclei_seg_mask, seeds, maxima = htk.segmentation.nuclear.max_clustering(
        im_log_max, im_fgnd_mask, local_max_search_radius)

    # filter out small objects
    min_nucleus_area = 80

    im_nuclei_seg_mask = htk.segmentation.label.area_open(
        im_nuclei_seg_mask, min_nucleus_area).astype(np.int)

    # compute nuclei properties
    objProps = skimage.measure.regionprops(im_nuclei_seg_mask)
    return len(objProps)

def init_output_dir(output_dir):
    print('initializing output directory')
    for folder in output_dirs:
        path = os.path.join(output_dir, folder)
        if not os.path.isdir(path):
            os.mkdir(path, 493 )
    print('done.')

def save_tile_by_count(img, name, count, output_dir):
    save_dir = None
    if count >= 100:
        save_dir = os.path.join(output_dir, output_dirs[3])
    elif count >= 11:
        save_dir = os.path.join(output_dir, output_dirs[2])
    elif count>=1:
        save_dir = os.path.join(output_dir, output_dirs[1])
    else:
        save_dir = os.path.join(output_dir, output_dirs[0])
    save_path = os.path.join(save_dir, f'{name}_nuc{count}.png')
    skimage.io.imsave(save_path, img)

def main(tiles_dir, output_dir, single):
    print('starting program!')
    if single:
        print('executing on single file')
        name = os.path.basename(tiles_dir)
        name = os.path.splitext(name)[0]
        img = load_img(tiles_dir)
        count, calc_time = count_tile_nucleoids(img)
        print(f'count: {count} | {calc_time} sec')
        save_tile_by_count(img, name, count, output_dir)
    else:
        img_paths = load_img_filenames(tiles_dir)
        for index, (path, name) in enumerate(img_paths):
            img = load_img(path)
            count, calc_time = count_tile_nucleoids(img)
            save_tile_by_count(img, name, count, output_dir)
            print(f'{index} | count: {count} | {calc_time} sec')
    print ('ending program')

def count_tile_nucleoids(img):
        start_time = time.time()
        count = calculate_nucleiod_count(img)
        calc_time = time.time() - start_time
        return count, calc_time

def execute_cmdline():
    parser = argparse.ArgumentParser(
        prog = 'Histology Tile - Nucleoid Classifier',
        description='Classify WSI as good or bad depending on Nucleoid Count. Uses HistomicsTK library.',
        epilog= 'Source Code: https://github.com/gagandaroach/python_image_prep'
    )
    parser.add_argument('--input','-i', help='WSI H&E Histology tiles directory.', required=True)
    parser.add_argument('--output','-o', help='Path to dump classified tiles.', required=True)
    parser.add_argument('--single','-s', help='Boolean flag if input is single image, not directory. Default False', default=False)
    args = parser.parse_args()
    input_dir = args.input
    output_dir = args.output
    single = args.single
    init_output_dir(output_dir)
    main(input_dir,output_dir, single)

if __name__ == "__main__":
    execute_cmdline()