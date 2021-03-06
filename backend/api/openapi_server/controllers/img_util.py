import numpy as np
import os
import cv2
def prep_single_img_selfrecorded(img,  viola_jones_model="haarcascade_files/haarcascade_frontalface_default.xml", image_shape=(48, 48), grey=True):
    face_detection = cv2.CascadeClassifier(viola_jones_model)
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #face detection 
    faces = face_detection.detectMultiScale(grey_img,scaleFactor=1.1,minNeighbors=5,minSize=(20,20),flags=cv2.CASCADE_SCALE_IMAGE)
    # sorting out images with failed detection
    target_face = None
    if len(faces) == 0:
        print ("ERROR: there was no face detected on image, discarding it")
        return None
    elif len(faces) > 1:
        print ("WARNING: there was more than one face detected on image, using the biggest one")
        for face in faces:
            size = face[2] * face[3]
            if target_face is None or (target_face[2] * target_face[3] < size):
                target_face = face
    else:
        target_face = faces[0]
        ## cropping image to only face
    (fX, fY, fW, fH) = target_face
    if grey:
        img = grey_img[ fY: fY + fH, fX: fX +fW].copy()
    else:
        img = img[ fY: fY + fH, fX: fX +fW].copy()
    #rescale it
    img = cv2.resize(img.astype('uint8'),image_shape)

    return img.astype('float32')

def normalize_input(image):
    image = image.astype('float32')
    image = image / 255.0
    return image


def pred_to_text(pred, cols = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise' ]):
    
    # Decoding the response
    # getting the emotion label for the highest predicition
    highest = 0.0
    emotion = ""
    for i in range(len(pred['predictions'][0])):
        if(highest < pred['predictions'][0][i]):
            highest = pred['predictions'][0][i]
            emotion = cols[i]
    return emotion