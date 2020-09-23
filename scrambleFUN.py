import os
import numpy as np
import matplotlib.pyplot as pp
import pandas as pd

#########################
## INTIALISE VARIABLES ##
#########################

newDesk=[]
selectedList=[]
yPlotlabel=""
flow=["red", "orange","brown","tan", "lime", "purple", "teal", "black", "blue", "grey", "pink", "violet", "goldenrod","darkkhaki","peru", "saddlebrown"]
blues=["blue","turquoise","lime", "darkgreen","midnightblue", "slateblue", "dodgerblue", "mediumblue", "seagreen","yellowgreen","olivedrab","lightseagreen"]
greens=["olive","crimson","black", "blue", "maroon", "lightcoral", "chocolate", "lightsalmon", "darkolivegreen", "rosybrown"]
reds=flow+blues+greens+flow+blues+greens
BODStats=pd.DataFrame()

######################
## DEFINE FUNCTIONS ##
######################

def importData(directory):
    
    os.chdir(directory)
    folderList=os.listdir()
    idvgData=pd.DataFrame() # Initialises a blank dataframe to be appended to 
    newDesk=[] # Initialise a blank list for the data to be selected from
    counter=0

    for folderName in folderList:# Loop over the functionalisation folders
        os.chdir(directory)
        folderList=os.listdir( )# Now list the FOLDERS inside the top directory
        os.chdir(directory+"/"+folderName) # Change directory to the ith folderName 
        fileList=os.listdir() # List the FILES in the folderName FOLDER
        
        for file in fileList:# Loop over the files in the fileList and import them to the dataframe with a new snazzier name 
            fName = directory+"/"+folderName+"/"+file
            df=pd.read_csv(fName, usecols=[1,2], skiprows=248)

            global device
            newTitle,device = newNameFinal(folderName,file)
            df.columns=pd.MultiIndex.from_product([[newTitle],df.columns]) # Introduce multiindex naming of columns
            idvgData=pd.concat([idvgData,df],axis=1)
            newDesk.append(newTitle)
    
    global copied_original
    copied_original=idvgData.copy()
    copied_original.name=device

    return copied_original,device,newDesk

def newNameFinal(folderName1, originalName):
    # Takes a file name and shortens it based on the position of the "_" and then concatenates with the folder name. 

    displayText=originalName[0:originalName.find("_")]
    outputName=folderName1+"_"+displayText

    return outputName, displayText[0:2]

def importBOD(filename):
    # Imports data from a .BOD file (a file which has been previosuly exported from SCRAMBLE)
    
    BODdf=pd.read_csv(filename, header=[0,1])
    
    global copied_original
    copied_original=BODdf.copy()
    
    # Produce a list of the data
    niceCoffee=[]
    for i, x in enumerate(BODdf.columns.get_level_values(0)): 
        if i%2>0: # Select every other name as they are repeated
            niceCoffee.append(x)

    return copied_original,niceCoffee

