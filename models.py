from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry(geometry_type='GEOMETRY', srid=4326))
    geom_type = Column(String)