

from writefiles import get_variable_from_file




from pprint import pprint 

# Reads input files
def read_input (filename): 
    
    g = get_variable_from_file(filename)    
    info = g['data']
    
    r = {}
    
    for i in info:
        
        n = {}
        
        n['id'] = i['id']
       
        n['opinions'] = sorted(i['opinions'])   # Sorted to help cache
            
        n['verbatim'] = i['sentence']
        
        n['word_count'] = len((n['verbatim']).split()) # Number of words        
        
        
        
        n['sent'] = {}
        for o in n['opinions']:
            if o[0] not in n['sent']:
                n['sent'][o[0]] = o[1]
            else:
                n['sent'][o[0]] += o[1]
        
        #pprint(n['opinions'])
        #pprint(n['sent'])
        #input()
               
                    
        r[n['id']] = n
    return r
 

