from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

conn = sqlite3.connect('plants.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS plants (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
species TEXT NOT NULL,
description TEXT
)
''')

class Plant(BaseModel):
    name: str
    species: str
    description: str = None

app = FastAPI()

@app.get("/plants")
def get_plants():
    cursor.execute('SELECT * FROM plants')
    plants = cursor.fetchall()
    if plants:
        return plants
    else:
        return []

@app.post("/plants")
def add_plant(plant: Plant):
    cursor.execute('INSERT INTO plants (name, species, description) VALUES (?, ?, ?)', (plant.name, plant.species, plant.description))
    conn.commit()
    return {"message": "Растение успешно добавлено в базу данных!"}

@app.put("/plants/{plant_id}")
def update_plant(plant_id: int, new_name: str):
    cursor.execute('UPDATE plants SET name = ? WHERE id = ?', (new_name, plant_id))
    conn.commit()
    return {"message": "Название растения успешно обновлено!"}

@app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int):
    cursor.execute('DELETE FROM plants WHERE id = ?', (plant_id,))
    conn.commit()
    return {"message": "Растение успешно удалено из базы данных!"}

@app.get("/plants/search")
def search_plant(query: str):
    cursor.execute('SELECT * FROM plants WHERE name LIKE ?', ('%' + query + '%',))
    plants = cursor.fetchall()
    if plants:
        return plants
    else:
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
