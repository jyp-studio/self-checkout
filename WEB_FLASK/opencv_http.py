import cv2

import argparse

parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    '--http',
    help='URL for video source.',
    required=True)

args = parser.parse_args()

cap = cv2.VideoCapture(args.http)

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
