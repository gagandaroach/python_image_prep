import pyvips
import os.path 
if __name__ == '__main__':
    print('hi')
    path = 'prostate_he_raw/247_12.tif'
    print(f'path: {(path)}')
    print(f'exists? {os.path.exists(path)}')
    img = pyvips.Image.tiffload(path)
    print('img dump: ', img)

    for x in img.get_fields():
        print('attribute: ', x, img.get(x))

    # tiles.pngsave('test_out/247.12.png')
    # note: above was maybe a succes dec 26. took 21g tiff and made 62g png. did not open png to check
