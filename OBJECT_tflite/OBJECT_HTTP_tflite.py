from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time
import cv2
import json

# import tensorflow as tf

import numpy as np
# import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels


def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results

def nothing(x):
  pass

def main():
  CAMERA_WIDTH = 640
  CAMERA_HEIGHT = 480

  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model', help='File path of .tflite file.', required=False,
      default='model.tflite')
  parser.add_argument(
      '--labels', help='File path of labels file.', required=False,
      default='coco_labels.txt')
  parser.add_argument(
      '--threshold',
      help='Score threshold for detected objects.',
      required=False,
      type=float,
      default=0.4)
  parser.add_argument(
      '--http',
      help='URL for video source.',
      required=True)
  args = parser.parse_args()

  labels = load_labels(args.labels)

  # interpreter = tf.lite.Interpreter(args.model)
  interpreter = Interpreter(args.model)

  interpreter.allocate_tensors()
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

  cap = cv2.VideoCapture(args.http)
  #cap.set(cv2.CAP_PROP_FRAME_WIDTH,CAMERA_WIDTH)
  #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

  cv2.namedWindow('Object Detecting....')

  key_detect = 0
  times=1

  while (key_detect==0) :

    ret,image_src =cap.read()

    image_size=image_src.shape
    CAMERA_HEIGHT=image_size[0]
    CAMERA_WIDTH=image_size[1]
    
    image = cv2.resize(image_src, (input_width, input_height))

    start = time.perf_counter()
    if (times==1):
      results = detect_objects(interpreter, image, args.threshold)
      inference_time = time.perf_counter() - start

      print("Length of results = " ,len(results))

      for num in range(len(results)) :
        label_id=int(results[num]['class_id'])
        box_top=int(results[num]['bounding_box'][0] * CAMERA_HEIGHT)
        box_left=int(results[num]['bounding_box'][1] * CAMERA_WIDTH)
        box_bottom=int(results[num]['bounding_box'][2] * CAMERA_HEIGHT)
        box_right=int(results[num]['bounding_box'][3] * CAMERA_WIDTH)

        if (labels[label_id] != ''):    #框選所有類別
        # if (labels[label_id] == 'person'):    #框選特定類別
          cv2.rectangle(image_src,(box_left,box_top),(box_right,box_bottom),(0,255,0),2)
          cv2.putText(image_src,labels[label_id] +' score=' +str(round(results[num]['score'],4)),
            (box_left,box_top+20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),1,cv2.LINE_AA)

        print(results[num],labels[label_id])
        print(box_left,box_top,box_right,box_bottom)
        print("***************************************************************")

      FPS_text = "FPS=" + str(round(1/inference_time,2))

      cv2.putText(image_src,
        FPS_text,
        (int(CAMERA_WIDTH*0.6),int(CAMERA_HEIGHT*0.08)),cv2.FONT_HERSHEY_SIMPLEX,1,
        (0,255,0),6,cv2.LINE_AA)

      cv2.putText(image_src,
        FPS_text,
        (int(CAMERA_WIDTH*0.6),int(CAMERA_HEIGHT*0.08)),cv2.FONT_HERSHEY_SIMPLEX,1,
        (0,0,0),2,cv2.LINE_AA)


      cv2.imshow('Object Detecting....',image_src)

    times=times+1
    if (times>20) :
      times=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
      key_detect = 1

  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()
