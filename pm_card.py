import json
import config
import json
import os.path

class card :
    def __init__(self, uuid, condition, language, modifications=[]):
        """
        """
        self.uuid = uuid
        #self.name = name
        self.condition = condition
        self.language = language
        self.modifications = modifications

    def move_from_one_to_another(self,from_coll, to_coll):
        """
        """
        from_coll.remove_card_with(self)
        to_coll.add_card_with(self)
        return(True)
    
    