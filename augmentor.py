# simple augmentation of a dataset
# author: gugs

import os
import argparse
import cv2

def load_filepaths(directory):
    '''
    grab filepaths of all files in input directory
    param: directory - path to input directory
    Gagan's favorite method.
    '''
    return([os.path.join(directory, filename) for filename in os.listdir(directory)])

def augment_image(image, flip=True):
    '''
    Augment image. 4x rotations. Flip. 4x Rotations. Return.
    param: image - input 2d array image
    param: flip - Flip image and rotate 4x more times. Default True. 
    return: [norm_rotations, flip_rotations] where *_rotations is image list (img_0, img_90, img_180, img_270)
    '''
    norm_rotations = create_rotations(image)
    flip = cv2.flip(image, 1) # 1 = leftright flip
    flip_rotations = create_rotations(flip)
    return [norm_rotations, flip_rotations]

def create_rotations(image):
    '''
    rotates image clockwise 3 times and returns all permutations
    param: image
    return: (img_0, img_90, img_180, img_270)
    '''
    img_0 = image
    img_90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    img_180 = cv2.rotate(image, cv2.ROTATE_180)
    img_270 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return (img_0, img_90, img_180, img_270)

def augment_images(image_paths, output_dir, legal_size=(1024, 1024, 3), flip=True):
    '''
    Loads all images, performs augentations, then saves them in output directory.
    param: image_paths - list of all image full paths
    param: output_dir - path to output dir
    param: legal_size - size of image to augment (useful if wrong sized images in input directory)
    param: flip - Flip image and rotate 4x more times. Default True. 
    '''
    for fullpath in image_paths:
        filename = os.path.basename(fullpath)
        image = cv2.imread(fullpath)
        if (image.shape != legal_size):
            print(f'skipping: {filename}, wrong size: {image.shape}')
            continue
        print(f'Augmenting: {filename}')
        augs = augment_image(image, flip)
        cv2.imwrite(os.path.join(output_dir, f'{filename}_0'), augs[0][0])
        cv2.imwrite(os.path.join(output_dir, f'{filename}_90'), augs[0][1])
        cv2.imwrite(os.path.join(output_dir, f'{filename}_180'), augs[0][2])
        cv2.imwrite(os.path.join(output_dir, f'{filename}_270'), augs[0][3])
        cv2.imwrite(os.path.join(output_dir, f'{filename}_flip_0'), augs[1][0])
        cv2.imwrite(os.path.join(output_dir, f'{filename}_flip_90'), augs[1][1])
        cv2.imwrite(os.path.join(output_dir, f'{filename}_flip_180'), augs[1][2])
        cv2.imwrite(os.path.join(output_dir, f'{filename}_flip_270'), augs[1][3])

def execute_cmdline():
    parser = argparse.ArgumentParser(
        prog = 'Image Dataset Auto Augmentor',
        description='Increase dataset size by 8x. Perform 4x rotations, flip image, then 4x more rotations.',
        epilog= 'Source Code: https://github.com/gagandaroach/python_image_prep'
    )
    parser.add_argument('--input','-i', help='Path to input dataset directory.', required=True)
    parser.add_argument('--output','-o', help='Path to augmented dataset dump directory.', required=True)
    parser.add_argument('--ext', help='File extension of input images. (currently ignored)', default='.png')
    parser.add_argument('--size', help='Size of valid image to import.', default=(1024,1024,3))
    parser.add_argument('--flip', help='Flip images and perform 4x more augmentations', default=True)
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    legal_shape = args.size
    flip = args.flip
    image_paths = load_filepaths(input_dir)
    augment_images(image_paths, output_dir, legal_shape, flip)

if __name__ == "__main__":
    execute_cmdline()
