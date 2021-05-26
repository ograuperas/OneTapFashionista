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

#retorna la paleta de colors que utilitza el model de segmentacio de rob
#a (un numpy array amb els colors rgb de cada label possible en la imatge de segmentacio)
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


#Aquesta funcio et retorna True o False si un label en concret esta a la imatge de segmentació que ens ha donat el model
#apart et retorna la mascara (1 la part de peça de roba i 0 lo que no es la peça de roba) de la peça de roba en concret (string label)
def is_label_in_image(img, string_label, LABELS_utils, colors_utils):

    index = LABELS_utils.index(string_label)
    color_roba = colors_utils[index]
    mask = np.all(img == (color_roba[2], color_roba[1], color_roba[0]), axis=-1)

    if np.all(mask == False):
        return False, mask
    else:
        return True, mask

#Aquesta funcio s'utilitza per ajustar la imatge del patró que volem posar a la roba
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


#aquesta es la funció que sencarrega de aplicar el patro a la peça de roba
def change_pattern(img, mask_uint8, pattern):
    
    #Obtenim la imatge original pero amb la part on hi ha la roba que volem segmentar a 0 ("amb un forat")
    input_img_no_clothes = img.copy()
    input_img_no_clothes[:, :, 0] = cv2.bitwise_not(mask_uint8) * img[:, :, 0]
    input_img_no_clothes[:, :, 1] = cv2.bitwise_not(mask_uint8) * img[:, :, 1]
    input_img_no_clothes[:, :, 2] = cv2.bitwise_not(mask_uint8) * img[:, :, 2]
    input_img_no_clothes = input_img_no_clothes * 255
    #plt.imshow(cv2.cvtColor(input_img_no_clothes, cv2.COLOR_BGR2RGB)), plt.suptitle('Source image minus mask'), plt.show()
    
    #Obtenim la part de la roba que volem segmentar de la imatge original i tota la resta a 0
    im_shape = img.copy()
    
    im_shape[:,:,0] = mask_uint8*img[:,:,0]
    im_shape[:,:,1] = mask_uint8*img[:,:,1]
    im_shape[:,:,2] = mask_uint8*img[:,:,2]

    im_shape = im_shape * 255

   # plt.imshow(cv2.cvtColor(im_shape, cv2.COLOR_BGR2RGB)), plt.suptitle('label'), plt.show()
      
    #apliquem canny per a obtenir les caracteristiques de la textura de la peça de roba
    im_shape[:, :, 0] = cv2.Canny(im_shape[:, :, 0], 80, 160)
    im_shape[:, :, 1] = cv2.Canny(im_shape[:, :, 1], 80, 160)
    im_shape[:, :, 2] = cv2.Canny(im_shape[:, :, 2], 80, 160)

    #plt.imshow(cv2.cvtColor(im_shape, cv2.COLOR_BGR2RGB)), plt.suptitle('canny'), plt.show()

    im_shape = im_shape.astype(bool)
    im_shape_def = im_shape[:, :, 0] + im_shape[:, :, 1] + im_shape[:, :, 2]
    im_shape_def= im_shape_def.astype('uint8')

    #Apliquem morfologia binaria a la mascara de la textura per a remarcar mes la textura
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

    #normalitzem les imatges per a poder fer les multiplicacions de la imatge patro editada i la original editada
    img = img / 255
    mask_uint8 = mask_uint8 / 255

    #Fem un "blur manual" difuminant las parts de la imatge que coincideixen amb la mascara de textura
    masked_non_shape = mask_uint8 - im_shape_def.astype("float64")
    img[masked_non_shape > 0] = 0.85
    img[masked_non_shape == 0] *= 1.5
    pattern = pattern / 255
    # np.multiply(m, m) multiplicación punto a punto de dos matrices. Funciona pero need to me same size
    img[:, :, 0] = np.multiply(img[:, :, 0], (mask_uint8 * pattern[:, :, 0]))
    img[:, :, 1] = np.multiply(img[:, :, 1], (mask_uint8 * pattern[:, :, 1]))
    img[:, :, 2] = np.multiply(img[:, :, 2], (mask_uint8 * pattern[:, :, 2]))

    #Tornem a invertir la normalitzacio
    img = img * 255
    img = img.astype('uint8')

    #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.suptitle('Recolored cloth piece'), plt.show()

    #Sumem la imatge original sense la peça de roba amb la peça de roba modificada
    img = input_img_no_clothes + img
    return img

