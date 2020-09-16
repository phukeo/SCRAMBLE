# SCRAMBLE


## Introduction

**SCRAMBLE** (**S**weep **C**omparison **R**esearch **A**pplication for **M**ultiple **B**ack-gated fie**L**d **E**ffect measurements) is an open-source software package for the comparison of back-gated sweep measurements for graphene field effect transistors (GFETs). It automatically determines the Dirac points, positions of maximum transconductance and calculates the field effect mobilities for electrons and holes. 

Version: 2.0

License: MIT

Request: Please cite this software package if it has been helpful with your own research - HyperLink [XXXXXX]
  
## Files Included

- scrambleFUN.py : Module handling the main functionality.
- scrambleGUI.py : Module handling all aspects of GUI.
- Example_Data.zip : Example data to get to grips with SCRAMBLE import.
- icon.ico : Application icon.
- README.md : This readme file. 


## System Requirements

1. Windows 64-bit operating system.
2. Python version 3.6.
3. Non standard Python Dependencies requiring installation (see XXXX [hyperlink to installing modules])
	* Matplotlib
	* NumPy
	* Pandas

***************
# Setup
***************

## Stage I - Acquiring & Storing Suitable Data
----------------------------------------------

### 1 - Data Acquisition

Data must be acquired from Semiconductor Device Analysers (SDA) with the following considerations:

1. The independent variable is Back-gate voltage (Vbg) in units (V)
2. The dependent variable is Current through the GFET (Isd) in units (A)
5. Files are exported from SDAs as .csv
6. There is an equal number of points for the forward and reverse sweeps
7. The sweep occurs in the following manner.
	* Forward Sweep begins at the lower Vbg value (Vbgl)
	* Forward Sweep takes an integer number of points to get the higher Vbg value (Vbgh)
	* Forward Sweep finishes at Vbgh
	* Backward Sweep begins at Vbgh 
	* Backward Sweep takes an integer number of points to get Vbgl
	* Backward Sweep finishes at Vbgl

**Demonstrative Example**:
 
* Consider a forward and reverse sweep from -100V to 100V with a step size of 1V.
* Here; Vbgl = -100 V, and Vbgh = +100 V.
* The independent variable is swept such that the following points are evaluated:
	* [-100, -99, -98 , ..., +98, +99, +100, +100, +99, +98,..., -98, -99, -100] 
* Note that +100 is evaluated twice. 

### 2 - Data Saving Conventions

In order to handle automatic import of files, the following must be considered. 

1. Files are located in folders as described below
2. Files are labelled as per the Naming Convention

Note that an example data set is provided in the online repository and is called "Example_Data". 

**Folder Structure:**

1. Data obtained from device(s) tested under the same conditions, including device repeats, should be located into a single folder, with the title of the stage name. For example all acquisitions  captured for Pristine graphene should be located in a folder called "Pristine". 
2. After device(s) are exposed to a different annealing / vacuum treatments all new acqusitions should be located in this folder, which exists in the same directory as the stage 1 folder.
3. Folder names should be numbered in chronological order such as "1_Pristine", "2_Annealed", "3_Annealed + Cleaned" for progressive stages if appropriate. 
  

**File Naming Conventions:**

Files should be saved with the following format ""TextToBeDisplayed_TextWhichIsHiddenDuringImport.csv"
* The underscore is used to seperate text that the user wants to be displayed in SCRAMBLE.
* It is recommended to keep the "TextToBeDisplayed" to a minimum to prevent elongated names in the Data List box. 
* For example: "Chip2Device3Measurement2_CapturedOnDD/MM/YY.csv" or (better) "C2D3M2_CapturedOnDD/MM/YY.csv"

**Final Name:**

During import SCRAMBLE will concatenate the name of the desired text to the name of the folder where the file lives.

**Demonstrative Example:**

1) Folder name = "2_Annealed"
2) File name = "C2D3M3_CapturedOnDD/MM/YY.csv"
Resulting name will be:
"2_Annealed_C2D3M3"

## Stage II - Downloading SCRAMBLE
---------------------------------

There are two ways to download SCRAMBLE. One way relies on users having Git previously installed on their machines

