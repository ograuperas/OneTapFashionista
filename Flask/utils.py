import cv2
import numpy as np
import matplotlib.pyplot as plt
#from training_model import *

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
    #plt.imshow(cv2.cvtColor(input_img_no_clothes, cv2.COLOR_BGR2RGB)), plt.suptitle('Source image minus mask'), plt.show()

    im_shape = img.copy()

    im_shape[:,:,0] = mask_uint8*img[:,:,0]
    im_shape[:,:,1] = mask_uint8*img[:,:,1]
    im_shape[:,:,2] = mask_uint8*img[:,:,2]

    im_shape = im_shape * 255

   # plt.imshow(cv2.cvtColor(im_shape, cv2.COLOR_BGR2RGB)), plt.suptitle('label'), plt.show()

    im_shape[:, :, 0] = cv2.Canny(im_shape[:, :, 0], 80, 160)
    im_shape[:, :, 1] = cv2.Canny(im_shape[:, :, 1], 80, 160)
    im_shape[:, :, 2] = cv2.Canny(im_shape[:, :, 2], 80, 160)

    #plt.imshow(cv2.cvtColor(im_shape, cv2.COLOR_BGR2RGB)), plt.suptitle('canny'), plt.show()

    im_shape = im_shape.astype(bool)
    im_shape_def = im_shape[:, :, 0] + im_shape[:, :, 1] + im_shape[:, :, 2]
    im_shape_def= im_shape_def.astype('uint8')

    kernel = np.ones((3, 3), np.uint8)
    im_shape_def = cv2.dilate(im_shape_def, kernel, iterations=1)

   # plt.imshow(im_shape_def), plt.suptitle('tri_canny'), plt.show()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    img[:,:,0] = img_gray
    img[:,:,1] = img_gray
    img[:,:,2] = img_gray

    # adjust pattern to image size
    pattern = adjust_pattern(img, pattern)

    img = img / 255
    mask_uint8 = mask_uint8 / 255

    masked_non_shape = mask_uint8 - im_shape_def.astype("float64")
    img[masked_non_shape > 0] = 0.85
    img[masked_non_shape == 0] *= 1.5
    pattern = pattern / 255
    # np.multiply(m, m) multiplicación punto a punto de dos matrices. Funciona pero need to me same size
    img[:, :, 0] = np.multiply(img[:, :, 0], (mask_uint8 * pattern[:, :, 0]))
    img[:, :, 1] = np.multiply(img[:, :, 1], (mask_uint8 * pattern[:, :, 1]))
    img[:, :, 2] = np.multiply(img[:, :, 2], (mask_uint8 * pattern[:, :, 2]))

    img = img * 255
    img = img.astype('uint8')

    #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.suptitle('Recolored cloth piece'), plt.show()

    img = input_img_no_clothes + img
    return img


def change_colour(img, mask_uint8, colour_rgb):

    input_img_no_clothes = img.copy()
    input_img_no_clothes[:,:,0] = cv2.bitwise_not(mask_uint8)*img[:,:,0]
    input_img_no_clothes[:,:,1] = cv2.bitwise_not(mask_uint8)*img[:,:,1]
    input_img_no_clothes[:,:,2] = cv2.bitwise_not(mask_uint8)*img[:,:,2]
    input_img_no_clothes = input_img_no_clothes*255
    plt.imshow(cv2.cvtColor(input_img_no_clothes, cv2.COLOR_BGR2RGB)), plt.suptitle('Source image minus mask'), plt.show()


    im_shape = img.copy()

    im_shape[:,:,0] = mask_uint8*img[:,:,0]
    im_shape[:,:,1] = mask_uint8*img[:,:,1]
    im_shape[:,:,2] = mask_uint8*img[:,:,2]

    im_shape = im_shape * 255

    plt.imshow(cv2.cvtColor(im_shape, cv2.COLOR_BGR2RGB)), plt.suptitle('label'), plt.show()

    im_shape[:, :, 0] = cv2.Canny(im_shape[:, :, 0], 80, 160)
    im_shape[:, :, 1] = cv2.Canny(im_shape[:, :, 1], 80, 160)
    im_shape[:, :, 2] = cv2.Canny(im_shape[:, :, 2], 80, 160)

    plt.imshow(cv2.cvtColor(im_shape, cv2.COLOR_BGR2RGB)), plt.suptitle('canny'), plt.show()

    im_shape = im_shape.astype(bool)
    im_shape_def = im_shape[:, :, 0] + im_shape[:, :, 1] + im_shape[:, :, 2]
    im_shape_def= im_shape_def.astype('uint8')

    kernel = np.ones((3, 3), np.uint8)
    im_shape_def = cv2.dilate(im_shape_def, kernel, iterations=1)

    plt.imshow(im_shape_def), plt.suptitle('tri_canny'), plt.show()


        
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    img[:,:,0] = img_gray
    img[:,:,1] = img_gray
    img[:,:,2] = img_gray

    img = img/255
    mask_uint8 = mask_uint8/255
    colour_rgb = colour_rgb/255

    masked_non_shape = mask_uint8 - im_shape_def.astype("float64")
    img[masked_non_shape > 0] = 0.85
    img[masked_non_shape == 0] *= 1.5
    # np.multiply(m, m) multiplicación punto a punto de dos matrices. Funciona pero need to me same size
    img[:, :, 0] = np.multiply(img[:, :, 0], (mask_uint8 * colour_rgb[0]))
    img[:, :, 1] = np.multiply(img[:, :, 1], (mask_uint8 * colour_rgb[1]))
    img[:, :, 2] = np.multiply(img[:, :, 2], (mask_uint8 * colour_rgb[2]))

    img = img*255
    img = img.astype('uint8')

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.suptitle('Recolored cloth piece'), plt.show()

    img = input_img_no_clothes + img
    return img


def return_labels(im_output, LABELS_utils, colors):
    labels = []

    llista_negra = ['Background', 'Hair', 'Glove', 'Sunglasses', 'Face', 'Left-arm', 'Right-arm', 'Left-leg',
                    'Right-leg', 'Left-shoe', 'Right-shoe']

    for label in LABELS_utils:
        bool_label, _ = is_label_in_image(im_output, label, LABELS_utils, colors)
        if bool_label == True:
            bool2 = label in llista_negra
            if bool2 == False:
                labels.append(label)

    return labels

def return_mask(im_input):
    
    
    
    for i in range(1,6):
        im_output = cv2.imread('/img/out/out' + str(i) '.png')
        
        if im_output.shape[0] == im_input.shape[0] and im_output.shape[1] == im_input.shape[1]:
            
            return im_output





