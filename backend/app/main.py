# backend/app/main.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, json
from app.model_utils import inference_pipeline
from app.route_solver import find_nearest_ngos, simple_route_order

app = FastAPI(title="RescueRoute API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NGOS = json.load(open(os.path.join(BASE_DIR, "ngos_sample.json")))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/predict")
async def predict(file: UploadFile = File(None), text: str = Form(...)):
    image_path = None
    if file:
        fp = os.path.join(UPLOAD_DIR, file.filename)
        with open(fp,"wb") as f:
            shutil.copyfileobj(file.file, f)
        image_path = fp
    result = inference_pipeline(image_path, text)
    # parse coords if provided like lat:11.02 lng:76.95
    lat = None; lng = None
    for token in (text or "").split():
        if token.startswith("lat:"):
            try: lat = float(token.split(":")[1])
            except: pass
        if token.startswith("lng:"):
            try: lng = float(token.split(":")[1])
            except: pass
    if not lat:
        lat,lng = 11.0168,76.9558
    ngos = find_nearest_ngos(lat,lng,NGOS, topk=3)
    return {"inference": result, "suggested_ngos": ngos}

@app.post("/route")
async def route(start_lat: float = Form(...), start_lng: float = Form(...), pickup_ids: str = Form(...)):
    ids = [int(x) for x in pickup_ids.split(",") if x.strip()]
    pickups = [n for n in NGOS if n["id"] in ids]
    order = simple_route_order((start_lat,start_lng), pickups)
    return {"route_order": order}