def statsTable(selection):
    
    bigData=copied_original.copy() # Always work from a copy of the original data

    statsInput=bigData.loc[:,(selection)] # Filter based on name of data
    sVg = statsInput.loc[:,[statsInput.columns[0]]] # Select the Vbg 
    sDrain = statsInput.loc[:,[statsInput.columns[1]]] # Select the Ids

    statsFrame=pd.DataFrame() #Initialise the dataframe for this loop

    ## FORWARD SWEEP STATS ##
    #Slice the data and select the forward sweep
    fVg=sVg.iloc[0:(int(statsInput.shape[0]/2))]  
    fDrain=sDrain.iloc[0:(int(statsInput.shape[0]/2))]    

    #DP Current - fDPI
    fMinI=fDrain.describe().loc["min"]
    statsFrame=pd.concat([statsFrame,fMinI],ignore_index=True)

    #DP Voltage - fDPV
    fMinVIndex=abs(fDrain-fMinI).idxmin()
    fMinV1=fVg.iloc[fMinVIndex].values[0][0]
    fMinV=pd.Series(fMinV1)
    statsFrame=pd.concat([statsFrame,fMinV], ignore_index=True)

    #DP Voltage Gradient - fDPMaxgrad and fDPMaxgradV
    fDPIseries=fDrain[statsInput.columns[1]].values
    fDPVseries=fVg[statsInput.columns[0]].values
    fDPIgrad1=np.gradient(fDPIseries)    
    fDPIgradMax1=max(abs(fDPIgrad1))
    indexGradMax=np.argmax(abs(fDPIgrad1))
    fDPVgradMax1=fDPVseries[indexGradMax]
    fDPIgradMaxI1=fDPIseries[indexGradMax]

    fDPIgradMax=pd.Series(fDPIgradMax1)
    fDPVgradMax=pd.Series(fDPVgradMax1)
    fDPIgradMaxI=pd.Series(fDPIgradMaxI1)

    statsFrame=pd.concat([statsFrame,fDPIgradMax], ignore_index=True)
    statsFrame=pd.concat([statsFrame,fDPVgradMax], ignore_index=True)
    statsFrame=pd.concat([statsFrame,fDPIgradMaxI], ignore_index=True)
    
    #Current value at 0 BackGate - fI0Vg
    fI0Vg1=fDrain.iloc[int(((fDrain.shape[0])-1)/2)].values[0] # Halfway point
    fI0Vg=pd.Series(fI0Vg1)
    statsFrame=pd.concat([statsFrame,fI0Vg], ignore_index=True)
    
    ## REVERSE SWEEP STATS ##
    #Slice the data and select the reverse sweep
    rVg=sVg.iloc[(int(statsInput.shape[0]/2)):]
    rDrain=sDrain.iloc[(int(statsInput.shape[0]/2)):] 

    #DP Current - rDPI
    rMinI=rDrain.describe().loc["min"]
    statsFrame=pd.concat([statsFrame,rMinI],ignore_index=True)

    #DP Voltage - rDPV
    rMinVIndex=abs(rDrain-rMinI).idxmin()
    rMinV1=sVg.iloc[rMinVIndex].values[0][0]
    rMinV=pd.Series(rMinV1)
    statsFrame=pd.concat([statsFrame,rMinV], ignore_index=True)

    #DP Voltage Gradient - rDPMaxgrad and rDPMaxgradV
    rDPIseries=rDrain[statsInput.columns[1]].values
    rDPVseries=rVg[statsInput.columns[0]].values
    rDPIgrad1=np.gradient(rDPIseries)    
    rDPIgradMax1=max(abs(rDPIgrad1))
    indexGradMax=np.argmax(abs(rDPIgrad1))
    rDPVgradMax1=rDPVseries[indexGradMax]
    rDPIgradMaxI1=rDPIseries[indexGradMax]

    rDPIgradMax=pd.Series(rDPIgradMax1)
    rDPVgradMax=pd.Series(rDPVgradMax1)
    rDPIgradMaxI=pd.Series(rDPIgradMaxI1)

    statsFrame=pd.concat([statsFrame,rDPIgradMax], ignore_index=True)
    statsFrame=pd.concat([statsFrame,rDPVgradMax], ignore_index=True)
    statsFrame=pd.concat([statsFrame,rDPIgradMaxI], ignore_index=True)

    #Current value at 0 BackGate - fI0Vg
    rI0Vg1=rDrain.iloc[int(((rDrain.shape[0])-1)/2)].values[0]
    rI0Vg=pd.Series(rI0Vg1)
    statsFrame=pd.concat([statsFrame,rI0Vg], ignore_index=True)
    
    ## CONSTRUCT THE PARAMETER TABLE ##

    insides = {'Column 1'     : [1,2,3,4,5,6,30,40,50,60,70,80],
                'Index Title'  : ["fDPI","fDPV","fMaxgrad","fMaxgradV", "fMaxgradI", "fI0Vg",
                                  "rDPI","rDPV","rMaxgrad","rMaxgradV","rMaxgradI", "rI0Vg"]}
    blankStats = pd.DataFrame(insides)
    del blankStats["Column 1"]
    blankStats.index.name = "BOD_Params"
    newFrame=pd.concat([blankStats,statsFrame], axis=1) #Concatenate the initial df with data from statsFrame
    newFrame.index = newFrame["Index Title"]
    del newFrame["Index Title"]
    newFrame.columns=[selection]
    newFrame.index.name="BOD_Params"
    
    return newFrame #Output from StatsTable

