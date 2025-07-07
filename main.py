import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from geoalchemy2.shape import to_shape
from shapely.geometry import shape
from database import SessionLocal, engine, Base
from models import Feature
from schemas import FeatureCreate
import json

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/features")
def create_feature(feature: FeatureCreate):
    """
    - Добавление объекта: POST /features
    :param feature:
    :return:
    """
    db = SessionLocal()
    try:
        geom = shape(feature.geometry)
        db_feature = Feature(geom=f'SRID=4326;{geom.wkt}', geom_type=feature.type)
        db.add(db_feature)
        db.commit()
        db.refresh(db_feature)
        return {"id": db_feature.id}
    finally:
        db.close()


@app.get("/features")
def get_features():
    """
    Получение всех объектов: GET /features
    :return:
    """
    db = SessionLocal()
    try:
        features = db.query(Feature).all()
        geojson_features = []
        for feat in features:
            geom = to_shape(feat.geom)
            geojson_features.append({
                "type": "Feature",
                "geometry": json.loads(json.dumps(geom.__geo_interface__)),
                "properties": {"id": feat.id, "type": feat.geom_type}
            })
        return {"type": "FeatureCollection", "features": geojson_features}
    finally:
        db.close()
#         Пример
# {
#   "geometry": {
#     "type": "Point",
#     "coordinates": [30.5234, 50.4501]
#   },
#   "type": "Point"
# }


@app.delete("/features/{feature_id}")
def delete_feature(feature_id: int):
    """
    Удаление объекта: DELETE /features/{feature_id}
    :param feature_id:
    :return:
    """
    db = SessionLocal()
    try:
        feature = db.query(Feature).get(feature_id)
        if not feature:
            raise HTTPException(status_code=404, detail="Функция не найдена")
        db.delete(feature)
        db.commit()
        return {"status": "deleted"}
    finally:
        db.close()

@app.get("/stats")
def get_stats():
    """
    Получение статистики: GET /stats
    :return:
    """
    db = SessionLocal()
    try:
        stats = {"points": 0, "lines": 0, "polygons": 0}
        for geom_type in ["Point", "LineString", "Polygon"]:
            count = db.query(Feature).filter(Feature.geom_type == geom_type).count()
            key = geom_type.lower() + 's'
            stats[key] = count
        return stats
    finally:
        db.close()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """
    Страница с дашбордом
    :param request:
    :return:
    """
    db = SessionLocal()
    try:
        features = db.query(Feature).order_by(Feature.id.desc()).limit(10).all()
        stats = {"points": 0, "lines": 0, "polygons": 0}
        for geom_type in ["Point", "LineString", "Polygon"]:
            count = db.query(Feature).filter(Feature.geom_type == geom_type).count()
            stats[geom_type.lower() + 's'] = count
        return templates.TemplateResponse("dashboard2.html", {"request": request, "stats": stats, "features": features})
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8000,
        reload=True,
    )