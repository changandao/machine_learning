source ../Misc/venv/bin/activate
./pyinstaller.py --windowed --additional-hooks-dir=. --onefile PyClassificationToolbox.py
# add image directory to spec file
./pyinstaller.py PyClassificationToolbox.spec
deactivate
