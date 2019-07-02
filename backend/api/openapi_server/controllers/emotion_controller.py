import connexion
import six
import os
from openapi_server.models.emotion_timeline import EmotionTimeline 
from openapi_server.models.emotion_timeline_emotions import EmotionTimelineEmotions # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.inline_object import InlineObject  # noqa: E501
from openapi_server import util
from openapi_server.controllers.img_util import pred_to_text, prep_single_img_selfrecorded, normalize_input
import base64
import cv2
import requests
import json

TF_CLASSIFIER_URL = os.environ.get("TF_CLASSIFIER_URL", "http://tf-classifier:8501/v1/models/model:predict")
INPUT_IMG_HEIGHT = int(os.environ.get("INPUT_IMG_HEIGHT", 71))
INPUT_IMG_WIDTH =  int(os.environ.get("INPUT_IMG_WIDTH ", 71))
INPUT_IMG_GREY =  bool(os.environ.get("INPUT_IMG_WIDTH ", False))

def predict_video(body):  # noqa: E501
    """predicts the emotions in from still images in a video over time

     # noqa: E501

    :param inline_object: 
    :type inline_object: dict | bytes

    :rtype: EmotionTimeline
    """
    if connexion.request.is_json:
        inline_object = InlineObject.from_dict(connexion.request.get_json())  # noqa: E501
    #return Error(400, inline_object)

    vidname =  inline_object.file_name + "_tempvid.webm" #TODO: UUID
    if not inline_object.file_content.startswith("data:video/webm"):
        return Error(400, "invalid file uploaded"), 400
    with open("/tmp/" + vidname, "wb") as fh:
        fh.write(base64.b64decode(inline_object.file_content))
    timeline = EmotionTimeline()
    timeline.videoname = inline_object.file_name
    timeline.emotions = predict_video_frames("/tmp/" + vidname)
    return timeline


def predict_video_frames(videofile, secondwise=True):
    
    vidcap = cv2.VideoCapture(videofile)
    if secondwise:
        #need to use the min function here because some videos returned FPS of 1000 or 2000 by mistake whcih resulted in only the first frame
        fps = min((50, int(vidcap.get((cv2.CAP_PROP_FPS)))))
        print ("extracting every {} frame from {}".format(fps,videofile))
    else:
        fps = 1 ## taking every frame
  

    success,image = vidcap.read()
    count = 0
    emotions = []
    while success:
        if (count % fps) == 0:
            emotion = EmotionTimelineEmotions()
            emotion.time = int(count / fps)
            emotion.emotion = predict_emotion(image)
            emotions.append(emotion)
            #cv2.imwrite("{}/{}_frame{}.jpg".format(targetdir, prefix , count) , image)     # save frame as JPEG file      
        success,image = vidcap.read()
       # print('Read a new frame: ', success)
        count += 1
    return emotions

def predict_emotion(image):

    img = prep_single_img_selfrecorded(image, image_shape=(INPUT_IMG_WIDTH, INPUT_IMG_HEIGHT), grey=INPUT_IMG_GREY)
    if img is None:
        return "no_face"

    img = normalize_input(img)
    payload = {
        "instances": [{'input_image': img.tolist()}]
    }
    # sending post request to TensorFlow Serving server
    r = requests.post(TF_CLASSIFIER_URL, json=payload)
    pred = json.loads(r.content.decode('utf-8'))

    return pred_to_text(pred)