#aquesta es la funció que sencarrega de aplicar el color a la peça de roba
def change_colour(img, mask_uint8, colour_rgb):
    #Obtenim la imatge original pero amb la part on hi ha la roba que volem segmentar a 0 ("amb un forat")

    input_img_no_clothes = img.copy()
    input_img_no_clothes[:, :, 0] = cv2.bitwise_not(mask_uint8) * img[:, :, 0]
    input_img_no_clothes[:, :, 1] = cv2.bitwise_not(mask_uint8) * img[:, :, 1]
    input_img_no_clothes[:, :, 2] = cv2.bitwise_not(mask_uint8) * img[:, :, 2]
    input_img_no_clothes = input_img_no_clothes * 255
    #plt.imshow(cv2.cvtColor(input_img_no_clothes, cv2.COLOR_BGR2RGB)), plt.suptitle('Source image minus mask'), plt.show()

    #Obtenim la part de la roba que volem segmentar de la imatge original i tota la resta a 0
    im_shape = img.copy()

    im_shape[:, :, 0] = mask_uint8 * img[:, :, 0]
    im_shape[:, :, 1] = mask_uint8 * img[:, :, 1]
    im_shape[:, :, 2] = mask_uint8 * img[:, :, 2]

    im_shape = im_shape * 255

    #plt.imshow(cv2.cvtColor(im_shape, cv2.COLOR_BGR2RGB)), plt.suptitle('label'), plt.show()
    #apliquem canny per a obtenir les caracteristiques de la textura de la peça de roba
    im_shape[:, :, 0] = cv2.Canny(im_shape[:, :, 0], 80, 160)
    im_shape[:, :, 1] = cv2.Canny(im_shape[:, :, 1], 80, 160)
    im_shape[:, :, 2] = cv2.Canny(im_shape[:, :, 2], 80, 160)

   # plt.imshow(cv2.cvtColor(im_shape, cv2.COLOR_BGR2RGB)), plt.suptitle('canny'), plt.show()

    im_shape = im_shape.astype(bool)
    im_shape_def = im_shape[:, :, 0] + im_shape[:, :, 1] + im_shape[:, :, 2]
    im_shape_def = im_shape_def.astype('uint8')
    
    #Apliquem morfologia binaria a la mascara de la textura per a remarcar mes la textura
    kernel = np.ones((1, 1), np.uint8)
    im_shape_def = cv2.dilate(im_shape_def, kernel, iterations=1)

    #plt.imshow(im_shape_def), plt.suptitle('tri_canny'), plt.show()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    img[:, :, 0] = img_gray
    img[:, :, 1] = img_gray
    img[:, :, 2] = img_gray

    #normalitzem les imatges per a poder fer les multiplicacions de la imatge amb colors modificats editada i la original editada
    img = img / 255
    mask_uint8 = mask_uint8 / 255
    colour_rgb = colour_rgb / 255
    
    #Fem un "blur manual" difuminant las parts de la imatge que coincideixen amb la mascara de textura
    masked_non_shape = mask_uint8 - im_shape_def.astype("float64")
    img[masked_non_shape > 0] = 0.85
    img[masked_non_shape == 0] *= 1.5
    # np.multiply(m, m) multiplicación punto a punto de dos matrices. Funciona pero need to me same size
    img[:, :, 0] = np.multiply(img[:, :, 0], (mask_uint8 * colour_rgb[0]))
    img[:, :, 1] = np.multiply(img[:, :, 1], (mask_uint8 * colour_rgb[1]))
    img[:, :, 2] = np.multiply(img[:, :, 2], (mask_uint8 * colour_rgb[2]))
 
    #Tornem a invertir la normalitzacio
    img = img * 255
    img = img.astype('uint8')

    #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.suptitle('Recolored cloth piece'), plt.show()
    
    
    #Sumem la imatge original sense la peça de roba amb la peça de roba modificada
    img = input_img_no_clothes + img
    return img


#Aquesta funcio et retorna els "labels", les peçes de roba, que te una imatge
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

#Aquesta funcio et retorna la mascara de la segmentacio per peçes de roba de la imatge
def return_mask(im_input):

    for i in range(1, 6):

        im_output = cv2.imread('/workspace/img/out/out' + str(i) + '.png')

        if im_output.shape[0] == im_input.shape[0] and im_output.shape[1] == im_input.shape[1]:
            glob_in = 'in' + str(i) + '.jpg'
            glob_out = 'out' + str(i) + '.png'

            return im_output, glob_in, glob_out
