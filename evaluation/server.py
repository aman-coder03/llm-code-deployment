from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/notify")
async def receive_evaluation(request: Request):
    data = await request.json()
    print("Received evaluation data:")
    print(data)
    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
