import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

# define B, G, R wavelength
color_wavelengths = [450, 550, 650]

# define, width, height, bands for nh7
width = 1280
height = 1024
bands = 151

# define list of wavelengths
min_wavelength = 350
max_wavelength = 1100
interval_wavelength = 5

wavelengths_list = list(range(min_wavelength, max_wavelength+1, interval_wavelength))

color_bands = []
color_wavelengths_closest = []
for w in color_wavelengths:
    diff = np.absolute(np.array(wavelengths_list)-w)
    index = diff.argmin()
    color_bands.append(index)
    color_wavelengths_closest.append(wavelengths_list[index])

def ref(fname1, fname2):
    basename = os.path.splitext(os.path.basename(fname2))[0]
    dirname = os.path.dirname(fname2)

    print(f'loading hypespectral file {fname1}')
    with open(fname1, 'rb') as fid:
        data_array = np.fromfile(fid, np.uint16)

        cube = np.zeros((height, width, bands),dtype=np.uint16)
        for k in range(bands):
            print(f'loading band {k}({wavelengths_list[k]}[nm])')
            for j in range(height):
                for i in range(width):
                    index = (i-1)+width*bands*(j)+width*(k)
                    cube[j,i,k] = data_array[index]

        color_image1 = np.zeros((height, width, 3))

        for k in range(3):
            color_image1[:,:,k] = cube[:,:,color_bands[k]]


        color_image1_uint8_by_cv2 = cv2.normalize(color_image1, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        r = cv2.selectROI("select White Diffuse Reflectance Standard", color_image1_uint8_by_cv2) 
        cv2.destroyWindow("select White Diffuse Reflectance Standard")

        # Crop image 
        cropped_cube1 = cube[int(r[1]):int(r[1]+r[3]),  
                            int(r[0]):int(r[0]+r[2]),:] 
        cropped_color_image1 = color_image1_uint8_by_cv2[int(r[1]):int(r[1]+r[3]),  
                            int(r[0]):int(r[0]+r[2])] 

        white_DN = []
        for k in range(bands):
            m = np.mean(cropped_cube1[:,:,k].flatten())
            white_DN.append(m)

    plt.figure()
    plt.plot(wavelengths_list, white_DN)
    plt.xlabel('Wavelength [nm]') 
    plt.ylabel('Digital Number') 
    plt.title('White Diffuse Reflectance Standard') 
    plt.savefig(f'white_DN_{basename}.png')   # save wavelength-DN plot of white diffuse reflectance standard
    # plt.close()

    if fname1 != fname2:
        print(f'loading hypespectral file {fname2}')
        with open(fname2, 'rb') as fid:
            data_array = np.fromfile(fid, np.uint16)

            cube = np.zeros((height, width, bands),dtype=np.uint16)
            for k in range(bands):
                print(f'loading band {k}({wavelengths_list[k]}[nm])')
                for j in range(height):
                    for i in range(width):
                        index = (i-1)+width*bands*(j)+width*(k)
                        cube[j,i,k] = data_array[index]

    print('generating reflectance cube')
    r_cube = np.zeros((height, width, bands), dtype=np.float32)
    for k in range(bands):
        print(f'calculating reflectance at band {k}({wavelengths_list[k]}[nm])')
        for j in range(height):
            for i in range(width):
                r_cube[j,i,k] = float(cube[j,i,k])/float(white_DN[k])

    r_color_image = np.zeros((height, width, 3))

    for k in range(3):
        r_color_image[:,:,k] = r_cube[:,:,color_bands[k]]

    r_color_image[r_color_image > 1.0] = 1.0

    r_color_image_uint8_by_cv2 = cv2.normalize(r_color_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    r_color_image_uint8_by_matplot = r_color_image_uint8_by_cv2[:,:,[2, 1, 0]]

    plt.figure()
    plt.imshow(r_color_image_uint8_by_matplot)
    # plt.close()

    cv2.imwrite(f'ref_{basename}.jpg', r_color_image_uint8_by_cv2)

    description = f'reflectance data generated from {fname1} (with white diffuse reflectance standard) and {fname2} (without white diffuse reflectance standard)'
    samples = width
    lines = height
    header_offset = 0
    file_type = 'ENVI Standard'
    data_type = 4 # Floating-point: 32-bit single-precision
    interleave = 'bsq' 
    byte_order = 0
    # sensor_type = 'NH-7'
    wavelength_units = 'Nanometers'
    wavelengths_list_txt = '{'
    for k in range(bands):
        w_txt = '{:.1f}'.format(float(wavelengths_list[k]))
        # print(w_txt)
        if k<bands-1:
            wavelengths_list_txt = wavelengths_list_txt+f'{w_txt}, '
        else:
            wavelengths_list_txt = wavelengths_list_txt+f'{w_txt}'+'}'

    print('writing envi hdr')
    with open(f'ref_{basename}.hdr', 'w',  encoding='utf-8', newline='\n') as f:
        f.write('ENVI\n')
        f.write('description = {'+description+'}\n')
        # f.write(f'description = \{{description}\}\n')
        f.write(f'samples = {samples}\n')
        f.write(f'lines = {lines}\n')
        f.write(f'bands = {bands}\n')
        f.write(f'header offset = {header_offset}\n')
        f.write(f'file type = {file_type}\n')
        f.write(f'data type = {data_type}\n')    
        f.write(f'interleave = {interleave}\n')
        f.write(f'byte order = {byte_order}\n')
        f.write(f'wavelength = {wavelengths_list_txt}\n')

    print('writing envi dat')
    with open(f'ref_{basename}.dat', 'wb') as f:
        for k in range(bands):
            layer = r_cube[:,:,k]
            f.write(layer.flatten())

    print('Done!')

def dn(fname1):
    basename = os.path.splitext(os.path.basename(fname1))[0]
    dirname = os.path.dirname(fname1)

    print(f'loading hypespectral file {fname1}')
    with open(fname1, 'rb') as fid:
        data_array = np.fromfile(fid, np.uint16)

        cube = np.zeros((height, width, bands),dtype=np.uint16)
        for k in range(bands):
            print(f'loading band {k}({wavelengths_list[k]}[nm])')
            for j in range(height):
                for i in range(width):
                    index = (i-1)+width*bands*(j)+width*(k)
                    cube[j,i,k] = data_array[index]

        color_image1 = np.zeros((height, width, 3))

        for k in range(3):
            color_image1[:,:,k] = cube[:,:,color_bands[k]]


        color_image1_uint8_by_cv2 = cv2.normalize(color_image1, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    cv2.imshow("Cropped image", color_image1_uint8_by_cv2) 
    # cv2.waitKey(0) 

    description = f'DN data generated from {fname1}'
    samples = width
    lines = height
    header_offset = 0
    file_type = 'ENVI Standard'
    data_type = 2 # Integer: 16-bit signed integer
    interleave = 'bsq' 
    byte_order = 0
    # sensor_type = 'NH-7'
    wavelength_units = 'Nanometers'
    wavelengths_list_txt = '{'
    for k in range(bands):
        w_txt = '{:.1f}'.format(float(wavelengths_list[k]))
        # print(w_txt)
        if k<bands-1:
            wavelengths_list_txt = wavelengths_list_txt+f'{w_txt}, '
        else:
            wavelengths_list_txt = wavelengths_list_txt+f'{w_txt}'+'}'

    print('writing envi hdr')
    with open(f'DN_{basename}.hdr', 'w',  encoding='utf-8', newline='\n') as f:
        f.write('ENVI\n')
        f.write('description = {'+description+'}\n')
        # f.write(f'description = \{{description}\}\n')
        f.write(f'samples = {samples}\n')
        f.write(f'lines = {lines}\n')
        f.write(f'bands = {bands}\n')
        f.write(f'header offset = {header_offset}\n')
        f.write(f'file type = {file_type}\n')
        f.write(f'data type = {data_type}\n')    
        f.write(f'interleave = {interleave}\n')
        f.write(f'byte order = {byte_order}\n')
        f.write(f'wavelength = {wavelengths_list_txt}\n')

    print('writing envi dat')
    with open(f'DN_{basename}.dat', 'wb') as f:
        for k in range(bands):
            layer = cube[:,:,k]
            f.write(layer.flatten())

    print('Done!')


def ref_rgb(fname1, fname2):
    print(f'loading hypespectral file {fname1}')

    basename = os.path.splitext(os.path.basename(fname2))[0]
    out_fname = f'./{basename}_color.jpg'
    
    with open(fname1, 'rb') as fid:
        data_array = np.fromfile(fid, np.uint16)

        cube = np.zeros((height, width, 3),dtype=np.uint16)

        for k,b in enumerate(color_bands):
            print(f'loading band {b} ({wavelengths_list[b]}[nm])')
            for j in range(height):
                for i in range(width):
                    index = (i-1)+width*bands*(j)+width*(b)
                    cube[j,i,k] = data_array[index]

        color_image1 = np.zeros((height, width, 3))

        color_image1 = cube


        color_image1_uint8_by_cv2 = cv2.normalize(color_image1, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        r = cv2.selectROI("select White Diffuse Reflectance Standard", color_image1_uint8_by_cv2) 
        cv2.destroyWindow("select White Diffuse Reflectance Standard")

        # Crop image 
        cropped_cube1 = cube[int(r[1]):int(r[1]+r[3]),  
                            int(r[0]):int(r[0]+r[2]),:] 
        cropped_color_image1 = color_image1_uint8_by_cv2[int(r[1]):int(r[1]+r[3]),  
                            int(r[0]):int(r[0]+r[2])] 

        white_DN = []
        for k in range(3):
            m = np.mean(cropped_cube1[:,:,k].flatten())
            white_DN.append(m)

    if fname1 != fname2:
        print(f'loading hypespectral file {fname2}')
        with open(fname2, 'rb') as fid:
            data_array = np.fromfile(fid, np.uint16)

            cube = np.zeros((height, width, 3),dtype=np.uint16)
            for k,b in enumerate(color_bands):
                print(f'loading band {b}({wavelengths_list[b]}[nm])')
                for j in range(height):
                    for i in range(width):
                        index = (i-1)+width*bands*(j)+width*(b)
                        cube[j,i,k] = data_array[index]


    print('generating reflectance color image')
    r_cube = np.zeros((height, width, 3), dtype=np.float32)
    for k in range(3):
        print(f'loading band {k}({wavelengths_list[k]}[nm])')
        for j in range(height):
            for i in range(width):
                r_cube[j,i,k] = float(cube[j,i,k])/float(white_DN[k])

    r_color_image = np.zeros((height, width, 3))

    r_color_image = r_cube

    r_color_image[r_color_image > 1.0] = 1.0

    r_color_image_uint8_by_cv2 =  cv2.normalize(r_color_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)


    cv2.imwrite(out_fname, r_color_image_uint8_by_cv2)

    r_color_image_uint8_by_matplot = r_color_image_uint8_by_cv2[:,:,[2, 1, 0]]

    plt.imshow(r_color_image_uint8_by_matplot)
