import cv2
import math
import numpy as np

def crop(img, pts, crop_size = 160, sub_dist = 50):
    """
    crop face patch with left eye located at the image center
    :param img: original face image
    :param pts: 5 facial landamrks
    :param crop_size: image size to crop
    :param sub_dist: horizontal as well as vertical distance
        between left eye and nose
        should no longer than 'sub_dist'
    :return: cropped image patch
    """
    (h,w,_) = img.shape
    ec_x = (pts[0,0] + pts[1,0]) / 2
    ec_y = (pts[0,1] + pts[1,1]) / 2
    #Step 1: Rotation
    ang_tan = (pts[0,1] - pts[1,1]) / (pts[0,0] - pts[1,0])
    ang = math.atan(ang_tan) / math.pi * 180
    M = cv2.getRotationMatrix2D((ec_x, ec_y), ang, 1)
    img = cv2.warpAffine(img, M, (w,h))
    #Step 2: Resize
    # -- get the new positions after rotation
    pts_ = np.concatenate((pts,np.ones((5,1),dtype=np.float32)), axis=1)
    pts_ = np.matmul(pts_,np.transpose(M))
    el_nose_x = pts_[2,0] - pts_[0,0]
    el_nose_y = pts_[2,1] - pts_[0,1]
    max_sub = max(el_nose_x, el_nose_y)
    scale_ = sub_dist / max_sub
    el_x = int(pts_[0,0] * scale_)
    el_y = int(pts_[0,1] * scale_)
    img = cv2.resize(img, None, fx=scale_, fy=scale_, interpolation=cv2.INTER_CUBIC)
    #Step 3: Crop
    res =  np.zeros((crop_size, crop_size, 3),dtype=np.uint8)
    (h_,w_,_) = img.shape
    # axis-X
    beg_x_dst = max(crop_size/2 - el_x, 0)
    beg_x_src = max(el_x - crop_size/2, 0)
    end_x_dst = min(crop_size, crop_size/2 + w_ - el_x)
    end_x_src = min(w_, el_x + crop_size/2)
    # axis-Y
    beg_y_dst = max(crop_size/2 - el_y, 0)
    beg_y_src = max(el_y - crop_size/2, 0)
    end_y_dst = min(crop_size, crop_size/2 + h_ - el_y)
    end_y_src = min(h_, el_y + crop_size/2)
    # copy
    res[beg_y_dst:end_y_dst, beg_x_dst:end_x_dst,:] = img[beg_y_src:end_y_src,
            beg_x_src:end_x_src,:]
    return res
