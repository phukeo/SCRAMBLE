import tkinter as tk
import scrambleFUN as sfu
import os
import pandas as pd

from tkinter import *
from tkinter import messagebox
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilenames, askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

originalDirect=os.getcwd() # Directs all dialogue boxes to the initial working directory

#######################
## CONSTRUCT THE APP ##
#######################

## CONSTRUCT MAIN CONTAINER ##

root=tk.Tk()
root.title("SCRAMBLE")
root.iconbitmap("scrambleICON.ico")
root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=1)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Position window in middle of screen:
w = 1300 # width for the Tk root
h = 600 # height for the Tk root

# Get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# Calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# Set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

## CONSTRUCT CONTROL PANEL ##

# Configure the control panel
leftFrame=Frame(root,width=200, height=700, bg="#f0f0f0")
leftFrame.grid(row=0, column=0, padx=2, pady=2, sticky='nesw', rowspan=2)
leftFrame.grid_propagate(0)
leftFrame.grid_rowconfigure(0, weight=1)
leftFrame.grid_rowconfigure(1, weight=1)
leftFrame.grid_rowconfigure(2, weight=1)
leftFrame.grid_rowconfigure(3, weight=1)
leftFrame.grid_rowconfigure(4, weight=1)
leftFrame.grid_rowconfigure(5, weight=1)
leftFrame.grid_columnconfigure(0, weight=1)
leftFrame.grid_columnconfigure(1, weight=1)
leftFrame.grid_columnconfigure(2, weight=1)
leftFrame.grid_columnconfigure(3, weight=1)

# Configure the Data Selection frame
frame0 = LabelFrame(leftFrame, text="Data Selection", padx=2, pady=2)
frame0.grid(row=0, column=0, padx=2, pady=2,sticky='nesw',  columnspan=4)
frame0.grid_rowconfigure(0, weight=1, pad=5)
frame0.grid_columnconfigure(0, weight=1)
frame0.grid_columnconfigure(1, weight=1)
frame0.grid_columnconfigure(2, weight=1)
frame0.grid_columnconfigure(3, weight=1)
frame0.grid_propagate(1)

# Configure the Device Parameters  frame
frame1 = LabelFrame(leftFrame,text="Device Parameters", padx=2,pady=2)
frame1.grid(row=1, column=0, padx=2, pady=2,sticky='nesw',  columnspan=4)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=1)
frame1.grid_rowconfigure(0, weight=1)
frame1.grid_rowconfigure(1, weight=1)
frame1.grid_rowconfigure(2, weight=1)
frame1.grid_rowconfigure(3, weight=1)
frame1.grid_rowconfigure(4, weight=1)
frame1.grid_propagate(1)

# Configure the Data List frame
frame2 = LabelFrame(leftFrame,text="Data List", padx=2,pady=2)
frame2.grid(row=2, column=0, padx=2, pady=2,sticky='nesw',  columnspan=4)
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_propagate(1)

# Configure the Visualisation frame
frame25 = LabelFrame(leftFrame,text="Visualisation", padx=2,pady=2)
frame25.grid(row=3, column=0, padx=2, pady=2,sticky='nesw',  columnspan=4)
frame25.grid_columnconfigure(0, weight=1)
frame25.grid_columnconfigure(1, weight=1)
frame25.grid_columnconfigure(2, weight=1)
frame25.grid_columnconfigure(3, weight=1)
frame25.grid_rowconfigure(0, weight=1)
frame25.grid_propagate(1)

# Configure the Functions frame
frame3 = LabelFrame(leftFrame,text="Functions", padx=2,pady=2)
frame3.grid(row=4, column=0, padx=2, pady=2,sticky='nesw',  columnspan=4)
frame3.grid_columnconfigure(1, weight=1)
frame3.grid_columnconfigure(0, weight=1)
frame3.grid_columnconfigure(2, weight=1)
frame3.grid_columnconfigure(3, weight=1)
frame3.grid_rowconfigure(0, weight=1)
frame3.grid_propagate(1)

# Configure the Export frame
frame4 = LabelFrame(leftFrame,text="Export", padx=2,pady=2)
frame4.grid(row=5, column=0, padx=2, pady=2,sticky='nesw',  columnspan=4)
frame4.grid_columnconfigure(0, weight=1)
frame4.grid_columnconfigure(1, weight=1)
frame4.grid_columnconfigure(2, weight=1)
frame4.grid_columnconfigure(3, weight=1)
frame4.grid_rowconfigure(0, weight=1)
frame4.grid_rowconfigure(1, weight=1)
frame4.grid_propagate(1)

