# -*- coding: utf-8 -*-
"""yolo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hTQl7JdPkI-RwNRvp16LnyAZs1hddFO2

# Welcome to the YOLO Workshop!

In this workshop, we will learn how to use the YOLO algorithm for object detection

## System set up

Since we will work with external files, you will need to **link this Google Colab Notebook file to your Google Drive Account**.

This is done with the following piece of code.
If you're using Jupyter Notebook on your computer, you don't need to do this
"""

import os
from google.colab import drive
drive.mount('/content/drive', force_remount=False)
os.chdir("/content/drive/My Drive/SDC Course/Tracking")


import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

"""## Define the class YOLO and the init() function"""

class YOLO():
    def __init__(self):
        """
        - YOLO takes an image as input. We should set the dimension of the image to a fixed number.
        - The default choice is often 416x416.
        - YOLO applies thresholding and non maxima suppression, define a value for both
        - Load the classes, model configuration (cfg file) and pretrained weights (weights file) into variables
        - If the image is 416x416, the weights must be corresponding to that image
        - Load the network with OpenCV.dnn function
        """
        self.confThreshold = 0.5
        self.nmsThreshold = 0.4
        self.inpWidth = 320
        self.inpHeight = 320
        classesFile = "/content/drive/My Drive/SDC Course/Tracking/Yolov3/coco.names"
        self.classes = None
        with open(classesFile,'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')
        modelConfiguration = "/content/drive/My Drive/SDC Course/Tracking/Yolov3/yolov3.cfg";
        modelWeights = "/content/drive/My Drive/SDC Course/Tracking/Yolov3/yolov3.weights";
        self.net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def getOutputsNames(self):
        '''
        Get the names of the output layers
        '''
        # Get the names of all the layers in the network
        layersNames = self.net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]


    def drawPred(self, frame, classId, conf, left, top, right, bottom):
        '''
        Draw a bounding box around a detected object given the box coordinates
        Later, we could repurpose that to display an ID
        '''
        # Draw a bounding box.
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), thickness=5)
        label = '%.2f' % conf
        # Get the label for the class name and its confidence
        if self.classes:
            assert(classId < len(self.classes))
            label = '%s:%s' % (self.classes[classId], label)
    
        #Display the label at the top of the bounding box
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=3)
        return frame

    
    def postprocess(self,frame, outs):
        """
        Postprocessing step. Take the output out of the neural network and interpret it.
        We should use that output to apply NMS thresholding and confidence thresholding
        We should use the output to draw the bounding boxes using the dramPred function
        """
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
    
        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            output_image = self.drawPred(frame,classIds[i], confidences[i], left, top, left + width, top + height)
        return frame, boxes

    
    def inference(self,image):
        """
        Main loop.
        Input: Image
        Output: Frame with the drawn bounding boxes
        """
        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(image, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False)
        # Sets the input to the network
        self.net.setInput(blob)
        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self.getOutputsNames())
        # Remove the bounding boxes with low confidence
        final_frame, boxes = self.postprocess(image, outs)
        return final_frame, boxes


