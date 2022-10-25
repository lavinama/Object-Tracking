# Object-Tracking

Tracking multi-objects using DeepSort.

https://user-images.githubusercontent.com/70475094/197843241-b1c5314f-c9ab-4001-9138-567670641201.mp4

### Structure of `DeepSORT_my_version.ipynb`:
1.  Detect the objects: Load a trained **YOLOv5** network
2.  For each of the objects define them as obstacles
3.  Use DeepSort to associate the deep convolutional features
4.  Tun the **Hungarian algorithm** to associate the different matches.

Extensions:
1. Change the **Non Maxima Suppression** formula to improve performance.
2. Use **age** to reduce the number of false positives and false negatives we get.

## Download dataset

Download the dataset along with other useful code using this [link](https://thinkautonomous-tracking.s3.eu-west-3.amazonaws.com/tracking_course.zip) or running this code:
```bash
!wget https://thinkautonomous-tracking.s3.eu-west-3.amazonaws.com/tracking_course.zip && unzip tracking_course.zip
rm tracking_course.zip
```
Details about the dataset: It is a dataset that comes from the [NVIDIA AI City Challenge Track 1: City-Scale Multi-Camera Vehicle Tracking](https://www.aicitychallenge.org/2022-challenge-tracks/)

