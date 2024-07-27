import datetime as dt
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import matplotlib.pyplot as plt
from database import get_available_images, get_image_slice, upload_image

APP_VERSION = "0.1.0"

# Upload an initial example to DB
try:
    upload_image(
        csv_path="/app/img.csv"
    )
    print("Example image successfully uploaded to DB")
except Exception as e:
    print(e)
    

# FastAPI
app = FastAPI(
    title="Get slices from DB Images",
    description="API allows to get slice from image with 'min_depth'-'max_depth' parameters",
    version=APP_VERSION)

class RequestData(BaseModel):
    image_name: str
    min_depth: float
    max_depth: float

@app.get('/')
async def read_root():
    return {
        "Api_Name": "Get slices"
    }

@app.get('/api/available_images')
async def available_images():
    response = get_available_images()
    return response


@app.post('/api/get_slice')
async def get_slice(data: RequestData):
    response = get_image_slice(
        image_name=data.image_name,
        min_depth=data.min_depth,
        max_depth=data.max_depth
    )

    image_path = f"/app/user_images/{dt.datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
    plt.imsave(fname=image_path, arr=response)
    response = FileResponse(path=image_path, media_type="image/png")

    return response

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
