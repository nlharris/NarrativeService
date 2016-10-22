import copy

class DataPaletteTypes:
    
    _TYPES = {"KBaseSets.ReadsSet": {}, 
              "KBaseFile.PairedEndLibrary": {},
              "KBaseFile.SingleEndLibrary": {}
              }
    
    _KEYS = frozenset([key for key in _TYPES])
    
    def __init__(self):
        pass
    
    def get(self, type_name):
        ret = self._TYPES.get(type_name)
        if ret is None:
            return None
        return copy.deepcopy(ret)
    
    def keys(self):
        return self._KEYS