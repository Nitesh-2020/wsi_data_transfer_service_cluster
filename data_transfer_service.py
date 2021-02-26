import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Request,BackgroundTasks
import json

from sender_decider import Sender
from service_logger import ServiceLogger

#wsi_data_transfer_service
# tar -cf, untar -xvf

sender_obj = Sender()

data_transfer_service_app = FastAPI()

# |----------------------------------------------------------------------------|
# service_startup
# |----------------------------------------------------------------------------|

@data_transfer_service_app.on_event("startup")
async def service_startup():
	ServiceLogger.get().initialize("data_transfer")
	


# |----------------------End of service_startup-------------------------------|



@data_transfer_service_app.post("/transfer/{slide_id}")
async def init_service(background_tasks: BackgroundTasks, slide_id : str,
						request: Request):

	print(slide_id)
	request_json = await request.json()	

	ServiceLogger.get().log_debug("Request JSON for slide {}".
                                  format(json.dumps(request_json)))
	
	background_tasks.add_task(sender_obj.job_queue,slide_id,request_json)

	return {"success" : True}



if __name__ == "__main__":
    uvicorn.run(data_transfer_service_app, host="0.0.0.0", port=8025)
