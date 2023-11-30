from fastapi import FastAPI, HTTPException, status
from db.schemas.userSchema import user_schema
from db.schemas.discSchema import disc_schema
from db.schemas.passengerSchema import passenger_schema
from pydantic import BaseModel 
from pymongo import MongoClient

class User(BaseModel):
    id: str | None
    username:str
    full_name: str
    email:str
    phone: str
    disabled:bool

class Disc(BaseModel):
    id: str | None
    title:str
    artist: str
    genre:str
    year: int
    label:str

class Passenger(BaseModel):
    id: str | None
    identifier: int
    name: str
    survived: bool
    sex: str
    age: int

app = FastAPI()
connection = MongoClient("mongodb+srv://juapamendoza:p0p0c1t4@clustermodelos.nm1fiwg.mongodb.net/?retryWrites=true&w=majority").juapamendoza


#******************* ALUMNOS MODELOS WEB ********************
@app.get("/modelosweb/")
async def usersclass():
    users_list = []
    try:
        for userdb in connection.Computacion.ModelosWEB.find():
            userJSON = user_schema(userdb)
            users_list.append(User(**userJSON))
        return users_list
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get("/modelosweb/{username}")
async def usersclass(username:str):
    try:
        new_user = user_schema(connection.Computacion.ModelosWEB.find_one({"username":username}))
        return User(**new_user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
@app.post("/modelosweb/")
async def usersclass(user:User):
    user_dict = dict (user) #convertir de User a JSON
    del user_dict["id"] #eliminar id
    id = connection.Computacion.ModelosWEB.insert_one(user_dict).inserted_id
    new_user = user_schema(connection.Computacion.ModelosWEB.find_one({"_id":id}))
    return {"Usuario Agregado :)"}

@app.put("/modelosweb/{username}", response_model=User)
async def usersclass(user: User, username:str):
    newusername = user.username
    full_name = user.full_name
    email = user.email
    phone = user.phone
    disabled = user.disabled

    filtro = {"username":username}
    newvalues = {"$set":{"full_name":full_name,
                         "email":email,
                         "phone":phone,
                         "disabled":disabled,
                         "username":newusername}}

    try:
        connection.Computacion.ModelosWEB.update_one(filtro,newvalues)
        new_user = user_schema(connection.Computacion.ModelosWEB.find_one({"username":newusername}))
        return User(**new_user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/modelosweb/{username}")
async def usersclass(username:str):
    try:
        connection.Computacion.ModelosWEB.delete_one({"username":username})
        return {"Usuario eliminado :)"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
#**************** DISCOS *****************
@app.get("/discos/")
async def discosclass():
    discos_list = []
    try:
        for disco in connection.Discos.DiscosDB.find():
            discJSON = disc_schema(disco)
            discos_list.append(Disc(**discJSON))
        return discos_list
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@app.get("/discos/{title}")
async def discosclass(title:str):
    try:
        discJSON = disc_schema(connection.Discos.DiscosDB.find_one({"title":title}))
        return Disc(**discJSON)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
@app.post("/discos/")
async def discosclass(disco:Disc):
    disc_dict = dict (disco) #convertir de User a JSON
    del disc_dict["id"] #eliminar id
    #id = 
    connection.Discos.DiscosDB.insert_one(disc_dict).inserted_id
    #new_user = user_schema(connection.Discos.find_one({"_id":id}))
    return {"Disco Agregado :)"}

@app.put("/discos/{title}", response_model=Disc, status_code=status.HTTP_201_CREATED)
async def discosclass(disco: Disc, title:str):
    newtitle = disco.title
    newartist = disco.artist
    newgenre = disco.genre
    newyear = disco.year
    newlabel = disco.label

    filtro = {"title":title}
    newvalues = {"$set":{"artist":newartist,
                         "genre":newgenre,
                         "year":newyear,
                         "label":newlabel}}

    try:
        connection.Discos.DiscosDB.update_one(filtro,newvalues)
        new_disc =  disc_schema(connection.Discos.DiscosDB.find_one({"title":newtitle}))
        return Disc(**new_disc)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    
@app.delete("/discos/{title}")
async def discosclass(title:str):
    try:
        connection.Discos.DiscosDB.delete_one({"title":title})
        return {"Disco eliminado :)"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

#**************** PASSEGNER *****************
@app.get("/titanic/")
async def titanicclass():
    passenger_list = []
    try:
        for passenger in connection.Titanic.Passengers.find():
            passengerJSON = passenger_schema(passenger)
            passenger_list.append(Passenger(**passengerJSON))
        return passenger_list
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@app.get("/titanic/{identifier}")
async def titanicclass(identifier:int):
    try:
        passengerJSON = passenger_schema(connection.Titanic.Passengers.find_one({"identifier":identifier}))
        return Passenger(**passengerJSON)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
@app.post("/titanic/")
async def titanicclass(passenger:Passenger):
    passenger_dict = dict (passenger) #convertir de User a JSON
    del passenger_dict["id"] #eliminar id
    connection.Titanic.Passengers.insert_one(passenger_dict).inserted_id
    return {"Pasajero Agregado :)"}

@app.put("/titanic/{identifier}", response_model=Passenger, status_code=status.HTTP_201_CREATED)
async def titanicclass(passenger: Passenger, identifier:int):
    newname = passenger.name
    newsurvived = passenger.survived
    newsex = passenger.sex
    newage = passenger.age

    filtro = {"identifier":identifier}
    newvalues = {"$set":{"name":newname,
                         "survived":newsurvived,
                         "sex":newsex,
                         "age":newage}}

    try:
        connection.Titanic.Passengers.update_one(filtro,newvalues)
        new_passenger =  passenger_schema(connection.Titanic.Passengers.find_one({"identifier":identifier}))
        return Passenger(**new_passenger)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    
@app.delete("/titanic/{identifier}")
async def titanicclass(identifier:int):
    try:
        connection.Titanic.Passengers.delete_one({"identifier":identifier})
        return {"Pasajero eliminado :)"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


"""
*** USER ***
"id": "",
"username": "User1",
"full_name": "Username Uno",
"email": "user@example.com",
"phone": "222 222 2222",
"disabled": false

*** DISC ***
"id": "",
"title": "DiscoPrueba",
"artist": "ArtistPrueba",
"genre": "Pop",
"year": 2023,
"label": "Any Label"

*** PASSENGER ***
"id": "",
"identifier": 1,
"name": "NameTest",
"survived": "False",
"sex": "male",
"age": 1

"""
