# algo to detect face positions and give out bounding boxes positions
# For now take haar cascade for quick prototyping
# Send the bounding boxes

# Haar Cascade 

import cv2
import sys

class detector:

    def __init__(self,algorithm='haar'):
        '''
        Main constructor.

        Parameters:
        arg1 (String): Algorithm selection, default is 'haar'.
                       Possible selections :-
        '''
        self.algorithm = algorithm

    def get_positions(self,img):
        '''
        Gets the bounding boxes positions.

        This is a wrapper function for all the algorithms in this list, 
        each algorithm can be individually accessed however.
        Main purpose is for ease of use.
        Select algorithm during init. 
        Default to haar.

        Parameters:
        arg1 (numpy.ndarray): image to work on

        Returns: 
        numpy.ndarray: Bounding boxes positions
        '''
        if self.algorithm == 'haar':
            faces = self.haar_cascader(img)
            
        return faces 

    def haar_cascader(self,img):
        '''
        Gets the bounding boxes positions.

        Here, haar cascade is specifically used.

        Parameters:
        arg1 (numpy.ndarray): image to work on

        Returns: 
        numpy.ndarray: Bounding boxes positions
        '''
        path_frontfacecascade = "haarcascade_frontalface_alt2.xml"   # Get the xml
        model = cv2.CascadeClassifier(path_frontfacecascade)            # Create Model 
        
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                # Gray conversion for haar requirement

        faces = model.detectMultiScale(                                 # faces will store the array of boxes of positions
            img_gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(1,1),
            flags = cv2.CASCADE_SCALE_IMAGE
        )        
        return faces
        

