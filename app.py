from fastapi import Depends, FastAPI,Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import get_db,User,Brand,Occasion,Outfit
from typing import Optional


app = FastAPI()

#create routes to access resources 
app.get("/")
def read_root():
    return{"Hello":"world"}

class UserSchema(BaseModel):
    username : str
    avatar_url : str
    bio : str


@app.post("/user")
def create_user(user : UserSchema, session= Depends(get_db)):
    user_details = User(
        username = user.username,
        avatar_url = user.avatar_url,
        bio = user.bio
    )
    session.add(user_details)
    session.commit()
    return{"message":"user details added successfully"}


@app.get("/user")
def get_user(session = Depends(get_db)):
    all_users = session.query(User).all()
    return all_users

#get a single user
@app.get("/user/{user_id}")
def get_single_user(user_id):
    return {"id":user_id}

class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


@app.patch("/user/{user_id}")
def patch_user(
    user_id: int,
    user_update: UpdateUserSchema,
    session = Depends(get_db)
):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Only update fields that were provided in the request
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.avatar_url is not None:
        user.avatar_url = user_update.avatar_url
    if user_update.bio is not None:
        user.bio = user_update.bio

    session.commit()
    session.refresh(user)    #ensures database reflects recent changes
    return user



class OccasionSchema(BaseModel):
    name : str
    description : str

@app.post("/occasion")
def create_occasion( occasion : OccasionSchema,session=Depends(get_db) ):
    all_occasion =  Occasion(
        name = occasion.name,
        description = occasion.description
    )
    session.add(all_occasion)
    session.commit()

@app.get("/occasion")
def get_occasions(session = Depends(get_db)):
    all_occasions = session.query(Occasion).all()
    return all_occasions

@app.get("/occasion/{occasion_id}")
def get_single_occasion(occasion_id):
    return {"id":occasion_id}




class BrandSchema(BaseModel):
    name:str
    description:str

@app.post("/brand")
def create_brand(brand : BrandSchema, session = Depends(get_db)):
    #creating an instance of the Brand class model with details
    brand_input= Brand( 
        name =brand.name,
        description =brand.description
        )
    #add instance to transaction
    session.add(brand_input)
    #commit transaction
    session.commit()
    return {"message":"brand was added successfully"}


@app.get("/brand")
def read_brand(session = Depends(get_db)):
    brands = session.query(Brand).all()
    return brands


class OutfitSchema(BaseModel):
    user_id: int
    brand_id: Optional[int] = None
    occasion_id: Optional[int] = None
    name: str
    description: str
    color: str
    image_url: str



@app.post("/outfit")
def create_outfit(outfit:OutfitSchema, session = Depends(get_db)):
    new_outfit = Outfit(
    user_id=outfit.user_id,
    brand_id=outfit.brand_id,
    occasion_id=outfit.occasion_id,
    name=outfit.name,
    description=outfit.description,
    color=outfit.color,
    image_url=outfit.image_url
)
    #add to session
    session.add(new_outfit)
    #save 
    session.commit()

    return {"message": "outfit added successfully"}


@app.get("/outfit")
def get_outfit(session = Depends(get_db)):
    #using sqlalchemy to retrieve all outfits
    all_outfits = session.query(Outfit).all()
    return all_outfits



# http://127.0.0.1:8000/brand