## CONSTRUCT VISUALISATION SCREEN ## 

# Configure Sweep Visualisation frame
middleFrame = LabelFrame(root, text="Sweep Visualisation", bg="#f0f0f0")
middleFrame.grid(row=0, column=1, padx=2, pady=2,sticky='nesw')
middleFrame.grid_propagate(0)

# Configure Mobilities frame
middleFrameB = LabelFrame(root, text="Mobilities", bg="#f0f0f0")
middleFrameB.grid(row=1, column=1, padx=2, pady=2,sticky='nesw')
middleFrameB.grid_propagate(0)

# Configure Parameter Details frame
rightFrame= LabelFrame(root, text="Parameter Details", bg="#f0f0f0")
rightFrame.grid(row=0, column=2, padx=2, pady=2, rowspan=2,sticky='nesw')
rightFrame.grid_propagate(0)

######################### 
## INITIAL CODE TO RUN ##
#########################

# Initialise Parameters
r = IntVar() # For RadioButtons
h=1  # Button height
w=30 # Button width
# Build the List to selectdata from
lstbox = Listbox(frame2, selectmode=EXTENDED, height=8, width=w,exportselection=0)
lstbox.grid(row=0, column=0, columnspan=4, sticky="nesw")

############################################################
## DEFINE BUTTON PRESS FUNCTIONS TO HANDLE FUNCTION CALLS ##
############################################################

def buttonPress (function, *args):
    if function == sfu.importData:
        originalDirect
        directory=askdirectory(initialdir=os.path.dirname(originalDirect+"\\"),title='Please select a folder where the data lives...')

        if directory=="": # This handles the case where the user presses cancel. 
            pass
        else:
            v1,v2,v3=function(directory)

            newDesk=v3
            lstbox.delete('0', 'end')
            for i, item in enumerate (newDesk):
                lstbox.insert(i,item)
            lstbox.grid(row=0, column=0, columnspan=4, sticky="nesw")

            # Create a vertical scrollbar to the right of the listbox
            yscroll = tk.Scrollbar(frame2,command=lstbox.yview, orient=tk.VERTICAL)
            yscroll.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E)
            lstbox.configure(yscrollcommand=yscroll.set)


def buttonPress1 (function,*args):
    if function == sfu.importBOD:
        originalDirect
        directory=askopenfilename(initialdir=os.path.dirname(originalDirect+"\\"),title='Please select a .BOD file to look at...')

        if directory=="": # This handles the case where the user presses cancel.
            pass
        else:

            v1,v2=function(directory)
            
            niceCoffee=v2
            lstbox.delete('0', 'end')
            for i, item in enumerate (niceCoffee):
                lstbox.insert(i,item)
            lstbox.grid(row=0, column=0, columnspan=4, sticky="nesw")

            # Create a vertical scrollbar to the right of the listbox
            yscroll = tk.Scrollbar(frame2,command=lstbox.yview, orient=tk.VERTICAL)
            yscroll.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E)
            lstbox.configure(yscrollcommand=yscroll.set)

    if function == sfu.exportALLF:
        userExportName=userSaveNameEntry.get()
        
        v1=function()

        BODExportAll=v1
        exitName1= askdirectory(initialdir=os.path.dirname(originalDirect+"\\"),title='Please select a folder to save data to:')+"/" # show an "Open" dialog box and return the path to the selected file
        exitName2=exitName1[0:exitName1.rfind("/")+1]+userExportName+"_Export_All"
        BODExportAll.to_csv(exitName2+"_Data.bod", encoding='utf-8-sig', index = False)
        tk.messagebox.showinfo(title="SCRAMBLE", message="Data Exported to: \n"+exitName2+"\n\nKeep up the good work!")

