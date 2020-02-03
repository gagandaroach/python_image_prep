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

def load_img_filenames(directory):
    '''
    input: (string) dir to call
    return: (array[string]) dir+path
    '''
    # names = []
    # print(f'fetching filenames from {directory}')
    # start_time = time.time()
    # count = 0
    # load_limit = 10
    # for filename in os.listdir(directory):
    #     names.append(filename)
    #     count = count + 1
    #     if count == load_limit
    #         break
    # load_time = time.time() - start_time
    # print(f'fetched {len(names)} filenames in {load_time} seconds.')
    names = ["247_12_x0.5__18432_63488.png", "247_12_x0.5__18432_64512.png", "247_12_x0.5__18432_65536.png", "247_12_x0.5__18432_66560.png", "247_12_x0.5__18432_67584.png", "247_12_x0.5__18432_68608.png", "247_12_x0.5__18432_69632.png", "247_12_x0.5__18432_70656.png", "247_12_x0.5__18432_7168.png", "247_12_x0.5__18432_71680.png", "247_12_x0.5__18432_72704.png", "247_12_x0.5__18432_73728.png", "247_12_x0.5__18432_74752.png", "247_12_x0.5__18432_75776.png", "247_12_x0.5__18432_76800.png", "247_12_x0.5__18432_77824.png", "247_12_x0.5__18432_78848.png", "247_12_x0.5__18432_79872.png", "247_12_x0.5__18432_80896.png", "247_12_x0.5__18432_8192.png", "247_12_x0.5__18432_81920.png", "247_12_x0.5__18432_82944.png", "247_12_x0.5__18432_83968.png", "247_12_x0.5__18432_84992.png", "247_12_x0.5__18432_86016.png", "247_12_x0.5__18432_87040.png", "247_12_x0.5__18432_88064.png", "247_12_x0.5__18432_89088.png", "247_12_x0.5__18432_90112.png", "247_12_x0.5__18432_91136.png", "247_12_x0.5__18432_9216.png", "247_12_x0.5__18432_92160.png", "247_12_x0.5__18432_93184.png"]
    full_paths = []
    for name in names:
        img_path = os.path.join(directory, name)
        full_paths.append(img_path)
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
    output_dirs = ['0','1-20','21-100','100+']
    for folder in output_dirs:
        path = os.path.join(output_dir, folder)
        os.mkdir(path, 493 )
    print('done.')

def classify_tiles(tiles_dir, output_dir):
    print('starting program!')
    img_paths = load_img_filenames(tiles_dir)
    for index, path in enumerate(img_paths):
        img = load_img(path)
        start_time = time.time()
        count = calculate_nucleiod_count(img)
        calc_time = time.time() - start_time
        print(f'{index} | count: {count} | {calc_time} sec')
    print ('ending program')

def execute_cmdline():
    parser = argparse.ArgumentParser(
        prog = 'Tile Nucleoid Classifier',
        description='Classify WSI as good or bad depending on Nucleoid Count. Uses HistomicsTK library.',
        epilog= 'Source Code: https://github.com/gagandaroach/python_image_prep'
    )
    parser.add_argument('--input','-i', help='WSI H&E Histology tiles directory.', required=True)
    parser.add_argument('--output','-o', help='Path to dump classified tiles.', required=True)
    args = parser.parse_args()
    input_dir = args.input
    output_dir = args.output
    init_output_dir(output_dir)
    classify_tiles(input_dir,output_dir)

if __name__ == "__main__":
    execute_cmdline()