def mobility(selection,Vds,L,W,oxideThick,oxideDielectric):
    
    bigData=copied_original.copy() # Always work from a copy of the original data
    mobilitySeries=pd.Series([]) # Convert dataframe to series for ease of maniupulation
    mobilityFrame=pd.DataFrame() #Initialise the dataframe for this sweep
    
    mobilityInput=bigData.loc[:,(selection)] # Filter based on name of data
    mVg = mobilityInput.loc[:,[mobilityInput.columns[0]]] # Select the Vg
    mDrain = mobilityInput.loc[:,[mobilityInput.columns[1]]] # Select the Ids 
    mDrainSeries=mDrain[mobilityInput.columns[1]].values 
    mVgSeries=mVg[mobilityInput.columns[0]].values
    mGradient=np.gradient(mDrainSeries) # Use the gradient function on the Ids data
    
    L=L
    W=W
    Cg=((8.854*(10**-12))*(oxideDielectric))/(oxideThick) # Calculate Cg from user parameters 
    
    # Equation below calculates the mobility
    mobilitySeries=abs((mGradient*L)/(W*Vds*Cg))*100*100 # Multiplication of *100*100 used convert end result into units of cm^2
    
    # Convert series into a dataframe to ease concatenation and plotting
    mobilityFrame=pd.DataFrame(data=mobilitySeries, index=mVgSeries)
    mobilityFrame.index=range(0,mobilityFrame.shape[0],1)
    mobilityFrame=pd.concat([mVg,mobilityFrame], axis=1,ignore_index=False)
    mobilityFrame.columns = [mobilityInput.columns[0],"Mobilities"]
    mobilityFrame.columns=pd.MultiIndex.from_product([[selection],mobilityFrame.columns])

    ## FORWARD & REVERSE SWEEP STATS ##
    
    statsInput=bigData.loc[:,(selection)] 
    sVg = statsInput.loc[:,[statsInput.columns[0]]] #statsInput.columns[0]
    sDrain = statsInput.loc[:,[statsInput.columns[1]]]
    fVg=sVg.iloc[0:(int(statsInput.shape[0]/2))]
    fDrain=sDrain.iloc[0:(int(statsInput.shape[0]/2))]    
    fMinI=fDrain.describe().loc["min"]
    fMinVIndex=abs(fDrain-fMinI).idxmin()
    rVg=sVg.iloc[(int(statsInput.shape[0]/2)):]
    rDrain=sDrain.iloc[(int(statsInput.shape[0]/2)):] 
    rMinI=rDrain.describe().loc["min"]
    rMinVIndex=abs(rDrain-rMinI).idxmin()

    fPoint=fMinVIndex.values[0]
    rPoint=rMinVIndex.values[0]
    
    return (fPoint, rPoint, mobilitySeries, mobilityFrame)
 
