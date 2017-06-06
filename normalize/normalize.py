import numpy as np
import cv2
import math

def align(img, pts, crop_size, dist_y, pos_y):
    (h,w,_) = img.shape
    ec_x = (pts[0,0] + pts[1,0])/2
    ec_y = (pts[0,1] + pts[1,1])/2
    #Step 1: Rotation
    ang_tan = (pts[0,1]-pts[1,1]) / (pts[0,0]-pts[1,0])
    ang = math.atan(ang_tan) / math.pi * 180
    M = cv2.getRotationMatrix2D((ec_x,ec_y),ang,1)
    img = cv2.warpAffine(img, M, (w,h))
    #Step 2: Translation
    M_ = np.array([[1,0,w/2-ec_x],[0,1,0]])
    img = cv2.warpAffine(img, M_, (w,h))
    pts_1 = np.concatenate((pts, np.ones((5,1),dtype=np.float32)), axis=1)
    pts_1 = np.matmul(pts_1,  np.transpose(M_))
    ec_y_t = (pts_1[0,1] + pts_1[1,1])/2
    mc_y = (pts_1[3,1] + pts_1[4,1])/2
    ec_mc = mc_y - ec_y_t
    #Step 3: Resize
    scale_ = dist_y / ec_mc
    img = cv2.resize(img, None, fx=scale_, fy=scale_, interpolation=cv2.INTER_CUBIC)
    #Step 4: Crop
    res = np.zeros((crop_size,crop_size,3),dtype=np.uint8)
    (h_,w_,_) = img.shape
    ec_y_r = ec_y_t * scale_
    offset_x = int(w_/2 - crop_size/2)
    offset_y = int(ec_y_r - pos_y)
    #axis-x
    beg_x_dst = max(-offset_x,0)
    beg_x_src = max(offset_x, 0)
    end_x_dst = min(beg_x_dst+w_, crop_size)
    end_x_src = min(beg_x_src+crop_size, w_)
    #axis-y
    beg_y_dst = max(-offset_y,0)#; print 'beg_y_dst:', beg_y_dst
    beg_y_src = max(offset_y, 0)#; print 'beg_y_src:', beg_y_src
    if beg_y_src == 0:
        end_y_dst = min(beg_y_dst+h_, crop_size)
        end_y_src = min(h_, crop_size+offset_y)
    else:
        end_y_dst = min(beg_y_dst+h_-offset_y, crop_size)
        end_y_src = min(beg_y_src+crop_size, h_)
    #print 'end_y_dst:',end_y_dst
    #print 'end_y_src:',end_y_src
    res[beg_y_dst:end_y_dst, beg_x_dst:end_x_dst, :] = img[beg_y_src:end_y_src, beg_x_src:end_x_src, :]
    return res

