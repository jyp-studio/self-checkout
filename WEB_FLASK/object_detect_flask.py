#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response
import cv2
import argparse
import json
import os
import io
import re
import numpy as np
from PIL import Image

import tflite_runtime.interpreter as tflite

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


app = Flask(__name__)

parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    '--model', help='Directory path of model.', required=False,
    default='object_detect_model')

parser.add_argument(
    '--threshold',
    help='Score threshold for detected objects.',
    required=False,
    type=float,
    default=0.3)

parser.add_argument(
    '--video',
    help='Video number',
    required=False,
    type=int,
    default=0)

args = parser.parse_args()

model_file = args.model + '/model.tflite'

labels_file = args.model + '/labels.txt'

labels = load_labels(labels_file)

# interpreter = tf.lite.Interpreter(model_file)
interpreter = tflite.Interpreter(model_file)

interpreter.allocate_tensors()
_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

camera = cv2.VideoCapture(args.video)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def gen_frames():
    times = 1
    while True:
        success, frame = camera.read()
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        image = cv2.resize(frame, (input_width, input_height))

        if (times == 1):
            results = detect_objects(interpreter, image, args.threshold)

        times = times + 1
        if (times > 5):
            times = 1
            
        for num in range(len(results)) :
            label_id=int(results[num]['class_id'])
            box_top=int(results[num]['bounding_box'][0] * frame_height)
            box_left=int(results[num]['bounding_box'][1] * frame_width)
            box_bottom=int(results[num]['bounding_box'][2] * frame_height)
            box_right=int(results[num]['bounding_box'][3] * frame_width)

            if (labels[label_id] != ''):    #框選所有類別
            #if (labels[label_id] == 'person'):    #框選特定類別
                cv2.rectangle(frame,
                    (box_left,box_top),(box_right,box_bottom),
                    (0,255,0),2)
                cv2.putText(frame,
                    labels[label_id] +' score=' +str(round(results[num]['score'],4)),
                    (box_left,box_top+20),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,
                    (0,255,255),1,cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
