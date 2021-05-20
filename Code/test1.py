

import cv2
import numpy as np
import matplotlib.pyplot as plt
import git
import sys
import os
import subprocess
from test2.py import main2



if os.path.exists('Self-Correction-Human-Parsing') == False:
    subprocess.call('git clone https://github.com/PeikeLi/Self-Correction-Human-Parsing')
os.chdir('Self-Correction-Human-Parsing')
if os.path.exists('checkpoint') == False:
    os.mkdir('checkpoint')
    os.mkdir('inputs')
    os.mkdir('outputs')

dataset = 'lip'         #select from ['lip', 'atr', 'pascal']
import gdown

if dataset == 'lip':
    url = 'https://drive.google.com/uc?id=1k4dllHpu0bdx38J7H28rVVLpU-kOHmnH'
elif dataset == 'atr':
    url = 'https://drive.google.com/uc?id=1ruJg4lqR_jgQPj-9K0PP-L2vJERYOxLP'
elif dataset == 'pascal':
    url = 'https://drive.google.com/uc?id=1E5YwNKW2VOEayK9mWCS3Kpsxf-3z04ZE'

output = 'checkpoint/final.pth'
if os.path.exists(output) == False:
    gdown.download(url, output, quiet=False)



os.chdir('inputs')
#penjar imatge a input

os.chdir('..')

main2()
#("python3 simple_extractor.py --dataset 'lip' --model-restore 'checkpoints/final.pth' --input-dir 'inputs' --output-dir 'outputs' ")



def get_palette(num_cls):
    """ Returns the color map for visualizing the segmentation mask.
    Args:
        num_cls: Number of classes
    Returns:
        The color map
    """

    n = num_cls
    palette = [0] * (n * 3)
    for j in range(0, n):
        lab = j
        palette[j * 3 + 0] = 0
        palette[j * 3 + 1] = 0
        palette[j * 3 + 2] = 0
        i = 0
        while lab:
            palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
            palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
            palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
            i += 1
            lab >>= 3

    palette = np.asarray(palette) # change to array
    palette= np.reshape(palette,(20,3)) # split it in 20 triplets (r,g,b)
    return palette.astype("uint8") # cast to uint8 and return


def is_label_in_image(img, string_label, LABELS_utils, colors_utils):
    
    index = LABELS_utils.index(string_label)
    color_roba = colors_utils[index]
    mask = np.all(img == (color_roba[2], color_roba[1], color_roba[0]), axis=-1)
    
    if np.all(mask == False):
        return False, mask
    else:
        return True, mask

def adjust_pattern(img, pattern):
    h, w = img.shape[0], img.shape[1]
    hp, wp = pattern.shape[0], pattern.shape[1]

    if(h < hp):
        pattern = pattern[:h,:,:]
    else:
        while (hp < (h-hp)):
            pattern=cv2.vconcat([pattern,pattern[:hp,:,:]])
            hp = pattern.shape[0]
        pattern = cv2.vconcat([pattern,pattern[:h-hp,:,:]])

    if(w < wp):
        pattern = pattern[:,:w,:]
    else:
        while (wp < (w-wp)):
            pattern=cv2.hconcat([pattern,pattern[:,:wp,:]])
            wp = pattern.shape[1]
        pattern = cv2.hconcat([pattern, pattern[:,:w-wp,:]])

    return pattern