def processData(selectedList,Vds,deviceL,deviceW,oxideThick,oxideDielectric, mouse):
    
    ## INITIALISE VARIABLES BELOW ##
    BODStats=pd.DataFrame()
    BODMobility=pd.DataFrame()
    BODMobListFwd=[]
    BODMobListRev=[]
    L=deviceL
    W=deviceW
    labelSize="xx-small"
    fontSize="x-small"
    textBox=dict(boxstyle='round', facecolor='wheat')
    pp.close("all")


    ## INITIALISE SWEEP VISUALISATION PLOT ##
    if len (selectedList)>0:        
        fig,ax1=pp.subplots(1,1) #NewLine
        ax1.set_xlabel("$V_{bg}$ (V)", fontsize=fontSize)

    for index, selection in enumerate (selectedList): 
        # Filter the data based on widget inputs
        bigData=copied_original.copy()
        smallData1 = bigData.loc[:,(selection)] # Filter based on name of data
        vBg=smallData1.iloc[:,0] # Select the Vbg
        iDrain=smallData1.iloc[:,1] # Select the Ids
    
        # Decide if the user wants to plot as Current or Resistance
        if mouse == 0: # Plot as Current
            yPlotlabel="$I_{sd}$ (A)"
            yPlotValue=iDrain
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        elif mouse == 1: # Plot as Resistance
            yPlotlabel="Resistance ($\Omega$)"
            yPlotValue= (Vds)/iDrain # Calculate the Resistance

            if index==0: # Initialise a secondary axis to plot the Sheet Resistance 
                ax2 = ax1.twinx()
                ax2.tick_params(axis="y", labelsize=labelSize)

        # Finalise  the axis parameters
        ax1.set_ylabel(yPlotlabel, fontsize=fontSize)
        ax1.tick_params(axis="both", labelsize=labelSize)

        # Plot the data       
        color=reds[index]
        if mouse == 1:
            ax2.plot(vBg,yPlotValue*(W/L), color=color, linewidth=0.5, marker = "o", markersize=1)
            ax2.set_ylabel('Sheet Resistance ($\Omega$/Sqaure)', color="blue",fontsize=fontSize)
            ax2.tick_params(axis='y', labelcolor="blue")
        ax1.plot(vBg, yPlotValue, color=color, label=selection, linewidth=0.5, marker = "o", markersize=1)
        ax1.legend(fancybox=True,fontsize="medium")

        
        ## CONSTRUCT DATAFRAMES FOR MOBILITIES AND PARAMETER DETAILS PLOTS ##
        # Call the Stats Table Function Here to Build the BOD_Parameters Dataframe
        newFrame=statsTable(selection)
        frameToAdd=newFrame
        BODStats=pd.concat([BODStats,frameToAdd], axis=1)
        
        # Call the Mobility Function Here to Build the BOD_Mobilities Dataframe
        (FWD,REV,mS,mF)=mobility(selection,Vds,L,W,oxideThick,oxideDielectric)
        BODMobility=pd.concat([BODMobility,mF], axis=1)
        BODMobListFwd.append(FWD)
        BODMobListRev.append(REV)
    
    ## COMPLETE PLOTTING MOBILITIES AND PARAMETER DETAILS BELOW ##
    if len(selectedList)>0:
        # Rename the stages to shorten them 
        shortNames=[]
        fourCharacterNames=[]
        for items in selectedList:
            if items.find("_")==1 or items.find("_")==2: # Then the user has numbered folders as per SCRAMBLES instructions
                firstOccurence=items.find("_")
                secondOccurence=items.find("_",firstOccurence+1)
                if secondOccurence-firstOccurence<5: # Then the foldername is less than 4 characters long
                    shortNames.append(items[firstOccurence+1:secondOccurence])
                    fourCharacterNames.append(items[firstOccurence+1:secondOccurence])
                else:
                    shortNames.append(items[firstOccurence+1:])
                    fourCharacterNames.append(items[firstOccurence+1:firstOccurence+5])    
            else:
                shortNames.append(items[:4])
                fourCharacterNames.append(items[0:4])
    
        # Collect Data from BOD_Parameters table 
        fDPI=list(BODStats.iloc[0])
        fDPV=list(BODStats.iloc[1])
        fDPMaxgrad=list(BODStats.iloc[2])
        fDPMaxgradV=list(BODStats.iloc[3])
        fDPMaxgradI=list(BODStats.iloc[4])
        fI0Vg=list(BODStats.iloc[5])
        rDPI=list(BODStats.iloc[6])
        rDPV=list(BODStats.iloc[7])
        rDPMaxgrad=list(BODStats.iloc[8])
        rDPMaxgradV=list(BODStats.iloc[9])
        rDPMaxgradI=list(BODStats.iloc[10])
        rI0Vg=list(BODStats.iloc[11])

        # Initialise Plots
        figStats,axStats=pp.subplots(3,2) #RightFrame - Parameter Details
        figStatsL,axStatsL=pp.subplots(1,3) #MiddleBFrame - Mobilities
        
        ## PLOT MOBILITIES ##
        for selection, color, f, re in zip(selectedList, reds, BODMobListFwd, BODMobListRev):
            filteredMob=BODMobility.loc[:,[selection]]
            mobilityPlot = filteredMob.iloc[:,1].values
            vPlot = filteredMob.iloc[:,0].values
            axStatsL[0].plot(vPlot[:f],mobilityPlot[:f], color=color, marker="|", linewidth=0) 
            axStatsL[0].plot(vPlot[f:re],mobilityPlot[f:re], color=color, marker="_",linewidth=0)
            axStatsL[0].plot(vPlot[re:],mobilityPlot[re:], color=color, marker="|",linewidth=0)
            holes=np.concatenate([mobilityPlot[:f],mobilityPlot[re:]])
            axStatsL[1].hist(holes,bins=10, color=color, alpha=0.5, rwidth=0.6)
            electrons=mobilityPlot[f:re]
            axStatsL[2].hist(electrons,bins=10, color=color, alpha=0.5, rwidth=0.6)
        
        # Finalise the axes parameters for the Sweep Visualisation Plot
        axStatsL[0].set_xlabel("$V_{bg}$ (V)", fontsize=fontSize)
        axStatsL[0].set_ylabel("$\mu$ ($cm^2 V^{-1} s^{-1}$)", fontsize=fontSize)
        axStatsL[0].tick_params(axis="both", labelsize=labelSize)
        axStatsL[1].set_xlabel("Hole $\mu$ ($cm^2 V^{-1} s^{-1}$)", fontsize=fontSize)
        axStatsL[1].set_ylabel("Frequency", fontsize=fontSize)
        axStatsL[1].tick_params(axis="both", labelsize=labelSize)
        axStatsL[2].set_xlabel("Electron $\mu$ ($cm^2 V^{-1} s^{-1}$)",fontsize=fontSize)
        axStatsL[2].set_ylabel("Frequency", fontsize=fontSize)
        axStatsL[2].tick_params(axis="both", labelsize=labelSize)
        
        
        ## PLOT PARAMETER DETAILS ##
        for q,w,e,r, k,l, x, y, i,j, color, selection in zip(fDPMaxgradV, fDPMaxgradI, rDPMaxgradV, rDPMaxgradI,fI0Vg, rI0Vg,fDPV, fDPI, rDPV, rDPI,reds, shortNames):
            
            # Below if/elif decides plotting behaviour for current or resistance visulaisation and also
            # overlays the Dirac points and Max Transconductance to the Sweep Visualisation Plot            
            if mouse == 0:
                ax1.plot(x,y,marker=">", color=color,   markersize=10)
                ax1.plot(i,j,marker="<", color=color,  markersize=10)
                ax1.plot(q,w,marker=">", color=color,  markerfacecolor="none", markersize=10)
                ax1.plot(e,r,marker="<", color=color, markerfacecolor="none", markersize=10)

                axStats[0,0].scatter(x,y,marker=">", color=color, label=selection)
                axStats[0,0].scatter(i,j,marker="<", color=color)

                axStats[0,1].scatter(selection,k,marker=">",color=color)
                axStats[0,1].scatter(selection,l,marker="<",color=color)
                axStats[0,1].annotate(**defineInsides(k,l,selection,"vE")[1],bbox=textBox)
                axStats[0,1].vlines(**defineInsides(k,l,selection,"vE")[0])

                axStats[2,0].scatter(selection,y,marker=">", color=color)
                axStats[2,0].scatter(selection,j,marker="<", color=color)
                axStats[2,0].annotate(**defineInsides(y,j,selection,"vE")[1],bbox=textBox)
                axStats[2,0].vlines(**(defineInsides(y,j,selection,"vE")[0]))
                    
                axStats[2,1].scatter(selection,w,color=color,marker="$\u25BB$")
                axStats[2,1].scatter(selection,r,color=color,marker="$\u25C5$")
                axStats[2,1].annotate(**defineInsides(w,r,selection,"vE")[1],bbox=textBox)
                axStats[2,1].vlines(**defineInsides(w,r,selection,"vE")[0])

            elif mouse==1:
                ax1.plot(x,Vds/y,marker=">", color=color,   markersize=10)
                ax1.plot(i,Vds/j,marker="<", color=color,  markersize=10)
                ax1.plot(q,Vds/w,marker=">", color=color,  markerfacecolor="none", markersize=10)
                ax1.plot(e,Vds/r,marker="<", color=color, markerfacecolor="none", markersize=10) 

                axStats[0,0].scatter(x,Vds/y,marker=">", color=color, label=selection)
                axStats[0,0].scatter(i,Vds/j,marker="<", color=color)

                axStats[0,1].scatter(selection,Vds/k,marker=">",color=color)
                axStats[0,1].scatter(selection,Vds/l,marker="<",color=color)
                axStats[0,1].annotate(**defineInsides(Vds/k,Vds/l,selection,"vP")[1],bbox=textBox)
                axStats[0,1].vlines(**defineInsides(Vds/k,Vds/l,selection,"vP")[0])

                axStats[2,0].scatter(selection,Vds/y,marker=">", color=color)
                axStats[2,0].scatter(selection,Vds/j,marker="<", color=color)
                axStats[2,0].annotate(**defineInsides(Vds/y,Vds/j,selection,"vP")[1],bbox=textBox)
                axStats[2,0].vlines(**(defineInsides(Vds/y,Vds/j,selection,"vP")[0]))
                    
                axStats[2,1].scatter(selection,Vds/w,color=color,marker="$\u25BB$")
                axStats[2,1].scatter(selection,Vds/r,color=color,marker="$\u25C5$")
                axStats[2,1].annotate(**defineInsides(Vds/w,Vds/r,selection,"vP")[1],bbox=textBox)
                axStats[2,1].vlines(**defineInsides(Vds/w,Vds/r,selection,"vP")[0])

            axStats[1,1].scatter(q,selection,color=color,marker="$\u25BB$")
            axStats[1,1].scatter(e,selection,color=color,marker="$\u25C5$")
            axStats[1,1].annotate(**defineInsides(q,e,selection,"hE")[1],bbox=textBox)
            axStats[1,1].hlines(**defineInsides(q,e,selection,"hE")[0])

            axStats[1,0].scatter(x,selection,marker=">", color=color)
            axStats[1,0].scatter(i,selection,marker="<", color=color)
            axStats[1,0].annotate(**defineInsides(x,i,selection,"hE")[1],bbox=textBox)
            axStats[1,0].hlines(**(defineInsides(x,i,selection,"hE")[0]))

        # Below if/elif decides axes behaviour depending on current or resistance visulaisation
        if mouse == 0:
            axStats[0,0].set_ylabel("$I_{sd}$ (A)",fontsize=fontSize)
            axStats[0,0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            axStats[0,0].set_ylim([0.96*min(min(fDPI),min(rDPI)),1.04*max(max(fDPI),max(rDPI))])
            axStats[0,0].set_xlim([0.96*min(min(fDPV),min(rDPV)),1.04*max(max(fDPV),max(rDPV))])

            axStats[0,1].set_ylabel("$I_{sd}$ (A)",fontsize=fontSize)
            axStats[0,1].set_ylim([0.96*min(min(fI0Vg),min(rI0Vg)),1.04*max(max(fI0Vg),max(rI0Vg))])
            axStats[0,1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            axStats[0,1].set_title('$I_{sd}$ @ $V_{bg}$=0',fontsize= "small",loc='right')

            axStats[2,0].set_ylabel("$I_{sd}$ (A)",fontsize=fontSize)
            axStats[2,0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            axStats[2,0].set_ylim([0.96*min(min(fDPI),min(rDPI)),1.04*max(max(fDPI),max(rDPI))])
            axStats[2,0].set_title('Dirac Point Currents',fontsize= "small", loc='right')

            axStats[2,1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            axStats[2,1].set_ylabel("$I_{sd}$ (A)",fontsize=fontSize)
            axStats[2,1].set_ylim([0.96*min(min(fDPMaxgradI),min(rDPMaxgradI)),1.04*max(max(fDPMaxgradI),max(rDPMaxgradI))])
            axStats[2,1].set_title('Max Trans. Currents',fontsize= "small",  loc='right')

        elif mouse ==1:
            axStats[0,0].set_ylabel("$R_{sd}$ ($\Omega$)",fontsize=fontSize)
            axStats[0,0].ticklabel_format(style='plain', axis='y', scilimits=(0,0))
            axStats[0,0].set_ylim([0.96*min(Vds/max(fDPI),Vds/max(rDPI)),1.04*max(Vds/min(fDPI),Vds/min(rDPI))])
            axStats[0,0].set_xlim([0.96*min(min(fDPV),min(rDPV)),1.04*max(max(fDPV),max(rDPV))])

            axStats[0,1].set_ylabel("$R_{sd}$ ($\Omega$)",fontsize=fontSize)
            axStats[0,1].set_ylim([0.96*min(Vds/max(fI0Vg),Vds/max(rI0Vg)),1.04*max(Vds/min(fI0Vg),Vds/min(rI0Vg))])
            axStats[0,1].ticklabel_format(style='plain', axis='y', scilimits=(0,0))
            axStats[0,1].set_title('$R_{sd}$ @ $V_{bg}$=0',fontsize= "small",loc='right') 
        
            axStats[2,0].set_ylabel("$R_{sd}$ ($\Omega$)",fontsize=fontSize)
            axStats[2,0].ticklabel_format(style='plain', axis='y', scilimits=(0,0))
            axStats[2,0].set_ylim([0.96*min(Vds/max(fDPI),Vds/max(rDPI)),1.04*max(Vds/min(fDPI),Vds/min(rDPI))])
            axStats[2,0].set_title('Dirac Point Resistances',fontsize= "small", loc='right')

            axStats[2,1].ticklabel_format(style='plain', axis='y', scilimits=(0,0))
            axStats[2,1].set_ylabel("$R_{sd}$ ($\Omega$)",fontsize=fontSize)
            axStats[2,1].set_ylim([0.96*min(Vds/max(fDPMaxgradI),Vds/max(rDPMaxgradI)),1.04*max(Vds/min(fDPMaxgradI),Vds/min(rDPMaxgradI))])
            axStats[2,1].set_title('Max Trans. Resistances',fontsize= "small",  loc='right')
        
        # Finalise the axes parameters for the Parameter Details plot
        axStats[0,0].set_title('Dirac Points',fontsize= "small",loc='right')
        axStats[0,0].set_xlabel("$V_{bg}$ (V)",fontsize=fontSize)
        axStats[0,0].tick_params(axis="both", labelsize=labelSize)
        
        axStats[0,1].set_xticklabels(fourCharacterNames, rotation=45, fontsize="xx-small")
        axStats[0,1].tick_params(axis="both", labelsize=labelSize)

        axStats[1,0].set_title('Dirac Point Voltages',fontsize= "small", loc='right')
        axStats[1,0].set_yticklabels(fourCharacterNames, rotation=45, fontsize="xx-small")
        axStats[1,0].set_xlabel("$V_{bg}$ (V)",fontsize=fontSize)
        axStats[1,0].tick_params(axis="both", labelsize=labelSize)
        
        axStats[1,1].set_title('Max Trans. Voltages',fontsize= "small", loc='right')
        axStats[1,1].set_xlabel("$V_{bg}$ (V)",fontsize=fontSize)
        axStats[1,1].set_yticklabels(fourCharacterNames, rotation=45, fontsize="xx-small")
        axStats[1,1].set_facecolor("#f5f5f5")
        axStats[1,1].tick_params(axis="both", labelsize=labelSize)

        axStats[2,0].set_xticklabels(fourCharacterNames, rotation=45, fontsize="xx-small")
        axStats[2,0].tick_params(axis="both", labelsize=labelSize)

        axStats[2,1].set_xticklabels(fourCharacterNames, rotation=45, fontsize="xx-small")
        axStats[2,1].set_facecolor("#f5f5f5")
        axStats[2,1].tick_params(axis="both", labelsize=labelSize)

    # Reposition the plots with respect to their white space before passing to front GUI
    figStatsL.subplots_adjust(left  = 0.10, right = 0.99,bottom = 0.16, top = 0.99, wspace = 0.28)    
    figStats.subplots_adjust(top=0.95,bottom=0.06,left=0.09,right=0.94,hspace=0.57,wspace=0.28)
    if mouse == 1:
        fig.subplots_adjust(left=0.09, bottom=0.16, right=0.91, top=0.93)
    else:
        fig.subplots_adjust(left=0.09, bottom=0.16, right=0.99, top=0.93)

    return fig, figStats,figStatsL

def averageData(selectedList,userName):
    
    ## INITIALISE VARIABLES ##
    BODAverage=pd.DataFrame()
    lovelyOldToad=[]

    # Filter the dataframe with the entries in the selectedList
    global copied_original
    bigData=copied_original
    fdf=bigData.loc[:,selectedList]
    # Get column for back gate values
    vBG=fdf.iloc[:,0]
    # Get columns for current
    iDrains=fdf.xs(fdf.columns[1][1],axis=1,level=1,drop_level=False)
    averageIDrain=iDrains.mean(axis=1)
    # Concatenate the two columns together
    BODAverage=pd.concat([vBG,averageIDrain],axis=1)
    # Rename the columns so that it can be read by legacy data visualisation
    BODAverage.columns=[fdf.columns[0][1],fdf.columns[1][1]]
    # Add the multicolumn level so that it can be found in the list
    newName=selectedList[0][:selectedList[0].find("_")+1]+userName+"_"+"AVE" #Append AVE so users know this has been edited
    BODAverage.columns=pd.MultiIndex.from_product([[newName],BODAverage.columns])
    # Concatenate to the copied_original database
    copied_original=pd.concat([copied_original,BODAverage],axis=1)
    # Now get a list of headers to display in the Datalist
    for x in copied_original.columns.get_level_values(0):
        if x not in lovelyOldToad:
            lovelyOldToad.append(x)
    
    return(lovelyOldToad)

def exportSelectedF(selectedList,Vds,L,W,oxideThick,oxideDielectric):
    
    ## INITIALISE VARIABLES ##
    BODExportSelect=pd.DataFrame()
    BODStats1=pd.DataFrame()
    BODMobility1=pd.DataFrame()
    
    if len (selectedList)>0:
        for selection in selectedList: 
            
            # Section to export Data
            bigData=copied_original.copy()
            smallData1 = bigData.loc[:,(selection)]
            smallData1.columns=pd.MultiIndex.from_product([[selection],smallData1.columns])        
            BODExportSelect=pd.concat([BODExportSelect,smallData1],axis=1)

            # Section to export the Parameters
            newFrame1=statsTable(selection)
            rFrame=Vds/(newFrame1.iloc[[0,4,5,6,10,11],:]) # Add in the Parameters for Resistance space
            rFrame.index=['fDPR', 'fMaxgradR','fR0Vg', 'rDPR', 'rMaxgradR','rR0Vg']
            newFrame1=pd.concat([newFrame1,rFrame],axis=0)
            frameToAdd1=newFrame1
            BODStats1=pd.concat([BODStats1,frameToAdd1], axis=1)
            BODStats1.index.name="BOD_Params"
            
            # Section to export the Mobilities
            _,_,_,newFrameMob1=mobility(selection,Vds,L,W,oxideThick,oxideDielectric)
            BODMobility1=pd.concat([BODMobility1,newFrameMob1], axis=1,ignore_index=False)

        return BODExportSelect,BODStats1,BODMobility1

def exportALLF():
    return copied_original

def defineInsides(x,y,selection,HorV): 
    # This function determines the label and line colours for all plots in the Parameter Details
    
    if HorV == "hE":
        if x < y:
            insidesLines={"y":selection,"xmin":x,"xmax":y,"color":"red","zorder":0}
            insidesText={"s":"{:.0f}".format(abs(x-y)),"xy":(((x+y)/2),selection),"textcoords":"offset points","xytext":(0,5), "color":"red", "fontsize":"xx-small"}
        elif x > y:
            insidesLines={"y":selection,"xmin":y,"xmax":x,"color":"black","zorder":0}
            insidesText={"s":"{:.0f}".format(abs(x-y)),"xy":(((x+y)/2),selection),"textcoords":"offset points","xytext":(0,5), "color":"black", "fontsize":"xx-small"}
        else:
            insidesLines={"y":selection,"xmin":y,"xmax":x,"color":"black","zorder":0, "linestyle":"None"}
            insidesText={"xy":(((x+y)/2),selection),"s":""} 

    if HorV[0] =="v":
        if x < y:
            insidesLines={"x":selection,"ymin":x,"ymax":y,"color":"red","zorder":0}
            if HorV[1] == "E":
                insidesText={"s":"{:.1e}".format(abs(x-y)),"xy":(selection,((x+y)/2)),"textcoords":"offset points","xytext":(5,0), "color":"red", "fontsize":"xx-small"}
            elif HorV[1] == "P":
                insidesText={"s":"{:.0f}".format(abs(x-y)),"xy":(selection,((x+y)/2)),"textcoords":"offset points","xytext":(5,0), "color":"red", "fontsize":"xx-small"}
                
        elif x > y:
            insidesLines={"x":selection,"ymin":y,"ymax":x,"color":"black","zorder":0}
            if HorV[1] == "E":
                insidesText={"s":"{:.1e}".format(abs(x-y)),"xy":(selection,((x+y)/2)),"textcoords":"offset points","xytext":(5,0), "color":"black", "fontsize":"xx-small"}
            if HorV[1] == "P":
                insidesText={"s":"{:.0f}".format(abs(x-y)),"xy":(selection,((x+y)/2)),"textcoords":"offset points","xytext":(5,0), "color":"black", "fontsize":"xx-small"}
 
        else:
            insidesLines={"x":selection,"ymin":y,"ymax":x,"color":"black","zorder":0, "linestyle":"None"}
            insidesText={"xy":(selection,((x+y)/2)),"s":""}    

    return insidesLines,insidesText

#############################
## TESTING CONDUCTED BELOW ##
#############################

if __name__=="__main__":
    # Testing is conducted down here...
    # print("Running test code inside the module")
    pass # Uncomment this if no testing is required