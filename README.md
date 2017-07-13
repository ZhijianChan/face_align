# face_align
This project provides some face preprocessing tools, including face normalization, patch cropping etc.

### Requirement
* python 2.7

### Dependencies
* cv2
* numpy

### Landmark file
Landmark file contains multiple lines, and each line is a json string, which encodes the information of an image file.
Like this:
{ "0001/001.jpg": { "landmark": {  
&nbsp;&nbsp;&nbsp;&nbsp;"eye_left":   [ 0.1, 0.1 ],  
&nbsp;&nbsp;&nbsp;&nbsp;"eye_right":  [ 0.1, 0.1 ],  
&nbsp;&nbsp;&nbsp;&nbsp;"nose":       [ 0.1, 0.1 ],  
&nbsp;&nbsp;&nbsp;&nbsp;"mouth_left": [ 0.1, 0.1 ],  
&nbsp;&nbsp;&nbsp;&nbsp;"mouth_right":[ 0.1, 0.1 ] } }  
}

### Usage
In order to do data augmentation, the setting of parameters will be a slightly different.  
Therefore, 2 scripts are provided: xxx_casia.sh for train set and xxx_lfw.sh for test set.  
* To get more detailed information about program input
  * Run: python align_db.py 
* To process database
  * Run: bash run_xxx_casia.sh

### Demo
#### normalization
| Frontal Face | Side Face | LFW test (acc/vr@far=0.001%) |
| :----------: |:---------:|:--------------:|
| ![Alt text](/demo_pictures/align_f.jpg) | ![Alt text](/demo_pictures/align_s.jpg) | 98.02%/89.0% |
#### nose
| Frontal Face | Side Face | LFW test (acc/vr@far=0.001%) |
| :----------: |:---------:|:--------------:|
| ![Alt text](/demo_pictures/nose_f.jpg) | ![Alt text](/demo_pictures/nose_s.jpg) | 95.48%/64.47% |
#### left eye
| Frontal Face | Side Face | LFW test (acc/vr@far=0.001%) |
| :----------: |:---------:|:--------------:|
| ![Alt text](/demo_pictures/left_eye_f.jpg) | ![Alt text](/demo_pictures/left_eye_s.jpg) | 94.58%/56.20% |
#### right eye
| Frontal Face | Side Face | LFW test (acc/vr@far=0.001%) |
| :----------: |:---------:|:--------------:|
| ![Alt text](/demo_pictures/right_eye_f.jpg) | ![Alt text](/demo_pictures/right_eye_s.jpg) | 94.62%/51.03% |
#### left mouth corner
| Frontal Face | Side Face | LFW test (acc/vr@far=0.001%) |
| :----------: |:---------:|:--------------:|
| ![Alt text](/demo_pictures/left_mouth_f.jpg) | ![Alt text](/demo_pictures/left_mouth_s.jpg) | 93.15%/48.83% |
#### right mouth corner
| Frontal Face | Side Face | LFW test (acc/vr@far=0.001%) |
| :----------: |:---------:|:--------------:|
| ![Alt text](/demo_pictures/right_mouth_f.jpg) | ![Alt text](/demo_pictures/right_mouth_s.jpg) | 94.12%/62.74% |
