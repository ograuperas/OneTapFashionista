import cv2
import numpy as np
import matplotlib.pyplot as plt
import git
import sys
import os
import subprocess


def dowload_model():
        
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
    
    

def make_prediction():
    os.chdir('inputs')
    #penjar imatge a input
    
    os.chdir('..')
    
    main2()
    #("python3 simple_extractor.py --dataset 'lip' --model-restore 'checkpoints/final.pth' --input-dir 'inputs' --output-dir 'outputs' ")