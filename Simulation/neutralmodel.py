
import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])


import CompuCellSetup


sim,simthread = CompuCellSetup.getCoreSimulationObjects()
            
# add extra attributes here
        
pyAttributeDictionaryAdder,dictAdder=CompuCellSetup.attachDictionaryToCells(sim)
        
pyAttributeListAdder,listAdder=CompuCellSetup.attachListToCells(sim)
            
CompuCellSetup.initializeSimulationObjects(sim,simthread)
# Definitions of additional Python-managed fields go here
        
#Add Python steppables here
steppableRegistry=CompuCellSetup.getSteppableRegistry()
        

from neutralmodelSteppables import ConstraintInitializerSteppable
ConstraintInitializerSteppableInstance=ConstraintInitializerSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(ConstraintInitializerSteppableInstance)
        

from neutralmodelSteppables import GrowthSteppable
GrowthSteppableInstance=GrowthSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(GrowthSteppableInstance)
        

from neutralmodelSteppables import MitosisSteppable
MitosisSteppableInstance=MitosisSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(MitosisSteppableInstance)
        

from neutralmodelSteppables import DeathSteppable
DeathSteppableInstance=DeathSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(DeathSteppableInstance)
        
from neutralmodelSteppables import ExtraPlotSteppable
ExtraPlotSteppableInstance=ExtraPlotSteppable(sim,_frequency=10)
steppableRegistry.registerSteppable(ExtraPlotSteppableInstance)



CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)        