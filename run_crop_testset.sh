#!/bin/bash
if [[ $# -ne 1 ]]; then
    echo 'usage: bash run_crop_lfw.sh [region_id]'
    echo 'region_id:'
    echo '  2 -- left_eye'
    echo '  3 -- right_eye'
    echo '  4 -- nose'
    echo '  5 -- left mouth'
    echo '  6 -- right mouth'
fi

db_src=/exports_data/origin_face/lfw/data/
db_dst=/home/chenzhijian/data/lfw/lfw_aligned/
landmark=/home/chenzhijian/data/lfw/files/lfw_landmark.json

if [[ $1 -eq 2 ]]; then
    # left-eye patch
    python align_db.py \
        $db_src \
        $landmark \
        $db_dst \
        lefteye \
        --region 2 \
        --crop_size 160 \
        --sub_dist 50
elif [[ $1 -eq 3 ]]; then
    # right eye patch
    python align_db.py \
        $db_src \
        $landmark \
        $db_dst \
        righteye \
        --region 3 \
        --crop_size 160 \
        --sub_dist 50
elif [[ $1 -eq 4 ]]; then
    # nose tip patch
    python align_db.py \
        $db_src \
        $landmark \
        $db_dst \
        nose \
        --region 4 \
        --crop_size 160 \
        --sub_dist 60
elif [[ $1 -eq 5 ]]; then
    # left mouth corner patch
    python align_db.py \
        $db_src \
        $landmark \
        $db_dst \
        leftmouth \
        --region 5 \
        --crop_size 160 \
        --sub_dist 80
elif [[ $1 -eq 6 ]]; then
    # right mouth corner patch
    python align_db.py \
        $db_src \
        $landmark \
        $db_dst \
        rightmouth \
        --region 6 \
        --crop_size 160 \
        --sub_dist 80
fi
