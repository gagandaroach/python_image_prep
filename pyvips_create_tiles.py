import pyvips
import os.path 
import re

def load_all_img_paths(dir_to_search):
    filepaths = []
    for subdir, dirs, files in os.walk(dir_to_search):
        for file in files:
            if is_wsi(file):
                filepath = os.path.join(subdir, file)
                filepaths.append(filepath)
    return filepaths


def is_wsi(img_path):
    '''
    Checks if filename is like 145_12.tiff.
    '''
    filename = os.path.basename(img_path)
    wsi_tiff_regex = '\d+_\d+.tif'
    x = re.search(wsi_tiff_regex, filename)
    if x is None:
        return False
    if filename.startswith('._'):
        return False
    return True

def create_tiles_with_vips(image_path):
    print(f'creating tiles with image: {image_path}')
    img = pyvips.Image.tiffload(image_path)
    print(img)


if __name__ == '__main__':
        
    input_dir = '/srv/data/mcw_research/prostate_he_raw/'
    output_dir = '/srv/data/mcw_research/prostate_he_tiles/'

    print(f'input dir: {input_dir}')
    print(f'output dir: {output_dir}')

    filenames = load_all_img_paths(input_dir)
    #print(filenames)
    create_tiles_with_vips(filenames[0])