def itemsFromList (function,*arg):
    
    # Get the items in the list
    selectedList=[]
    cs=lstbox.curselection()
    for items in cs:
        selectedList.append(lstbox.get(items))
    
    # Get the Source Drain Voltage
    try:
        Vds1=float(sourceDrainEntry.get())
        Vds=Vds1/1000
    except:
        Vds=0.005
        sourceDrainEntry.delete(0,END)
        sourceDrainEntry.insert(0,"ERROR VDS=0.005")

    # Get the Device Length
    try:
        deviceL1=float(deviceLengthEntry.get())
        deviceL=deviceL1/(1*10**6)
    except:
        deviceL=9.5*10**-5
        deviceLengthEntry.delete(0,END)
        deviceLengthEntry.insert(0,"ERROR Length=9.5E-5")

    # Get the Device Width
    try:
        deviceW1=float(deviceWidthEntry.get())
        deviceW=deviceW1/(1*10**6)
    except:
        deviceW=8.0*10**-5
        deviceWidthEntry.delete(0,END)
        deviceWidthEntry.insert(0,"ERROR Width=8.0E-5")

    ### Get the Oxide Thickness
    try:
        oxideThick1=float(oxideThickEntry.get())
        oxideThick=oxideThick1/(1*10**9)
    
    except:
        oxideThick=3.0*10**-7
        oxideThickEntry.delete(0,END)
        oxideThickEntry.insert(0,"ERROR Tox=3.0E-7")

    ### Get the Oxide Dielectric Constant
    try:
        oxideDielectric=float(oxideDielecEntry.get())

    except:
        oxideDielectric=3.8
        oxideDielecEntry.delete(0,END)
        oxideDielecEntry.insert(0,"ERROR Er=3.8")

    # Plotting resistance or current depends on the mouse variable 
    mouse=r.get() # Variable for Radiobuttons
    
    if function == sfu.processData:
    
        #######################################
        ## PREAMBLE TO PROCESS DATA FUNCTION ##
        #######################################
        
        # Delete all widgets in the main window
        try:
            for widget in middleFrame.winfo_children():
                widget.destroy()
            for widget in middleFrameB.winfo_children():
                widget.destroy()
            for widget in rightFrame.winfo_children():
                widget.destroy()
        except:
            pass

        fig,figStats,figStatsL=sfu.processData(selectedList,Vds,deviceL,deviceW,oxideThick,oxideDielectric, mouse)

        # Put the figures onto the Cavases with Nvaigation Toolbars
        canvas1 = FigureCanvasTkAgg(fig,master=middleFrame)
        toolbar=NavigationToolbar2Tk(canvas1,middleFrame)
        canvas1.get_tk_widget().pack(side=TOP,fill=BOTH, expand=True)
        canvas1.draw()
        canvas2 = FigureCanvasTkAgg(figStats,master=rightFrame)
        toolbar2=NavigationToolbar2Tk(canvas2,rightFrame)
        canvas2.get_tk_widget().pack(side=TOP,fill=BOTH, expand=True)
        canvas2.draw()
        canvas3 = FigureCanvasTkAgg(figStatsL,master=middleFrameB) 
        toolbar3=NavigationToolbar2Tk(canvas3,middleFrameB)
        canvas3.get_tk_widget().pack(side=TOP,fill=BOTH, expand=True)
        canvas3.draw()

    if function == sfu.exportSelectedF:
        userExportName=userSaveNameEntry.get() # Determine the user inputted name

        BODExportSelect,BODStats1,BODMobility1=sfu.exportSelectedF(selectedList,Vds,deviceL,deviceW,oxideThick,oxideDielectric)

        exitName= askdirectory(initialdir=os.path.dirname(originalDirect+"\\"),title='Save to: ') # Location for save files
        exitName1=exitName+("/")+userExportName+"_Export_Selected"
        BODExportSelect.to_csv(exitName1+"_Data.bod", encoding='utf-8-sig', index = False)
        BODStats1.to_csv(exitName1+"_Parameters"+".bod", encoding='utf-8-sig', index = True)
        BODMobility1.to_csv(exitName1+"_Mobilities"+".bod", encoding='utf-8-sig', index = False)
        tk.messagebox.showinfo(title="SCRAMBLE", message="Data Exported to: \n\n"+exitName1+"\n\nKeep up the good work!")

    if function == sfu.averageData:
        userExportName=userSaveNameEntry.get() # Determine the user inputted name

        v1=function(selectedList,userExportName)

        newDesk=v1
        lstbox.delete('0', 'end') # Delete all entries in the listbox
        for i, item in enumerate (newDesk):
            lstbox.insert(i,item)
        lstbox.grid(row=0, column=0, columnspan=4, sticky="nesw")

        # Create a vertical scrollbar to the right of the listbox
        yscroll = tk.Scrollbar(frame2,command=lstbox.yview, orient=tk.VERTICAL)
        yscroll.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E)
        lstbox.configure(yscrollcommand=yscroll.set)

###################################################
## GENERIC FUNCTION(S) TO RUN WITHIN THIS MODULE ##
###################################################

def sort(lst): #Function which takes the filename tuple from the dialog box and returns a sorted list of filenames 
    lst=list(lst)
    lst.sort()
    return lst

 
##################################################
## POPULATE MAIN CONTAINER WITH BUTTONS/WIDGETS ##
##################################################

