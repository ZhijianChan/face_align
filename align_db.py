""" Align Face with rotation, translation and crop

author: chenzhijian
date: 20170521
"""
import argparse
import os
import cv2
import sys
import json
import time
import numpy as np
import normalize

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
    return parser.parse_args(argv)

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
    print 'db:',args.db_src
    print 'total:',len(landmarks_data)

    #Step 2: Normalize face
    beg_time = time.time()
    keys_ = ['eye_left', 'eye_right', 'nose', 'mouth_left', 'mouth_right']
    for i,line in enumerate(landmarks_data):
        sys.stdout.write('\rprocess: %d' % (i+1))
        sys.stdout.flush()
        tmp = json.loads(line)
        path = tmp.keys()[0]
        #1: Read Image
        imgpath = os.path.join(args.db_src, path)
        img = cv2.imread(imgpath)
	(h,w,_) = img.shape
        #2: Parse pts
        pts = [tmp[path]['landmark'][k] for k in keys_]
        pts = np.array(pts)
	pts[:,0] = pts[:,0] * w
	pts[:,1] = pts[:,1] * h
        #3: Normalize
        res = normalize.align(img, pts, args.crop_size, args.dist_y, args.pos_y)
        #4: Save normalized image
	if path[-4] == '.':
		path = '%s_%s_%s' % (path[:-4],args.img_type,path[-4:])
	elif path[-5] == '.':
		path = '%s_%s_%s' % (path[:-5],args.img_type,path[-5:])
	else:
		path = '%s_%s_.jpg' % (path,normalize_type)
        savepath = os.path.join(args.db_dst, path)
        cv2.imwrite(savepath, res)
    print '\ndone in %.2g min' % ((time.time()-beg_time) / 1000 / 60)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
