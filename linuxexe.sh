#!/bin/bash
TARGET_DIR=bin
TARGET_NAME=ICS
INCLUDE_MODULES=sip

echo "Creating package"

cxfreeze local_start.py --target-dir=$TARGET_DIR --target-name=$TARGET_NAME \
    --include-modules=$INCLUDE_MODULES

echo "Copying images"
for x in local_GUI/r.png local_GUI/g.png local_GUI/b.png local_GUI/rgb.png
do
    cp $x $TARGET_DIR/
done
echo "Done creating package"
