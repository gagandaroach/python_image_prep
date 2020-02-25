import argparse
import pyvips
import os.path
import re
from datetime import datetime


def load_all_img_paths(dir_to_search, valid_ext):
    filepaths = []
    for subdir, dirs, files in os.walk(dir_to_search):
        for filename in files:
            if is_wsi(filename, valid_ext):
                filepath = os.path.join(subdir, filename)
                filepaths.append(filepath)
    return filepaths


def is_wsi(img_path, valid_ext):
    '''
    valid_ext: tif (note no dot)
    Checks if filename is like 145_12.tif.
    '''
    filename = os.path.basename(img_path)
    wsi_tiff_regex = f'\\d+_\\d+.{valid_ext}'
    x = re.search(wsi_tiff_regex, filename)
    if x is None:
        return False
    if filename.startswith('._'):
        return False
    return True


def create_tiles_with_vips(image_path, scale_factor, output_dir, t_size, count):
    print(f'creating tiles with image: {image_path}')
    img = pyvips.Image.tiffload(image_path)
    print(img)
    tiff_name = os.path.basename(image_path)
    tiff_name = os.path.splitext(tiff_name)[0]

    img = img.resize(scale_factor)

    width = img.width
    height = img.height

    tile_w = t_size[0]
    tile_h = t_size[1]

    start_x = 0
    start_y = 0

    debug_count = 0

    for y in range(start_x, height-tile_h, tile_h):
        for x in range(start_y, width-tile_w, tile_w):
            print(f'creating tile: {debug_count}')
            if (count != 0 and debug_count > count):
                return
            tile = img.extract_area(x, y, tile_w, tile_h)
            save_tile(tiff_name, tile, x, y, output_dir, scale_factor)
            debug_count = debug_count + 1


def save_tile(tile_name, tile, xpos, ypos, output_dir, scale_factor):
    filename = f'{tile_name}_x{scale_factor}_{xpos}_{ypos}.png'
    save_path = os.path.join(output_dir, filename)
    tile.pngsave(save_path)
    print(f'saved tile: {filename}')


def execute_cmdline():
    parser = argparse.ArgumentParser(
        prog='PYVIPS WSI to Tiles',
        description='Able to tile large 20GB+ whoel slide images into square tiles.',
        epilog='Source Code: https://github.com/gagandaroach/python_image_prep'
    )
    parser.add_argument(
        '--input', '-i', help='Path to input dataset directory. If input dir is file, then process just that file.', required=True)
    parser.add_argument(
        '--output', '-o', help='Directory to dump image tiles.', required=True)
    parser.add_argument(
        '--ext', help='File extension of input images.', default='.tif')
    parser.add_argument(
        '--scale', help='How much to resize the WSI (0.5x resize is 2x zoom)', default='0.5')
    parser.add_argument(
        '--count', help='Limit of tiles to create before quitting. (Useful for testing) If 0, process whole WSI.', default='0')
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output
    valid_ext = args.ext
    scale = args.scale
    count = args.count
    t_size = (1024, 1024)

    print(f'input dir: {input_dir}')
    print(f'output dir: {output_dir}')

    filenames = []
    if (os.path.isfile(input_dir)):
        print('processing a single image file.')
        filenames.append(input_dir)
    else:
        filenames = load_all_img_paths(input_dir, valid_ext)
        print('loaded %d image filenames' % len(filenames))

    for image_filepath in filenames:
        starttime = datetime.now()
        create_tiles_with_vips(image_filepath, scale,
                               output_dir, t_size, count)
        print(f'tiled {image_filepath} in {(datetime.now()-starttime).seconds}')

    print('done with script. file in output dir')


if __name__ == "__main__":
    execute_cmdline()
