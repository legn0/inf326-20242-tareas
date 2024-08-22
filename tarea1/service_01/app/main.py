from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Pokemon(BaseModel):
    name: str
    poke_types: List[str]

fake_db_pokemon = {
    'curr_id': 8,
    'items' : {
        1: Pokemon(name='bulbasaur', poke_types=['grass', 'poison']),
    
        2: Pokemon(name='squirtle', poke_types=['water'] ),
        
        4: Pokemon(name='charmander', poke_types=['fire']),
       
        5: Pokemon(name='pikachu', poke_types=['electric']),
 
        6: Pokemon(name='pidgey', poke_types=['flying', 'normal']),

        7: Pokemon(name='gastly', poke_types=['ghost', 'poison'])
    }
}



@app.get("/")
async def root():

    return {"this is" : "a fake pokemon DB"}


@app.get("/pokemon/{poke_id}/")
async def get_pokemon(poke_id: int):
    if poke_id in fake_db_pokemon['items']:
        return {'pokemon': fake_db_pokemon['items'][poke_id].dict()}
    else:
        return {'pokemon': 'Not Found'}

@app.post('/pokemon/')
async def create_pokemon(pokemon: Pokemon):
    curr_id = fake_db_pokemon['curr_id']
    fake_db_pokemon['items'][curr_id] = pokemon
    fake_db_pokemon['curr_id'] += 1
    return pokemon