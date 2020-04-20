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
    INPUT_BUFFERDIST = 'BUFFERDIST'
    INPUT_SEARCHKEY='INPUT_SEARCHKEY'
    FIELD_TOSEARCH='FIELD_TOSEARCH'
    OUTPUT_BUFFER = 'OUTPUT_BUFFER'
    INPUT_VECTOR = 'INPUT_VECTOR'
    

    def __init__(self):
        super().__init__()

    def name(self):
        return "Buffering_Selected_Feature_With_SearcKey"

    def displayName(self):
        return "Buffering_Selected_Feature_With_SearcKey"

    def createInstance(self):
        return type(self)()
    #Initialization of the parameters
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_VECTOR, "Input vector"))
        self.addParameter(QgsProcessingParameterNumber(
            self.INPUT_BUFFERDIST, "Buffer distance",
            QgsProcessingParameterNumber.Double,
            0.1))
        self.addParameter(QgsProcessingParameterField( self.FIELD_TOSEARCH,'Field to Search Key Value', parentLayerParameterName=self.INPUT_VECTOR, type=QgsProcessingParameterField.Any))
        self.addParameter(QgsProcessingParameterString(
            self.INPUT_SEARCHKEY, "Search Key","C"))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT_BUFFER, "Output buffer"))

    def processAlgorithm(self, parameters, context, feedback):

        FieldNametoSearch=self.parameterAsString(parameters, self.FIELD_TOSEARCH, context)
       
        #The process takes input and search key, and creates buffer for feture containin search key in the attribute "Name"
        
        Expession=FieldNametoSearch+" LIKE '%"+parameters[self.INPUT_SEARCHKEY]+"%'"
        #'\"Name\" LIKE \'%C%\''
        algresult=processing.run("native:extractbyexpression", {'INPUT':parameters[self.INPUT_VECTOR],'EXPRESSION':Expession,'OUTPUT':'TEMPORARY_OUTPUT'})
        selected = algresult['OUTPUT']
        algresult = processing.run("native:buffer", {'INPUT':selected,'DISTANCE':parameters[self.INPUT_BUFFERDIST],'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':True,'OUTPUT':parameters[self.OUTPUT_BUFFER]}, context=context, feedback=feedback, is_child_algorithm=True)
        buffered= algresult['OUTPUT']
        return {self.OUTPUT_BUFFER:buffered}

