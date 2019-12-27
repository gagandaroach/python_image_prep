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
    tiff_name = os.path.basename(image_path)
    tiff_name = os.path.splitext(tiff_name)[0]

    width = img.width
    height = img.height
    tile_w = 1024
    tile_h = 1024
    
    start_x = 0
    start_y = 0

    debug_count = 0

    for y in range(start_x,height-tile_h,tile_h):
        for x in range(start_y,width-tile_w,tile_w):
            print(f'creating tile: {debug_count}')
            #if (debug_count > 10):
            #    return tiles
            tile = img.extract_area(x,y,tile_w,tile_h)
            save_tile(tiff_name, tile, x, y, output_dir)
            debug_count = debug_count + 1

def save_tile(tile_name, tile, xpos, ypos, output_dir):
    filename = f'{tile_name}_{xpos}_{ypos}.png'
    save_path = os.path.join(output_dir, filename)
    tile.pngsave(save_path)
    print(f'saved tile: {filename}')

if __name__ == '__main__':
        
    input_dir = '/srv/data/mcw_research/prostate_he_raw/'
    output_dir = '/srv/data/mcw_research/prostate_he_tiles/'

    print(f'input dir: {input_dir}')
    print(f'output dir: {output_dir}')

    filenames = load_all_img_paths(input_dir)
    #print(filenames)

    create_tiles_with_vips(filenames[0])

    print('done with script. file in output dir')
    
    

