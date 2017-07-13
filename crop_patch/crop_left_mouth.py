import cv2
import math
import numpy as np

def crop(img, pts, crop_size = 160, sub_dist = 80):
    """
    crop face patch with left mouth corner located at the image center
    :param img: original face image
    :param pts: 5 facial landamrks
    :param crop_size: image size to crop
    :param sub_dist: horizontal as well as vertical distance
        between left mouth corner and eye center
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
    ml_ec_x = ec_x - pts_[3,0]
    ml_ec_y = pts_[3,1] - ec_y
    max_sub = max(ml_ec_x, ml_ec_y)
    scale_ = sub_dist / max_sub
    ml_x = int(pts_[3,0] * scale_)
    ml_y = int(pts_[3,1] * scale_)
    if scale_ <= 0:
        return None
    img = cv2.resize(img, None, fx=scale_, fy=scale_, interpolation=cv2.INTER_CUBIC)
    #Step 3: Crop
    res =  np.zeros((crop_size, crop_size, 3),dtype=np.uint8)
    (h_,w_,_) = img.shape
    # axis-X
    beg_x_dst = max(crop_size/2 - ml_x, 0)
    beg_x_src = max(ml_x - crop_size/2, 0)
    end_x_dst = min(crop_size, crop_size/2 + w_ - ml_x)
    end_x_src = min(w_, ml_x + crop_size/2)
    # axis-Y
    beg_y_dst = max(crop_size/2 - ml_y, 0)
    beg_y_src = max(ml_y - crop_size/2, 0)
    end_y_dst = min(crop_size, crop_size/2 + h_ - ml_y)
    end_y_src = min(h_, ml_y + crop_size/2)
    # copy
    res[beg_y_dst:end_y_dst, beg_x_dst:end_x_dst,:] = img[beg_y_src:end_y_src,
            beg_x_src:end_x_src,:]
    return res
