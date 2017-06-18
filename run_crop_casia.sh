#!/bin/bash
if [[ $# -ne 1 ]]; then
    echo 'usage: bash run_crop_casia.sh [region_id]'
    echo 'region_id:'
    echo '  2 -- left_eye'
    echo '  3 -- right_eye'
    echo '  4 -- nose'
    echo '  5 -- left mouth'
    echo '  6 -- right mouth'
fi

if [[ $1 -eq 2 ]]; then
    # left-eye patch
    python align_db.py \
        /exports_data/origin_face/casia_clean_face/data/ \
        /exports_data/origin_face/casia_clean_face/casia_clean_facebox_landmark.json \
        /home/chenzhijian/data/casia/casia_aligned \
        lefteye \
        --region 2 \
        --crop_size 160 \
        --sub_dist 50
elif [[ $1 -eq 3 ]]; then
    # right eye patch
    python align_db.py \
        /exports_data/origin_face/casia_clean_face/data/ \
        /exports_data/origin_face/casia_clean_face/casia_clean_facebox_landmark.json \
        /exports_data/czj/data/casia/casia_aligned \
        righteye \
        --region 3 \
        --crop_size 160 \
        --sub_dist 50
elif [[ $1 -eq 4 ]]; then
    # nose tip patch
    python align_db.py \
        /exports_data/origin_face/casia_clean_face/data/ \
        /exports_data/origin_face/casia_clean_face/casia_clean_facebox_landmark.json \
        /home/chenzhijian/data/casia/casia_aligned \
        nose \
        --region 4 \
        --crop_size 160 \
        --sub_dist 60
elif [[ $1 -eq 5 ]]; then
    # left mouth corner patch
    python align_db.py \
        /exports_data/origin_face/casia_clean_face/data/ \
        /exports_data/origin_face/casia_clean_face/casia_clean_facebox_landmark.json \
        /home/chenzhijian/data/casia/casia_aligned \
        leftmouth \
        --region 5 \
        --crop_size 160 \
        --sub_dist 80
elif [[ $1 -eq 6 ]]; then
    # right mouth corner patch
    python align_db.py \
        /exports_data/origin_face/casia_clean_face/data/ \
        /exports_data/origin_face/casia_clean_face/casia_clean_facebox_landmark.json \
        /home/chenzhijian/data/casia/casia_aligned \
        rightmouth \
        --region 6 \
        --crop_size 160 \
        --sub_dist 80
fi
