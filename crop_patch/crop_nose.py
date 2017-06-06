import cv2
import math
import numpy as np

def crop(img, pts, crop_size = 160, sub_dist = 60):
    """
    crop face patch with nose staying in the center
    :param img: original face image
    :param pts: 5 facial landamrks
    :param crop_size: image size to crop
    :param sub_dist: distance between nose and eye center
        as well as distance between nose and mouth center
        should no longer than 'sub_dist'
    :return: cropped image patch
    """
    (h,w,_) = img.shape
    ec_x = (pts[0,0] + pts[1,0])/2
    ec_y = (pts[0,1] + pts[1,1])/2
    #Step 1: Rotation
    ang_tan = (pts[0,1] - pts[1,1]) / (pts[0,0] - pts[1,0])
    ang = math.atan(ang_tan) / math.pi * 180
    M = cv2.getRotationMatrix2D((ec_x, ec_y), ang, 1)
    img = cv2.warpAffine(img, M, (w,h))
    #Step 2: Resize
    # -- get the new position after rotation
    pts_ = np.concatenate((pts,np.ones((5,1),dtype=np.float32)), axis=1)
    pts_ = np.matmul(pts_,np.transpose(M))
    # (eye center)
    ec_x = (pts_[0,0] + pts_[1,0])/2
    ec_y = (pts_[0,1] + pts_[1,1])/2
    # (mouth center)
    mc_x = (pts_[3,0] + pts_[4,0])/2
    mc_y = (pts_[3,1] + pts_[4,1])/2
    # (nose)
    nose_x = pts_[2,0]
    nose_y = pts_[2,1]
    # (sub-distances)
    ec_nose = nose_y - ec_y
    nose_mc = mc_y - nose_y
    max_sub = max(ec_nose, nose_mc)
    scale_  = sub_dist / max_sub
    nose_x_ = int(nose_x * scale_)
    nose_y_ = int(nose_y * scale_)
    img = cv2.resize(img, None, fx=scale_, fy=scale_, interpolation=cv2.INTER_CUBIC)
    #Step 3: Crop
    res = np.zeros((crop_size, crop_size, 3),dtype=np.uint8)
    (h_,w_,_) = img.shape
    # axis-X
    beg_x_dst = max(crop_size/2 - nose_x_, 0)
    beg_x_src = max(nose_x_ - crop_size/2, 0)
    end_x_dst = min(crop_size, crop_size/2 + w_ - nose_x_)
    end_x_src = min(w_, nose_x_ + crop_size/2)
    # axis-Y
    beg_y_dst = max(crop_size/2 - nose_y_, 0)
    beg_y_src = max(nose_y_ - crop_size/2, 0)
    end_y_dst = min(crop_size, crop_size/2 + h_ - nose_y_)
    end_y_src = min(h_, nose_y_ + crop_size/2)
    # copy
    res[beg_y_dst:end_y_dst, beg_x_dst:end_x_dst,:] = img[beg_y_src:end_y_src,
            beg_x_src:end_x_src,:]
    return res
