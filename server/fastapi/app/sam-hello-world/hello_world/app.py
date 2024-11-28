from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/hello", status_code=200)
async def root():
  return {"message": "Hello SAM World"}

lambda_handler = Mangum(app)