1. Downloading the as a .ZIP
2. Downloading via git

### 1 - Downloading the .ZIP 

1. Navigate to the online github repositiory [XXXXX hyperlink]
2. Press the green "Code" button and select "Download ZIP" from the dropdown
3. Extract all contents and relocate the extracted folder to a location of your choice on your machine

### 2 - Downloading via git

1. Open a terminal and navigate to the location where you would like to store SCRAMBLE 
2. Clone the files using the following command: `git clone https://github.com/phukeo/SCRAMBLE.git`


## Stage III - Customising SCRAMBLE
-----------------------------------

### 1 - Import

Users will need to customise the import algorithm to be in accordance with the data file exported from their measurement system/templates. This is easily achieved following steps below: 

1. Open your own raw data file 
2. Determine the column numbers for the data and denote these as i for Vbg and j for Isd.
3. Determine the row number for the data and denote this as k. Note that this should be the header row for the data.
4. Open up the 'scrambleFUN.py' file in a text editor
5. Navigate to line XXX which reads ` df=pd.read_csv(fName, usecols=[1,2], skiprows=248)`
6. Alter line XXX to read ` df=pd.read_csv(fName, usecols=[i,j], skiprows=(k-1))`
7. Save and close the file

### 2 - Device Parameters

Setting the device parameters to default values suitable for your devices will offer a substantial time saving everytime SCRAMBLE is used. This is easily achieved following steps below:

1. Open up the 'scrambleGUI.py' file in a text editor
2. Navigate to line XXX which reads ` sourceDrainEntry.insert(0,5)`. Replace ' 5' mV with default value for Vds
3. Navigate to line XXX which reads ` deviceLengthEntry.insert(0,95)`. Replace ' 95' um with default value for Device length
4. Navigate to line XXX which reads ` deviceWidthEntry.insert(0,80)`. Replace ' 80' um with default value for Device width
5. Navigate to line XXX which reads ` oxideThickEntry.insert(0,300)`. Replace ' 300' nm with default value for Oxide Thickness
6. Navigate to line XXX which reads ` oxideDielecEntry.insert(0,3.8)`. Replace ' 3.8' with default value for Oxide Dielectric Constant
7. Check Units! 
8. Save and close the file

************************
# Using SCRAMBLE
************************

## Stage I - Launching SCRAMBLE
-------------------------------

1. Open a terminal and navigate to the root directory for SCRAMBLE
2. Run the package ` python scrambleGUI.py`

## Stage II - Importing Data into SCRAMBLE
------------------------------------------

### Handling Import - Pathway I

Before the data has been previously processed, the user must use the "Open Folder" button to start the import process.

When the "Open Folder" button is pressed, the user must navigate to the folder where the stage name folders are located.


### Handling Import - Pathway II

Data that has been previously processed in SCRAMBLE can be swiftly imported using the "Open .BOD" button. This import pathway requires the "UserDefinedName_Data.bod" file to be selected. 

Note: Data can be exported following instructions below. 

## Stage III - Using SCRAMBLE
-----------------------------

1. Select data: Use "Open Folder" or "Open .BOD" depending on desired import pathway (see above)
2. Enter details into the "Device Parameters"
3. Highlight the data of choice from "Data List". Note that the use of standard windows controls such as shift, ctrl, mouse drag etc for the multiple selection of data is supported in this listbox. 
4. Decide on presentation from "Visualisation"
5. To plot data of choice press "Process Data" button
6. To average; select data of choice, enter name into the "User Input" box, then press "Average" button
7. To export all data press, enter name into the "User Input" box, then press "Export All" button
8. To export selected data, select data, enter name into the "User Input" box, then press "Export Select" button

Note that the individual figures can be manipulated with the navigation toolbars allowing, panning, zooming and the configuration of subplots. Pressing the “Save” icon allows the user to export the plots in various formats such as Portable Network Graphics (PNG), Scalable Vector Graphics (SVG) and Raw RGBA bitmap to name a few.

A more detailed walkthrough is given here - XXXXX [hyperlink to paper]

Acknowledgement
---------------
Funding is acknowledged from University of Plymouth GD110025-104
