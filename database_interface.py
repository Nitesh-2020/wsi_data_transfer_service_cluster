import pymongo
from datetime import date

# ==============================================================================
# DatabaseInterface
# ==============================================================================


class DatabaseInterface():
    '''
    Interface class to talk to the Mongo database
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
#        no class variables

# |----------------------------------------------------------------------------|
# Constructor
# |----------------------------------------------------------------------------|
    def __init__(self):
        self._mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self._mongo_db = self._mongo_client["data_transfer_status"]

# |---------------------------End of Constructor------------------------------|

# |----------------------------------------------------------------------------|
# insert_slide
# |----------------------------------------------------------------------------|
    def insert_slide(self, slide_name,metadata):
        slide_collection = self._mongo_db["slide_info"]

        slide_data = {
            "slide_name": slide_name,
            "metadata": metadata,
            "status": ''
        }
        slide_collection.insert_one(slide_data)

# |----------------------End of insert_slide-------------------------------------|

# |----------------------------------------------------------------------------|
# slide_exists
# |----------------------------------------------------------------------------|
    def slide_exists(self, slide_name):
        slide_collection = self._mongo_db["slide_info"]

        filter_query = {
            "slide_name": slide_name
        }
        slide_doc_count = slide_collection.find(filter_query).count()
        if slide_doc_count > 0:
            return True
        else:
            return False

# |----------------------End of slide_exists----------------------------------|

# |----------------------------------------------------------------------------|
# delete_slide
# |----------------------------------------------------------------------------|
    def delete_slide(self, slide_name):
        slide_collection = self._mongo_db["slide_info"]

        filter_query = {
            "slide_name": slide_name
        }
        slide_collection.delete_one(filter_query)

# |----------------------End of delete_slide----------------------------------|

# |----------------------------------------------------------------------------|
# fetch_slide
# |----------------------------------------------------------------------------|
    def fetch_slide(self):
        slide_collection = self._mongo_db["slide_info"]
        
        data = {
            '_id': 0,
            'slide_name' : 1,
            'metadata' : 1,
            "status": 1
            }
        
        filter_condition = {
                "$or" : [{
                     "status" : { "$eq" : ''}
                  },
                  {
                       "status" : { "$eq" : 'tarring'}
                  }]
            }
        #slide = slide_collection.find_one({'status':''},filter_query ) 
        slide = slide_collection.find_one(filter_condition,data ) 
        print(slide)
        
        return slide

# |----------------------End of fetch_slide----------------------------------|

# |----------------------------------------------------------------------------|
# update_slide_status
# |----------------------------------------------------------------------------|
    def update_slide_status(self, slide_name,status):
        slide_collection = self._mongo_db["slide_info"]

        filter_query = {
            "slide_name": slide_name
        }
        update_query = {
            "$set": {
                "status": status
            }
        }
        slide_collection.update_one(filter_query, update_query)
        

# |----------------------End of update_slide_status----------------------|


# |----------------------------------------------------------------------------|
# log
# |----------------------------------------------------------------------------|
    def log(self, slide_name,metadata,url,code,url_type):
        today = date.today()
        
        slide_collection = self._mongo_db['log']

        slide_data = {
            "slide_name": slide_name,
            "metadata": metadata,
            "url": url,
            "code":code,
            "date":today.strftime("%d_%b_%Y"),
            "type":url_type
        }
        slide_collection.insert_one(slide_data)

# |----------------------End of insert_slide-------------------------------------|

if __name__ == '__main__':
    obj = DatabaseInterface()
    if obj.slide_exists('Test_129')== False:
        metadata = {
            'x':1,
            'y':2
            }
        obj.insert_slide('Test_129',metadata)
    else:
        print('Slide exits')
    
    obj.update_slide_status('Test_129','tarring')
    
    slide_name =obj.fetch_slide()
    #obj.delete_slide(slide_name['slide_name'])
