from pydantic import BaseModel
from typing import Literal

class FeatureCreate(BaseModel):
    geometry: dict
    type: Literal['Point', 'LineString', 'Polygon']
