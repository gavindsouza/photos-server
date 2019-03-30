from keras.models import load_model
import numpy as np
import os
import cv2
from imageio import imread
from keras.models import load_model
from keras import backend as K

class quantifier:
    def __init__(self):
        # Load Model for quantitative analysis
        self.cascade_path = 'haarcascade_frontalface_alt2.xml' # Cascade 
        self.image_size = 160 # cropping size
        
    def process(self,x):
        if x.ndim == 4:
            axis = (1, 2, 3)
            size = x[0].size
        elif x.ndim == 3:
            axis = (0, 1, 2)
            size = x.size
        else:
            raise ValueError('Dimension should be 3 or 4')

        mean = np.mean(x, axis=axis, keepdims=True)
        std = np.std(x, axis=axis, keepdims=True)
        std_adj = np.maximum(std, 1.0/np.sqrt(size))
        y = (x - mean) / std_adj
        return y
    
    def l2_normalize(self,x, axis=-1, epsilon=1e-10):
        output = x / np.sqrt(np.maximum(np.sum(np.square(x), axis=axis, keepdims=True), epsilon))
        return output


    def param_val_single(self,image, model_path = 'facenet_keras.h5'):
        model = load_model(model_path)  # load this model
        take_dis = self.process( 

            np.array([image])
        ) #send cropped image

        score = model.predict(take_dis)  # get a score
            


        fin = self.l2_normalize(np.concatenate(score)) # make a single array and normalize

        K.clear_session()
        return fin