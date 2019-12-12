# simple augmentation of a dataset
# author: gugs

import os
import argparse
import cv2

def load_filepaths(directory):
    return([os.path.join(directory, filename) for filename in os.listdir(directory)])

def perform_autmentations(image):
    norm_rotations = create_rotations(image)
    flip = cv2.flip(image, 1) # 1 = leftright flip
    flip_rotations = create_rotations(flip)
    return [norm_rotations, flip_rotations]

def create_rotations(image):
    img_0 = image
    img_90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    img_180 = cv2.rotate(image, cv2.ROTATE_180)
    img_270 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return (img_0, img_90, img_180, img_270)

def flip_all_images(image_paths, output_dir, legal_size=(1024, 1024, 3)):
    for fullpath in image_paths:
        filename = os.path.basename(fullpath)
        image = cv2.imread(fullpath)
        if (image.shape != legal_size):
            print(f'skipping: {filename}, wrong size: {image.shape}')
            continue
        print(f'woring on: {filename}')
        augs = perform_autmentations(image)
        cv2.imwrite(os.path.join(output_dir, '0_',filename), augs[0][0])
        # cv2.imshow('hi', augs[0][3])
        # cv2.waitKey(0)
        print(os.path.join(output_dir, '90_',filename))
        cv2.imwrite(os.path.join(output_dir, f'90_{filename}'), augs[0][1])
        cv2.imwrite(os.path.join(output_dir, f'180_{filename}'), augs[0][2])
        cv2.imwrite(os.path.join(output_dir, f'270_{filename}'), augs[0][3])
        cv2.imwrite(os.path.join(output_dir, f'flip_0_{filename}'), augs[1][0])
        cv2.imwrite(os.path.join(output_dir, f'flip_90_{filename}'), augs[1][1])
        cv2.imwrite(os.path.join(output_dir, f'flip_180_{filename}'), augs[1][2])
        cv2.imwrite(os.path.join(output_dir, f'flip_270_{filename}'), augs[1][3])

def execute_cmdline():
    parser = argparse.ArgumentParser(
        prog = 'Image Dataset Auto Augmentor',
        description='Increase dataset size by 8x. Perform 4x rotations, flip image, then 4x more rotations.',
        epilog= 'Source Code: https://github.com/gagandaroach/python_image_prep'
    )
    parser.add_argument('--input','-i', help='Path to input dataset directory.', required=True)
    parser.add_argument('--output','-o', help='Path to augmented dataset dump directory.', required=True)
    parser.add_argument('--ext', help='File extension of input images.', default='.png')
    parser.add_argument('--size', help='Size of valid image to import.', default=(1024,1024,3))
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    legal_shape = args.size
    image_paths = load_filepaths(input_dir)
    flip_all_images(image_paths, output_dir, legal_shape)

if __name__ == "__main__":
    execute_cmdline()