## BUTTONS / LABELS ##

openFolder=tk.Button(frame0,text="Open Folder", height=h, width=w, padx=5, pady=5, command=lambda: buttonPress(sfu.importData))
openFolder.grid(row=0, column=0,sticky='nesw',columnspan=2)

openFolderBOD=tk.Button(frame0,text="Open .BOD", height=h, width=w, padx=5, pady=5, command=lambda: buttonPress1(sfu.importBOD))
openFolderBOD.grid(row=0, column=2,sticky='nesw',columnspan=2)

sourceDrainLabel=tk.Label(frame1, text="Vds (mV):",padx=5, pady=5, width=w)
sourceDrainLabel.grid(row=0,column=0,sticky="nesw")

sourceDrainEntry=tk.Entry(frame1, justify="center", width=w)
sourceDrainEntry.grid(row=0, column=1,sticky="nesw")
sourceDrainEntry.insert(0,5)

deviceLengthLabel=tk.Label(frame1, text="Device Length (\u03bcm):",padx=5, pady=5, width=w)
deviceLengthLabel.grid(row=1, column=0,sticky="nesw",columnspan=1)

deviceLengthEntry=tk.Entry(frame1, justify="center", width=w)
deviceLengthEntry.grid(row=1, column=1,sticky="nesw",columnspan=1)
deviceLengthEntry.insert(0,95)

deviceWidthLabel=tk.Label(frame1, text="Device Width (\u03bcm): ",padx=5, pady=5, width=w)
deviceWidthLabel.grid(row=2, column=0,sticky="nesw",columnspan=1)

deviceWidthEntry=tk.Entry(frame1, justify="center", width=w)
deviceWidthEntry.grid(row=2, column=1,sticky="nesw",columnspan=1)
deviceWidthEntry.insert(0,80)

oxideThickLabel=tk.Label(frame1, text="Oxide Thickns' (nm): ",padx=5, pady=5, width=w)
oxideThickLabel.grid(row=3, column=0,sticky="nesw",columnspan=1)

oxideThickEntry=tk.Entry(frame1, justify="center", width=w)
oxideThickEntry.grid(row=3, column=1,sticky="nesw",columnspan=1)
oxideThickEntry.insert(0,300)

oxideDielecLabel=tk.Label(frame1, text="Dielectric Constant: ",padx=5, pady=5, width=w)
oxideDielecLabel.grid(row=4, column=0,sticky="nesw",columnspan=1)

oxideDielecEntry=tk.Entry(frame1, justify="center", width=w)
oxideDielecEntry.grid(row=4, column=1,sticky="nesw",columnspan=1)
oxideDielecEntry.insert(0,3.8)

Radiobutton(frame25,text="Current", height=h, width=w, variable=r, value=0,indicatoron=0, padx=5, pady=5).grid(sticky='nesw',row=0,column=0, columnspan=2)
Radiobutton(frame25,text="Resistance", height=h, width=w, variable=r, value=1, indicatoron=0, padx=5, pady=5).grid(sticky='nesw',row=0,column=2,columnspan=2)

printList=tk.Button(frame3,text="Process Data", height=h, width=w,padx=5, pady=5, command=lambda: itemsFromList(sfu.processData))
printList.grid(row=0, column=0,sticky='nesw',columnspan=2)

exitBut=tk.Button(frame3,text="Average", height=h, width=w, padx=5, pady=5, command=lambda: itemsFromList(sfu.averageData))
exitBut.grid(row=0, column=2,sticky='nesw',columnspan=2)

userSaveNameLabel=tk.Label(frame4, text="User Input:",padx=5, pady=5,height=h, width=w,)
userSaveNameLabel.grid(row=0,column=0,sticky="nesw", columnspan=2)

userSaveNameEntry=tk.Entry(frame4, justify="center", width=w,)
userSaveNameEntry.grid(row=0, column=2,sticky="nesw",columnspan=2)
userSaveNameEntry.insert(0,"Data Name")

exportSelected=tk.Button(frame4,text="Export Select",  height=h,width=w, padx=5, pady=5, command=lambda: itemsFromList(sfu.exportSelectedF))
exportSelected.grid(row=1, column=0,sticky='nesw',columnspan=2)

exportAll=tk.Button(frame4,text="Export All", height=h, width=w, padx=5, pady=5, command=lambda: buttonPress1(sfu.exportALLF))
exportAll.grid(row=1, column=2,sticky='nesw',columnspan=2)

######################
## TKINTER MAINLOOP ##
######################
root.mainloop()