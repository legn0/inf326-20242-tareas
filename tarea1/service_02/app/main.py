from fastapi import FastAPI
from pydantic import BaseModel
from typing import Set

app = FastAPI()

class PokeType(BaseModel):
    name: str
    effective: Set[str] | None = None
    non_effective: Set[str] | None = None
    cancelled: Set[str] | None = None

fake_db_types = {
    'curr_id': 9,
    'items' : {
        1: PokeType(name='grass', effective={'water'}, non_effective={'poison', 'fire', 'grass'}),
    
        2: PokeType(name='poison', effective={'grass'}, ),
        
        3: PokeType(name='water', effective={'fire'}, non_effective={'water', 'fire', 'electric'}),
       
        4: PokeType(name='fire', effective={'grass'}, non_effective={'fire', 'water'}),
 
        5: PokeType(name='flying' ),

        6: PokeType(name='normal', cancelled={'ghost'}),

        7: PokeType(name='ghost', effective={'ghost'}, cancelled={'normal'}),

        8: PokeType(name='electric', effective={'water'}, non_effective={'grass'})
    }
}



@app.get("/")
async def root():

    return {"this is" : "a fake type DB"}


@app.get("/poke_type/{poke_type_id}/")
async def get_pokemon(poke_type_id: int):
    return {'poke_type': fake_db_types['items'][poke_type_id].dict()}

@app.get('/poke_type/weak_against/{poke_type_id}/')
async def get_weaknesses(poke_type_id: int):
    items = fake_db_types['items']
    name = items[poke_type_id].name
    stronger_types = list(filter(lambda type_id: name in items[type_id].effective , items))
    return {'stronger_types':stronger_types}

@app.get('/poke_type/strong_against/{poke_type_id}/')
async def get_resistances(poke_type_id: int):
    items = fake_db_types['items']
    name = items[poke_type_id].name
    weaker_types = list(filter(lambda type_id: name in items[type_id].non_effective.union(items[type_id].cancelled) , items))
    return {'weakger_types':weaker_types}

@app.post('/poke_type/')
async def create_poke_type(poke_type: PokeType):
    curr_id = fake_db_types['curr_id']
    fake_db_types['items'][curr_id] = poke_type
    fake_db_types['curr_id'] += 1
    return poke_type