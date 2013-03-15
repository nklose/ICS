#!/bin/bash
TARGET_DIR=bin
TARGET_NAME=ICS
INCLUDE_MODULES=sip

echo "Creating package"

cxfreeze local_start.py --target-dir=$TARGET_DIR --target-name=$TARGET_NAME \
    --include-modules=$INCLUDE_MODULES

mkdir $TARGET_DIR/Images

echo "Copying images"
for x in Images/r.png Images/g.png Images/b.png Images/rgb.png
do
    cp $x $TARGET_DIR/Images/
done
echo "Done creating package"
