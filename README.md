# Tidal Analysis (T Tide and U Tide) GUI using PyQt5 
This is a tidal analysis GUI using T Tide and U Tide (both Python version).

The GUI itself was developed by _Rifqi Muhammad Harrys_ using PyQt5, a python GUI library.

Both T Tide and U Tide developed by two different entities.
The original versions of [T Tide](https://www.eoas.ubc.ca/~rich/#T_Tide "T Tide Harmonic Analysis Toolbox") and [U Tide](https://www.mathworks.com/matlabcentral/fileexchange/46523-utide-unified-tidal-analysis-and-prediction-functions?w.mathworks.com "UTide Unified Tidal Analysis and Prediction Functions") 
are in MATLAB language developed by _R. Pawlowicz et. al_ (T Tide) and _Daniel Codiga_ (U Tide).

The python version of [T Tide](https://github.com/moflaher/ttide_py "T Tide for Python") and [U Tide](https://github.com/wesleybowman/UTide "U Tide for Python") were developed by _moflaher_ (T Tide) and _Wesley Bowman_ (U Tide).

A description of the theoretical basis of the analysis and some implementation details of T Tide and U Tide Matlab version can be found in:

>R. Pawlowicz, B. Beardsley, and S. Lentz, "Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE", Computers and Geosciences 28 (2002), 929-937. 
      
>Codiga, D.L., 2011. Unified Tidal Analysis and Prediction Using the UTide Matlab Functions. Technical Report 2011-01. Graduate School of Oceanography, University of Rhode Island, Narragansett, RI. 59pp.

## Getting Started
In order to use this tide analysis and prediction GUI for python, you need to prepare several dependencies beforehand

1. Install python 3
2. Install python modules on the list below:
   - numpy
   - scipy
   - pandas
   - matplotlib
   - PyQt5
   - utide for python
   - ttide for python
   
   To Install the modules listed above (except ttide), type in script below into terminal or cmd or powershell:
   
        pip install numpy scipy pandas matplotlib PyQt5 utide

   or run:

        python -m pip install numpy scipy pandas matplotlib PyQt5 utide

   ttide for python doesn't have a pip package installer, so its installation has different steps, which is:
   1. Download ttide for python from https://github.com/moflaher/ttide_py
   2. Extract from zip file
   3. Run `python setup.py install` from inside the extracted folder using terminal or cmd or powershell.
      to go inside the extracted folder, type in `cd` or `dir` and then type the folder path
3. Run `python tide_widget.py`

## How to Use
 1. Prepare your tide observation data containing at least two types of dataset which is water level and timestamp. Your data must contain headers on every dataset column.

 2. Press "Merge Data" button to merge your multiple files into a single file. Note that this feature only works if your files have identical features (e.g. same header type, same columns, etc).

 3. Push "Load Data" button to load your data and a dialog will pop out. Push "Open File(s)" button to select 1 or more text files (.txt, .csv, or .dat). Push "Open Folder" button to select files inside a folder/directory and its subfolder/subdirectory (select text type before push "Open Folder" to filter file type from the directory).

 4. Select your data separator. Select your text type only if you want to open from a folder and do it before you push "Open Folder".

 5. Insert row/line number to use as the column names into "Header Starting Line" form. If the first line of the header is the column names, insert "1". If you use valeport data as an input file, insert "22" because the column names' location is on the 22nd line.

 6. Insert row/line number of your data starting right after the header or the column names into "Data Starting Line" form. If your data starting right after the header, insert "1". If you use valeport data as an input file, insert "2" because the data starts on the second line after the header.

 7. Push "Load" after you're done. Check "Show All Data to Table" if you want to load all data to main widget table (a huge number of data will slowed down the process). If you leave it unchecked, it will only show first 100 dataset.

 8. From Day First input, select "True" if your data timestamp parses dates with the day first. Otherwise, select "False" if your data doesn't begin with day first. As an example, if the time parses 10/09/2019 (October 9th 2019), select "False".

 9. Select timestamp and depth header name of your data from the selection with the corresponding name right beside it.

10. If you wish to plot the observation data, push "Plot Observation Data" which located under "Merge Data" button. Note that you have to select the right timestamp and depth header first in order to plot your observation data.

11. Select one of the tidal analysis method (T Tide or U Tide).

12. Type in the latitude of your tide station in which your observation data was taken.

13. Push "Save File Location" button to select the location of analysed tidal data you wish to save in .txt format, or insert the data path manually into a text box on the right side of the push button.

14. Select the first and last date of tide prediction from two calendar boxes.

15. Insert time interval of tide prediction in hourly unit or in minutes.

16. Push "Analyse Tide" button if you wish to save the tide parameters. The report will be saved in the save location that you insert before with an addition of "report" and the tide method at the end of the file name.

17. Select the checkboxes in the middle of "Analyse Tide" and "Predict Tide" button as you desire. The default state would be checked on both checkboxes (save prediction and plot prediction). If you unselect both checkboxes, pushing "Predict Tide" button will lead to showing tide prediction table.

18. Push "Predict Tide" button if wish to go straight to make tide prediction without saving tidal analysis parameters into a file. If you check on "Save Prediction" box, the tide prediction file will be saved in the save location that you insert before with an addition of the tide method at the end of the file name.