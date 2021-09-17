from fastapi import FastAPI
from models import Hero
from typing import List
from database import create_db_schemas
import services

app=FastAPI()


@app.get('/heros', response_model=List[Hero])
def get_heros():
    return services.get_heros()
    
@app.get('/heros/{hero_id}', response_model=Hero)
def get_hero_by_id(hero_id):
    return services.find_hero(hero_id)

@app.post('/heros', response_model=Hero)
def create_hero(hero: Hero):
    return services.create_hero(hero)

@app.post('/fakeheros', response_model=List[Hero])
def create_fake_heros():
    services.create_fake_heros()
    return services.get_heros()
    
@app.on_event('startup')
def on_startup():
    print('on started')
    create_db_schemas()
    