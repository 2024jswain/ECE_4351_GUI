This is an education GUI that shows computer vision methods on a real time video of the user

To Use:

1. Create a conda env using
conda env create -f environment.yml

2. Activate conda env using
conda activate CV_class

3. Run main.py in the conda environment


Known Issues:

1. Video sometimes skips a frame when changing filters

2. Camera resources are not always deallocated properly

3. Parameters for deselected filters stay on page

The app is in a working state, but has room for improvement on these issues.
In hindsight, streamlit was probably the wrong tool to build this with.