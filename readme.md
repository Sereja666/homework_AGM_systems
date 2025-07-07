
alembic init alembic
alembic revision --autogenerate -m "Описание изменений"
alembic upgrade head
alembic downgrade -1


http://localhost:8000/docs

Примеры Json для добавления в БД:
{
  "geometry": {
    "type": "Point",
    "coordinates": [30.5234, 50.4501]
  },
  "type": "Point"
}
{
  "geometry": {
    "type": "LineString",
    "coordinates": [
      [30.5234, 50.4501],
      [30.5240, 50.4510]
    ]
  },
  "type": "LineString"
}
{
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [30.5234, 50.4501],
        [30.5240, 50.4501],
        [30.5240, 50.4510],
        [30.5234, 50.4510],
        [30.5234, 50.4501]
      ]
    ]
  },
  "type": "Polygon"
}