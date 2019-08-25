# <------------------------>
# <-----> PAR <----->
# <------------------------>

SUMLEN = None # Summary length (number of sentences on each side). Set 'None' for automatic.

MAX_WORDS = 2*100

#PAR = dict()
LANGUAGE = 'portuguese'
LAMBDA = '0.5'
METHOD = 'CF' 
CENTROIDS_AS_SUMMARY = 'False'
USE_HUNGARIAN_METHOD = 'False'
ALLOW_REPETITION = False


DATASET_ID = 8


ASPECTS_TAGS = ['none', 'join', 'only'][0]



# Products IDs 
#SOURCE1 = '10'    
#SOURCE2 = '11'   

SOURCE1, SOURCE2= [ (), ('D1a','D1b'), ('D2a','D2b'), ('D3a','D3b'), ('D4a','D4b'), ('D5a','D5b'), ('D6a','D6b'), ('D7a','D7b'), ('D8a','D8b')][DATASET_ID]


SIZE_FAC = {}
SIZE_FAC['none'] = {}
SIZE_FAC['none']['CF'] = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
SIZE_FAC['none']['RF'] = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
SIZE_FAC['join'] = {}
SIZE_FAC['join']['CF'] = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
SIZE_FAC['join']['RF'] = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
SIZE_FAC['only'] = {}
SIZE_FAC['only']['CF'] = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
SIZE_FAC['only']['RF'] = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]


#PAR['ASPECT'] = 'short'
#ASPECT = PAR['ASPECT']

#if ASPECT != '':
    #FILENAME1 = SOURCE1+'-'+ASPECT
    #FILENAME2 = SOURCE2+'-'+ASPECT
#else:
    #FILENAME1 = SOURCE1
    #FILENAME2 = SOURCE2

DATAPATH = '../input'

#PAR[SOURCE1] = PAR['DATAPATH'] + '/' + ASPECT + '_' + PAR['ID1'] + '.txt'
#PAR[SOURCE2] = PAR['DATAPATH'] + '/' + ASPECT + '_' + PAR['ID2'] + '.txt'


SHOW_SUMMARY = False
SHOW_EVALUATION = True
SHOW_INDEXES = False



#DATA_DIR = PAR['DATAPATH']
# Get full path for the file with data of target 
def filepath(target):
    #if ASPECT == '':
        #return DATA_DIR+'/'+target+'.json'  
    #else:
        #return DATA_DIR+'/'+target+'-'+ASPECT+'.json'
    return DATAPATH +'/'+target+'.json'


#PAR = dict()
#PAR['LANGUAGE'] = LANGUAGE

#PAR['ALLOW_REPETITION'] = ALLOW_REPETITION
