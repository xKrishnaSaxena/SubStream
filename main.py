from fastapi import FastAPI,UploadFile,Form
from fastapi.responses import FileResponse
from typing import Annotated
import tempfile
import os
import uuid

app = FastAPI()

languages_available= [ "english" , "hindi" , "hinglish" ]

status_map={}
file_map={}

def generate_uuid():
    new_uuid=uuid.uuid4()
    return str(new_uuid)

def pipeline(file_path:str,lang_mode:str,job_id:str):
    status_map[job_id]="Pipeline Started"
    print(status_map[job_id])
    print("File Path: ",file_path)
    print("Lang Mode: ",lang_mode)
    print("Job Id: ",job_id)
    status_map[job_id]="Completed"
    #TODO
    #Update the file_map with the new file
    return 

@app.get("/")
def greet():
    return {"Hello from SubStream's API!"}

@app.post("/process-video")
async def process_video(file:UploadFile , lang_mode:Annotated[str,Form()]):
    if lang_mode not in languages_available:
        return {"Sorry! Language not available currently!"}
    job_id=generate_uuid()
    status_map[job_id]="Started"
    print(status_map[job_id])
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path=os.path.join(temp_dir,file.filename)

        with open(temp_file_path,"wb")as temp_file:
            content=await file.read()
            temp_file.write(content)
        file_map[job_id]=temp_file_path
        status_map[job_id]="Processing File Content"
        print(status_map[job_id])
        pipeline(temp_file_path,lang_mode,job_id)
    
    return {"job_id":job_id}


@app.get("/status/{job_id}")
def get_status(job_id:str):
    if(job_id not in status_map):
        return {"Job Id Not Found"}
    status=status_map[job_id]
    return {"Status":status}

@app.get("/download/{job_id}")
async def download_video(job_id:str):
    video_path=file_map[job_id]
    if(job_id not in file_map):
        return {"Job Id Not Found"}
    if(status_map[job_id] != "Completed"):
        return {"Job not done yet"}
    return FileResponse(video_path, media_type="video/mp4", filename="Updated Video with Subtitle.mp4")
    
