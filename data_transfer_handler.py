import time
import subprocess
import re
from xml_reading import XmlReading
from os.path import join,exists
import os
import requests
from database_interface import DatabaseInterface
import json
from service_logger import ServiceLogger
from tar_data import Tar

# ==============================================================================
# Upload
# ==============================================================================

class Upload():
	def __init__(self):
		readxml_obj = XmlReading()
		self.ip = readxml_obj.get_cluster_ip()
		self.src_path = readxml_obj.get_src_path()
		self.dst_path = readxml_obj.get_dst_path()
		self.tar_type = readxml_obj.get_tar_type()
		self.database_obj = DatabaseInterface()
		self.tar_obj = Tar()

# |----------------------------------------------------------------------------|
# get_folder_size
# |----------------------------------------------------------------------------|
	def get_folder_size(self, folder_path):
		folder_size_content = subprocess.Popen(["du -sh {}".format(folder_path)],
                                  stdout=subprocess.PIPE, shell=True)
		content_list = str(folder_size_content.stdout.read())
		content_list = re.findall(r'([-+]?\d*\.\d+|\d+)(\w+)', content_list)		
		#print("content_list : ", content_list)
		first_tuple = content_list[0]
		folder_size = float(first_tuple[0])
		if "M" in first_tuple:
		    folder_size = folder_size / 1000
		if "K" in first_tuple:
		    folder_size = folder_size / (1000 * 1000)
	    
		print(folder_size)
		 
		return folder_size
            
# |----------------------End of get_folder_size-------------------------------|

# |----------------------------------------------------------------------------|
# update_status_to_node
# |----------------------------------------------------------------------------|
	def update_status_to_node(self,slide_name,slide_metadata,activity_status,error_info):
		basket_status_url = "http://10.20.0.1:1337/basketslot/status/"

		slide_metadata['data'] = {}
		slide_metadata['data']['slide_name'] = slide_name
		slide_metadata['data']['activity_status'] = activity_status
		slide_metadata['data']['error_info'] = error_info

		#print(slide_metadata)
		
		try:
			resp = requests.post(url=basket_status_url,
                             data=json.dumps(slide_metadata),
                             timeout=20)
			if resp.status_code == 200:
				ServiceLogger.get().log_info("Request to node for "
											"folder name {} "
											"succeeded.".
											format(slide_name))
			else:
				ServiceLogger.get().log_info("Request to node for "
											"folder name {} "
											"failed with response code: {}.".
											format(slide_name,resp.status_code))
			self.database_obj.log(slide_name,slide_metadata,basket_status_url,resp.status_code,'node')
		
		except Exception as msg:
			ServiceLogger.get().log_error("Request to node for "
                                      "folder name {} failed due to: {} ".
                                      format( slide_name, msg))
			self.database_obj.log(slide_name,slide_metadata,basket_status_url,'500','node')

# |----------------------End of update_status_to_node-------------------------|

# |----------------------------------------------------------------------------|
# tar_slide_folder
# |----------------------------------------------------------------------------|
	def tar_slide(self,slide_path,slide_name):
		'''
		print('slide_path ',slide_path)
		os.chdir(slide_path)
		tarcmd = "tar -cf {}.tar {}".format(slide_name,slide_name)
		print(tarcmd)
		status = os.system(tarcmd)
		'''
		status = 123
		
		if self.tar_type == '1':
			status = self.tar_obj.tar_slide_folder(slide_path,slide_name)
		elif self.tar_type == '2':
			status = self.tar_obj.tar_complete_slide_folder(slide_path,slide_name)
		elif self.tar_type == '3':
			status = self.tar_obj.tar_grid_folder(slide_path,slide_name)

		return status

# |----------------------End of tar_slide_folder-------------------------|


# |----------------------------------------------------------------------------|
# transfer_slide_folder_to_cluster
# |----------------------------------------------------------------------------|
	def transfer_slide_folder_to_cluster(self, slide_name,metadata):
		move_status = False
		err_msg = ''
		status = 123
		#slide_path =''
		try:
			slide_path = join(self.src_path,slide_name)
			if exists(slide_path) is True:				
				ServiceLogger.get().log_info("*** CALL for tar ***")
				
				self. update_status_to_node(slide_name,metadata,'transfering','')
				tar_status = self.tar_slide(self.src_path,slide_name)
				
				print("Move src_path: ", slide_path, " to: ", self.dst_path)	

				if tar_status == 0:		
				
					command = "sshpass -p 'adminspin#123' rsync -e 'ssh -o \
								StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null' "\
							"-av {} adminspin@{}:{}".format(slide_path, self.ip, self.dst_path)
		
					#print("command: ",command)
					ServiceLogger.get().log_info("rsync command: {}".
												format(command))
		
					startTime = time.time()
					status = os.system(command)
					endTime = time.time()
					total_time = endTime - startTime
					
					folder_size = self.get_folder_size(slide_path)
					
					print("Total time to move {} of size {}GB is: {}".format(slide_path,
					folder_size,
					total_time))
					ServiceLogger.get().log_info("Total time to move {} of size {}GB is: {}".
												format(slide_path,folder_size,total_time))
					
					if status == 0:
						move_status = True
						rmcmd = "rm -rf {} {}".format(slide_path,slide_path)
						#print("rmcmd ",rmcmd)
						ServiceLogger.get().log_info("rsync rmcmd: {}".
												format(rmcmd))
						os.system(rmcmd)
					else:
						move_status = False
						print('Fail to transfer')
						ServiceLogger.get().log_error("Fail to transfer {}".
													format(slide_name))
						self. update_status_to_node(slide_name,metadata,'error','Fail to transfer the data')
				else:
					self. update_status_to_node(slide_name,metadata,'error','Fail to tar the data')
					
			else:
				err_msg ='Yes'
				print("Slide does not exits")
				ServiceLogger.get().log_error("Slide: {} does not exits".
											format(slide_name))

		except Exception as msg:	
			ServiceLogger.get().log_error("exception during transfer slide :{} "
                                      "failed due to: {}".
                                      format(slide_name, msg))
			
		return move_status,err_msg
			
# |----------------------End of transfer_slide_folder_to_cluster-------------------------------|




if __name__ == '__main__':
	obj = Upload()
	#size = obj.transfer_slide_folder_to_cluster('/home/adminspin/wsi_app/acquired_data/2001V301001_1206_1','/datadrive')
	#print("Total size {} GB".format(size))
	obj.transfer_slide_folder_to_cluster('S1_34752','/datadrive')
