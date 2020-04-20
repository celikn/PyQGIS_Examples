#This part export necessary modules
from qgis.core import (QgsProcessingAlgorithm,
       QgsProcessingParameterNumber,
       QgsProcessingParameterFeatureSource,
       QgsProcessingParameterFeatureSink,
       QgsProcessingParameterString,
       QgsProcessingParameterField)

import processing
from qgis.utils import iface

#This part specify qgis tool input parameters
class algTest(QgsProcessingAlgorithm):
    INPUT_SEARCHKEY='INPUT_SEARCHKEY'
    FIELD_TOSEARCH='FIELD_TOSEARCH'
    OUTPUT_SELECTION = 'OUTPUT_SELECTION'
    INPUT_VECTOR = 'INPUT_VECTOR'
    

    def __init__(self):
        super().__init__()

    def name(self):
        return "Selecting_Feature_With_SearcKey"

    def displayName(self):
        return "Selecting_Feature_With_SearcKey"

    def createInstance(self):
        return type(self)()
    #Initialization of the parameters
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_VECTOR, "Input vector"))
        self.addParameter(QgsProcessingParameterField( self.FIELD_TOSEARCH,'Field to Search Key Value', parentLayerParameterName=self.INPUT_VECTOR, type=QgsProcessingParameterField.Any))
        self.addParameter(QgsProcessingParameterString(
            self.INPUT_SEARCHKEY, "Search Key","C"))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT_SELECTION, "Output selection"))

    def processAlgorithm(self, parameters, context, feedback):
        #The process takes input and search key, and creates buffer for feture containin search key in the attribute "Name"
        FieldNametoSearch=self.parameterAsString(parameters, self.FIELD_TOSEARCH, context)
        Expession=FieldNametoSearch+" LIKE '%"+parameters[self.INPUT_SEARCHKEY]+"%'"
        #'\"Name\" LIKE \'%C%\''
        algresult=processing.run("native:extractbyexpression", {'INPUT':parameters[self.INPUT_VECTOR],'EXPRESSION':Expession,'OUTPUT':parameters[self.OUTPUT_SELECTION]},context=context, feedback=feedback, is_child_algorithm=True)

        selected = algresult['OUTPUT']   
        return {self.OUTPUT_SELECTION:selected}

