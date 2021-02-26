from os.path import join, exists
from lxml import etree

# ==============================================================================
# XmlReading
# ==============================================================================

class XmlReading():

# |----------------------------------------------------------------------------|
# __init__
# |----------------------------------------------------------------------------|
    def __init__(self):        
        base_path = join("/home", "adminspin","wsi_data_transfer_service")
        self.config_path = join(base_path,'config','cluster_info.xml') 
        
        self.cluster_ip = ''
        self.src_path = '' 
        self.dst_path = ''
        self.tar_type = 0
        
        if self.read_xml_data() is None:
            print('config file is missing in {}'.format(self.config_path))
        
# |----------------------End of __init__--------------------------------------|

# |----------------------------------------------------------------------------|
# read_xml_data
# |----------------------------------------------------------------------------|
    def read_xml_data(self):
        if not(exists(self.config_path)):
            return None
        
        xml_file = etree.parse(self.config_path)
        root_tag = xml_file.getroot()
        
        cluster_ip_tag = root_tag.find("ip")
        
        self.cluster_ip = cluster_ip_tag.attrib["value"]
                
        src_path_tag = root_tag.find("src_path")
        
        self.src_path = src_path_tag.attrib["value"]
        
        dst_path_tag = root_tag.find("dst_path")
        
        self.dst_path = dst_path_tag.attrib["value"]

        tar_type_tag = root_tag.find("tar_type")

        self.tar_type = tar_type_tag.attrib["value"]
        
        return 1
# |----------------------End of read_xml_data--------------------------------------|

# |----------------------------------------------------------------------------|
# get_cluster_ip
# |----------------------------------------------------------------------------|            
    def get_cluster_ip(self):
        return self.cluster_ip
    
# |----------------------End of get_cluster_ip--------------------------------------|
# |----------------------------------------------------------------------------|
# get_src_path
# |----------------------------------------------------------------------------|
    def get_src_path(self):
        return self.src_path
    
# |----------------------End of get_src_path--------------------------------------|
    
# |----------------------------------------------------------------------------|
# get_dst_path
# |----------------------------------------------------------------------------|
    def get_dst_path(self):
        return self.dst_path
    
# |----------------------End of get_dst_path--------------------------------------|

# |----------------------------------------------------------------------------|
# get_tar_type
# |----------------------------------------------------------------------------|
    def get_tar_type(self):
        return self.tar_type
    
# |----------------------End of get_tar_type--------------------------------------|
    
    
    
    
if __name__ == '__main__':
    obj = XmlReading()
    print("cluster ip is {},scanner src path is {},cluster dst path is {}".format(obj.get_cluster_ip(),
                                          obj.get_src_path(),obj.get_dst_path()))
        
