""" Align Face with rotation, translation and crop
author: chenzhijian
date: 20170521
"""
# -*- coding: utf-8 -*-
import argparse
import os
import cv2
import sys
import json
import time
import numpy as np
from normalize import normalize
from crop_patch import crop_nose
from crop_patch import crop_left_eye
from crop_patch import crop_right_eye
from crop_patch import crop_left_mouth
from crop_patch import crop_right_mouth


def main(args):
    if os.path.isdir(args.db_src) == False:
        print 'invalid db_src.'
        exit()
    if os.path.isdir(args.db_dst) == False:
        print 'invalid db_dst.'
        exit()
    if os.path.isfile(args.landmarks) == False:
        print 'invalid landmarks file.'
        exit()

    #Step 1: Loads landmarks file
    with open(args.landmarks) as fp:
        landmarks_data = [line.strip() for line in fp]
    cnt = 0
    #Step 2: Normalize face
    beg_time = time.time()
    keys_ = ['eye_left', 'eye_right', 'nose', 'mouth_left', 'mouth_right']
    for i,line in enumerate(landmarks_data):
        '''
        sys.stdout.write('\rprocess: %d' % (i+1))
        sys.stdout.flush()
        '''
        tmp = json.loads(line)
        path = tmp.keys()[0]
        #1: Read Image
        imgpath = os.path.join(args.db_src, path)
        imgpath = imgpath.encode('utf-8')
        print 'process:',i,':',imgpath
        img = cv2.imread(imgpath)
        if img is None:
            continue
        (h,w,_) = img.shape
        #2: Parse pts
        if not tmp[path]['landmark']:
            continue
        pts = [tmp[path]['landmark'][k] for k in keys_]
        pts = np.array(pts)
        pts[:,0] = pts[:,0] * w
        pts[:,1] = pts[:,1] * h
        #3: Image process
        if args.region == 1:   # crop whole face
            res = normalize.align(img, pts, args.crop_size, args.dist_y, args.pos_y)
        elif args.region == 2: # crop left eye
            res = crop_left_eye.crop(img, pts, args.crop_size, args.sub_dist)
        elif args.region == 3: # crop right eye
            res = crop_right_eye.crop(img, pts, args.crop_size, args.sub_dist)
        elif args.region == 4: # crop nose
            res = crop_nose.crop(img, pts, args.crop_size, args.sub_dist)
        elif args.region == 5: # crop left mouth
            res = crop_left_mouth.crop(img, pts, args.crop_size, args.sub_dist)
        elif args.region == 6: # crop right mouth
            res = crop_right_mouth.crop(img, pts, args.crop_size, args.sub_dist)
        if res is None:
            continue
        #4: Save normalized image
        if path[-4] == '.':
            path = '%s_%s_%s' % (path[:-4],args.img_type,path[-4:])
        elif path[-5] == '.':
            path = '%s_%s_%s' % (path[:-5],args.img_type,path[-5:])
        else:
            path = '%s_%s_.jpg' % (path,normalize_type)
        savepath = os.path.join(args.db_dst, path)
        savepath = savepath.encode('utf-8')
        cv2.imwrite(savepath, res)
        cnt += 1

    print 'db:',args.db_src
    print 'total:',len(landmarks_data)
    print 'success:',cnt
    print '\ndone in %.2g minutes' % ((time.time()-beg_time)/60.)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('db_src', type=str, 
        help='Source directory of database')
    parser.add_argument('landmarks', type=str,
        help='Json file of landmarks')
    parser.add_argument('db_dst', type=str, 
        help='Target directory of database')
    parser.add_argument('img_type', type=str, 
        help='Saved image type')
    parser.add_argument('--crop_size', type=int,
        help='Width/Height of normalized face', default=144)
    parser.add_argument('--dist_y', type=int,
        help='Distance between eye center and mouth center', default=48)
    parser.add_argument('--pos_y', type=int,
        help='Y-coordinate of eye center', default=48)
    parser.add_argument('--sub_dist', type=int,
        help='sub-distance between specific keypoints', default=60)
    parser.add_argument('--region', type=int,
        help='crop region', default=1, choices=[1,2,3,4,5,6])
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
