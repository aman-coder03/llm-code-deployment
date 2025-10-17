from fastapi import FastAPI, HTTPException, status, Request,BackgroundTasks
from fastapi.responses import JSONResponse
from .models import TaskRequest
from .utils import validate_secret
from .rounds import round1,round2
app = FastAPI()


@app.post("/handle-task",status_code=status.HTTP_200_OK)
async def handle_task(request: TaskRequest, background_tasks: BackgroundTasks):
    # Validate secret
    if not validate_secret(request.secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid secret",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Respond immediately
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "Secret validated, task accepted for processing."
        }
    )
    if request.round == 1 or request.round =="1":
        background_tasks.add_task(round1, request)
    elif request.round ==2 or request.round =="2":
        background_tasks.add_task(round2)


    return response



@app.get("/")
def read_root():
    return {"Hello": "World"}   
