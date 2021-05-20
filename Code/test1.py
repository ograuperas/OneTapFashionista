

import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
!git clone https://github.com/PeikeLi/Self-Correction-Human-Parsing
%cd Self-Correction-Human-Parsing
!mkdir checkpoints
!mkdir inputs
!mkdir outputs
"""


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
    return palette


def is_label_in_image(img, string_label, LABELS_utils, colors_utils):
    
    index = LABELS_utils.index(string_label)
    color_roba = colors_utils[index]
    mask = np.all(img == (color_roba[2], color_roba[1], color_roba[0]), axis=-1)
    
    if np.all(mask == False):
        return False, mask
    else:
        return True, mask
    


def change_colour(img, mask_uint8, colour_rgb):
    
    input_img_no_clothes = img.copy()
    input_img_no_clothes[:,:,0] = cv2.bitwise_not(mask_uint8)*img[:,:,0]
    input_img_no_clothes[:,:,1] = cv2.bitwise_not(mask_uint8)*img[:,:,1]
    input_img_no_clothes[:,:,2] = cv2.bitwise_not(mask_uint8)*img[:,:,2]
    input_img_no_clothes = input_img_no_clothes*255
    plt.imshow(cv2.cvtColor(input_img_no_clothes, cv2.COLOR_BGR2RGB)), plt.show()
    
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
    mask_uint8 = mask_uint8*255
    colour_rgb = colour_rgb*255
    
    img = img.astype('uint8')
    mask_uint8 = mask_uint8.astype('uint8')
    colour_rgb = colour_rgb.astype('uint8')
    
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.show()
    
    img = input_img_no_clothes + img
    return img



def get_colours():
    colors = get_palette(20)
    colors = np.asarray(colors)
    colors_utils = np.reshape(colors,(20,3))
       
    colors_utils = colors_utils.astype("uint8")
    return colors_utils


if __name__ == "__main__":
    
    
    
    im_input = cv2.imread('images/in.jpg')
    im_output = cv2.imread('images/out.png')
    
    
    colors_utils = get_colours()
    
    
    LABELS_utils = ['Background', 'Hat', 'Hair', 'Glove', 'Sunglasses', 'Upper-clothes', 'Dress', 'Coat', \
          'Socks', 'Pants', 'Jumpsuits', 'Scarf', 'Skirt', 'Face', 'Left-arm', 'Right-arm', 'Left-leg',
          'Right-leg', 'Left-shoe', 'Right-shoe']
        
    LABELS_K_VOLS = ['Coat', 'Upper-clothes']
    rgbs = [[128,128,128], [128,128,128]]
    
    for x, label in enumerate(LABELS_K_VOLS):
        cloth_in_image, mask = is_label_in_image(im_output, label, LABELS_utils, colors_utils)
        plt.imshow(cv2.cvtColor(im_output, cv2.COLOR_BGR2RGB)), plt.show()
        
        mask_uint8 = mask.astype('uint8')*255
        plt.imshow(cv2.cvtColor(mask_uint8, cv2.COLOR_BGR2RGB)), plt.show()
        
        plt.imshow(cv2.cvtColor(im_input, cv2.COLOR_BGR2RGB)), plt.show()
        
        
        rgb = rgbs[x]
        rgb = np.asarray(rgb)
        rgb = np.flip(rgb)
        
        if cloth_in_image:
            im_input = change_colour(im_input, mask_uint8, rgb)
        
            plt.imshow(cv2.cvtColor(im_input, cv2.COLOR_BGR2RGB)), plt.show()
        
            
        else:
            print('no hi ha peça roba k dius titu')
    













        