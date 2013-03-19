
from PySteppables import *
import CompuCell
import sys

from PySteppablesExamples import MitosisSteppableBase
            

class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        for cell in self.cellList:
            cell.targetVolume=25
            cell.lambdaVolume=1.0
        
        

class GrowthSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def step(self,mcs):
        for cell in self.cellList:
            cellNeighborList=self.getCellNeighbors(cell) # generates list of neighbors of cell 'cell'                        totnbr = 0
            count = 0            for nbr in cellNeighborList:                if nbr.neighborAddress:                    totnbr += 1
                    if nbr.neighborAddress.type == 1:                        count += 1            w =  0.5            benefit = 2.0            cost = 1.0#       The first option is just a linear function of the number of neighbours                #        if cell.type==1:    #           f = 1.0 - w + w*(benefit*(count+1.0)/(totnbr+1) - cost)    #        else:    #           f = 1.0 - w + w*(benefit*count/(totnbr+1))#            if count>totnbr/2.0:#       Here is a function with synergy and discounting                        factor = 0.6 # try out values above and below 1
            if cell.type==1:               f = benefit*(1-pow(factor,count))/(1-factor) - cost            else:               f = benefit*(1-pow(factor,count))/(1-factor)                           cell.targetVolume+=f            
#       Now it would be nice to have a function which is actually relevant to the cell environment the idea is as follows #       each cell gets gamma from the nutrient medium#       if a cell is a cooperaor then it donates delta = gamma * 0.1 and gets delta from each of its cooperators #       therefore f = gamma + delta*count - 1)#       and for a defector f = gamma + delta *count#       in this way maybe we can incorporate hte nutrient function in the fitness.#       Also it would be nice if we could control which function to implement from the player menu if that is possible!! (like to choose linear, synergy/disciunting, nutrient etc.)                        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,_simulator,_frequency=1):
        MitosisSteppableBase.__init__(self,_simulator, _frequency)
    
    def step(self,mcs):
        # print "INSIDE MITOSIS STEPPABLE"
        cells_to_divide=[]
        for cell in self.cellList:
            if cell.volume>50:
                
                cells_to_divide.append(cell)
                
        for cell in cells_to_divide:
            self.divideCellRandomOrientation(cell)

    def updateAttributes(self):
        parentCell=self.mitosisSteppable.parentCell
        childCell=self.mitosisSteppable.childCell
        
        parentCell.targetVolume /= 2.0
        
        childCell.targetVolume=parentCell.targetVolume
        childCell.lambdaVolume=parentCell.lambdaVolume
        childCell.type=parentCell.type        
        

class DeathSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def step(self,mcs):
        # kill cell if it is under too much pressure:
        for cell in self.cellList:
            pressure=cell.targetVolume - cell.volume
            if pressure > 100 :
                cell.targetVolume==0
                cell.lambdaVolume==100

class ExtraPlotSteppable(SteppablePy):
    def __init__(self,_simulator,_frequency=10):
        SteppablePy.__init__(self,_frequency)
        self.simulator=_simulator
        self.inventory=self.simulator.getPotts().getCellInventory()
        self.cellList=CellList(self.inventory)

    def start(self):
        import CompuCellSetup  
        self.pW=CompuCellSetup.viewManager.plotManager.getNewPlotWindow()
        if not self.pW:
            return
        #Plot Title - properties           
        self.pW.setTitle("Population dynamics")
        self.pW.setTitleSize(12)
        self.pW.setTitleColor("Black")
        
        #plot background
        self.pW.setPlotBackgroundColor("white")
        
        # properties of x axis
        self.pW.setXAxisTitle("MonteCarlo Step (MCS)")
        self.pW.setXAxisTitleSize(10)      
        self.pW.setXAxisTitleColor("black")              
        
        # properties of y axis
        self.pW.setYAxisTitle("number of cells")        
        # self.pW.setYAxisLogScale()
        # If you use logscale, it will diverge when one of the two types disappears.
        self.pW.setYAxisTitleSize(10)        
        self.pW.setYAxisTitleColor("black")                      
        
        # choices for style are NoCurve,Lines,Sticks,Steps,Dots
        self.pW.addPlot("Cooperators",_style='Lines')
        self.pW.addPlot("Defectors",_style='Lines')
        
        # plot MCS
        self.pW.changePlotProperty("Cooperators","LineWidth",5)
        self.pW.changePlotProperty("Cooperators","LineColor","blue")     
        # plot MCS1
        self.pW.changePlotProperty("Defectors","LineWidth",5)
        self.pW.changePlotProperty("Defectors","LineColor","red")         
        
        self.pW.addGrid()
        self.pW.addAutoLegend("top")
        self.clearFlag=False
    
    
    def step(self,mcs):
        if not self.pW:
            print "To get scientific plots working you need extra packages installed:"
            print "Windows/OSX Users: Make sure you have numpy installed. For instructions please visit www.compucell3d.org/Downloads"
            print "Linux Users: Make sure you have numpy and PyQwt installed. Please consult your linux distributioun manual pages on how to best install those packages"
            return        
        tot=0
        coop=0
        defe=0
        for cell  in  self.cellList:
            tot+=1
            if cell.type == 1: 
                coop += 1
            if cell.type == 2:
                defe += 1
        self.pW.addDataPoint("Cooperators",mcs,coop)
        self.pW.addDataPoint("Defectors",mcs,defe)
            
        self.pW.showAllPlots()

        #Saving plots as PNG's
#         if mcs<50:            
#             qwtPlotWidget=self.pW.getQWTPLotWidget()
#             qwtPlotWidgetSize=qwtPlotWidget.size()
#             # print "pW.size=",self.pW.size()
#             fileName="ExtraPlots_"+str(mcs)+".png"
#             #self.pW.savePlotAsPNG(fileName,qwtPlotWidgetSize.width(),qwtPlotWidgetSize.height()) # here we specify size of the image saved - default is 400 x 400
#             #self.pW.savePlotAsPNG(fileName,1000,1000) # here we specify size of the image saved - default is 400 x 400
