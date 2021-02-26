from data_transfer_handler import Upload
import time
import requests
import json
from database_interface import DatabaseInterface
import copy
from service_logger import ServiceLogger

# ==============================================================================
# Sender
# ==============================================================================

class Sender():
	def __init__(self):
		self.joblist =[]
		self.upload_obj = Upload()
		self.dcider_flag = True
		self.database_obj = DatabaseInterface()

# |----------------------------------------------------------------------------|
# job_queue
# |----------------------------------------------------------------------------|
	def job_queue(self,slide,metadata):
		print('job_queue ',slide)
		data = {
			"slide_name":slide,
			"metadata": metadata

		}
		self.joblist.append(data)
		#print(len(self.joblist))

		self.database_obj.log(slide,metadata,'http://localhost:8025/transfer/','200','transfer')		
				
		if self.dcider_flag is True:
			self.dcider_flag = False
			self.decider()
			
# |----------------------End of job_queue-------------------------------|

# |----------------------------------------------------------------------------|
# call_restoration_service
# |----------------------------------------------------------------------------|
	def call_restoration_service(self,slide_folder_name,slide_metadata):
		restoration_service_url = "http://10.20.0.1:8026/restore/{}".\
		format(slide_folder_name)
		print(restoration_service_url)
		print(slide_metadata)
		try:
			resp = requests.post(url=restoration_service_url,
                             data=json.dumps(slide_metadata),
                             timeout=5)

			if resp.status_code == 200:
				ServiceLogger.get().log_info("Request to restore service for "
                                         "slide {} "
                                         "succeeded.".
                                         format(slide_folder_name))
			else:
				ServiceLogger.get().log_info("Request to restore service for "
                                         "slide {}"
                                         "failed with response code: {}.".
                                         format(slide_folder_name,resp.status_code))
			
			self.database_obj.log(slide_folder_name,slide_metadata,restoration_service_url,resp.status_code,'restore')
		except Exception as msg:
			print("Request failed due to: ", msg)
			ServiceLogger.get().log_error("Request to transfer service for slide "
                                      "{} failed due to: {}".
                                      format(slide_folder_name, msg))
			self.database_obj.log(slide_folder_name,slide_metadata,restoration_service_url,'500','restore')

# |----------------------End of call_restoration_service-------------------------|

# |----------------------------------------------------------------------------|
# decider
# |----------------------------------------------------------------------------|
	def decider(self):				
		if(len(self.joblist)>0):
			slide_name = self.joblist[0]["slide_name"]	
			metadata = copy.deepcopy(self.joblist[0]["metadata"])		
			status,error = self.upload_obj.transfer_slide_folder_to_cluster(slide_name,metadata)			
			#time.sleep(10)
			
			print(status)
			#if status is True or error == 'Yes':
			if status is True:
				print("----------Finish-------------------")
				self.call_restoration_service(slide_name,self.joblist[0]["metadata"])
			self.joblist.pop(0)	 
			self.decider()
		else:			
			self.dcider_flag = True
			
# |----------------------End of decider-------------------------------|
			
				

			
