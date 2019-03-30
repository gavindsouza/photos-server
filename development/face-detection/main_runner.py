# imports
import sys #for arguments
import cv2  # for resizing
import pandas as pd # for database management
from imageio import imread  # read image
from os import path # to check if file exists
import os
import re
from sklearn.cluster import KMeans
import numpy as np

# My lib
from face_detector import detector
from quantifier import quantifier


# call the model(image) 
model_identifier = detector()
model_rater = quantifier()      

list_faces = []         # List to store what we found in an image
margin = 10
image_size = 160

#if path.exists('summary.csv'):
#    # import the file and write to df
#    print(str(path.exists('summary.csv')))
#    data = pd.read_csv('summary.csv',header=0,index_col=0)
#    # otherwise create dataframe
#else:
#    data = pd.DataFrame(columns=['index','path','quant','cluster'])
data = pd.DataFrame(columns=['index','path','quant','cluster'])

def str_to_arrist(text):
    print(text)
    return np.array([float(s) for s in re.findall(r'-?\d+\.?\d*', text)])


def calculator(path):
    '''
        Give an image path input and get the face parameter list
    '''
    # get image
    img = imread(path)  # Later change it to a function and accept from there

    # get positions(bounding boxes)
    faces = model_identifier.get_positions(img)

    # for each face you found
    for face in faces:
        (x,y,w,h) = face

        # Crop face
        #crop_img = img[y:y+h, x:x+w]

        crop_img = img[y-margin//2:y+h+margin//2,
                          x-margin//2:x+w+margin//2, :]

        # Resize to shape
        crop_img = cv2.resize(crop_img, (image_size, image_size), interpolation = cv2.INTER_AREA)

        # Store in list 
        list_faces.append(crop_img)
    
    rating_list = []
    for face in list_faces:
        #print(face.size)

        rating_list.append(model_rater.param_val_single(face))    
        # send to 'parameter calculation algorithm'
    return rating_list

def write_to_df(path_to_file,values):
    '''
        Simply take the path that is provided and write the values supplies to it.
        
        Doesn't consider the uniqueness of a path.
        Index is unique.
        Creates a table if it doesn't exist.
        Must handle the database complexity
    '''
    data.loc[data.shape[0]] = [path_to_file,quant,-1]
    return data 

# check all files in dir
def load_images_from_folder_process(folder,data):
    images = []
    maxi= 1
    for filename in os.listdir(folder): #get all files in dir
        img = cv2.imread(os.path.join(folder,filename)) # read the file
        if img is not None: # if it acutually is an image
            values = calculator(os.path.join(folder,filename)) #calculate it
            print(os.path.join(folder,filename),len(values))
            if len(values)> maxi:
                maxi = len(values) 
            for value in values: # for all the values i geti.e. faces
                data.loc[len(data)] = [len(data),os.path.join(folder,filename),value,-1] #write_to_df(filename,value) # write to dataframe
    return maxi,data


# put in df for processing
no_of_clusters,data = load_images_from_folder_process(sys.argv[1],data)

data.to_csv('summary.csv')

#for i in range(len(data)):
#    data.quant[i] = [float(s) for s in re.findall(r'-?\d+\.?\d*', data.quant[i])] 

X = np.array(data.quant.to_list())
kmeans = KMeans(n_clusters=no_of_clusters, random_state=0).fit(X)
print(kmeans.labels_)


# run calculator on each file

    #print(calculator())
# save parameters to dataset(pandas dataframe)
# (Later Stage) Calculate Clusters and all