def change_pattern(img, mask_uint8, pattern):
    input_img_no_clothes = img.copy()
    input_img_no_clothes[:, :, 0] = cv2.bitwise_not(mask_uint8) * img[:, :, 0]
    input_img_no_clothes[:, :, 1] = cv2.bitwise_not(mask_uint8) * img[:, :, 1]
    input_img_no_clothes[:, :, 2] = cv2.bitwise_not(mask_uint8) * img[:, :, 2]
    input_img_no_clothes = input_img_no_clothes * 255
    plt.imshow(cv2.cvtColor(input_img_no_clothes, cv2.COLOR_BGR2RGB)), plt.suptitle('Source image minus mask'), plt.show()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    img[:, :, 0] = img_gray
    img[:, :, 1] = img_gray
    img[:, :, 2] = img_gray
    # adjust pattern to image size

    pattern = adjust_pattern(img, pattern)

    img = img / 255
    mask_uint8 = mask_uint8 / 255
    pattern = pattern / 255
    # np.multiply(m, m) multiplicación punto a punto de dos matrices. Funciona pero need to me same size
    img[:, :, 0] = np.multiply(img[:, :, 0], (mask_uint8 * pattern[:, :, 0]))
    img[:, :, 1] = np.multiply(img[:, :, 1], (mask_uint8 * pattern[:, :, 1]))
    img[:, :, 2] = np.multiply(img[:, :, 2], (mask_uint8 * pattern[:, :, 2]))

    img = img * 255

    img = img.astype('uint8')

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.suptitle('Recolored cloth piece'), plt.show()

    img = input_img_no_clothes + img
    return img




def change_colour(img, mask_uint8, colour_rgb):
    
    input_img_no_clothes = img.copy()
    input_img_no_clothes[:,:,0] = cv2.bitwise_not(mask_uint8)*img[:,:,0]
    input_img_no_clothes[:,:,1] = cv2.bitwise_not(mask_uint8)*img[:,:,1]
    input_img_no_clothes[:,:,2] = cv2.bitwise_not(mask_uint8)*img[:,:,2]
    input_img_no_clothes = input_img_no_clothes*255
    plt.imshow(cv2.cvtColor(input_img_no_clothes, cv2.COLOR_BGR2RGB)), plt.suptitle('Source image minus mask'), plt.show()
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    img[:,:,0] = img_gray
    img[:,:,1] = img_gray
    img[:,:,2] = img_gray
    
    img = img/255
    mask_uint8 = mask_uint8/255
    colour_rgb = colour_rgb/255
    
    img[:,:,0] = img[:,:,0]*(mask_uint8*colour_rgb[0])   
    img[:,:,1] = img[:,:,1]*(mask_uint8*colour_rgb[1])
    img[:,:,2] = img[:,:,2]*(mask_uint8*colour_rgb[2])

    img = img*255
    img = img.astype('uint8')

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.suptitle('Recolored cloth piece'), plt.show()
    
    img = input_img_no_clothes + img
    return img

if __name__ == "__main__":
    
    
    
    
    im_input = cv2.imread('inputs/in.jpg')
    im_output = cv2.imread('outputs/in.jpg')
    
    colors = get_palette(20)
    
    LABELS_utils = ['Background', 'Hat', 'Hair', 'Glove', 'Sunglasses', 'Upper-clothes', 'Dress', 'Coat', \
          'Socks', 'Pants', 'Jumpsuits', 'Scarf', 'Skirt', 'Face', 'Left-arm', 'Right-arm', 'Left-leg',
          'Right-leg', 'Left-shoe', 'Right-shoe']
        
    LABELS_K_VOLS = ['Coat']
    rgbs = [[50, 231, 241], [128,128,128]]

    for x, label in enumerate(LABELS_K_VOLS):
        cloth_in_image, mask = is_label_in_image(im_output, label, LABELS_utils, colors)
        plt.imshow(cv2.cvtColor(im_output, cv2.COLOR_BGR2RGB)), plt.suptitle('Cloth detections'), plt.show()
        
        mask_uint8 = mask.astype('uint8')*255
        plt.imshow(cv2.cvtColor(mask_uint8, cv2.COLOR_BGR2RGB)), plt.suptitle('Matching pixels with label'), plt.show()
        
        plt.imshow(cv2.cvtColor(im_input, cv2.COLOR_BGR2RGB)), plt.suptitle('Source Image'), plt.show()

        rgb = np.flip(np.asarray(rgbs[x]))

        pattern=cv2.imread('patterns/blue_feathers.jpg')

        #im_input = change_colour(im_input, mask_uint8, rgb)
        im_input = change_pattern(im_input, mask_uint8, pattern)
        plt.imshow(cv2.cvtColor(im_input, cv2.COLOR_BGR2RGB)), plt.suptitle('Final Result'), plt.show()



    cv2.imwrite("images/final.png", im_input)