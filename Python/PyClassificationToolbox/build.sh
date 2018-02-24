#!/bin/bash
clear
source ../Misc/venv/bin/activate
rm -rf ./build/PyClassificationToolbox
rm dist/PyClassificationToolbox
python3 version.py
./pyinstaller.py PyClassificationToolbox.spec
rm -rf ./build/PyClassificationToolbox
deactivate
