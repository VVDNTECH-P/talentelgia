import email
from email.policy import default
from xmlrpc.client import Boolean
from fastapi import FastAPI , Request,Depends ,Form, Body ,  File , UploadFile , status , HTTPException , Response
import database
import models
from sqlalchemy.orm import Session
import schema
from datetime import datetime
from typing import Union 
import shutil
from pydantic import SecretStr , EmailStr
from sqlalchemy import  JSON, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import smtplib , ssl
from email.message import EmailMessage
import random as r
import email_validator as  _email_check 

from fastapi.responses import JSONResponse
import services as _services
import schema as _schema
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import passlib.hash as _hash



app = FastAPI()

models.Parent.metadata.create_all(database.engine) # create database when you create your models
models.Child.metadata.create_all(database.engine)
def get_db():
    db = database.SessionLocal()
    try :
        yield db 
    finally:
        db.close()

# for current dateand time 
now = datetime.now()
current_time = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


#this instance/API is for category upload 
@app.post('/category/', status_code=status.HTTP_201_CREATED)
async def Business_category_function(request : schema.category ,user : _schema.User = _fastapi.Depends(_services.get_current_user) , db : Session = Depends(get_db)   ):
    if request.name == "":
        raise _fastapi.HTTPException(status_code=404 , detail= "this field not null  ")
        
    Business_category_post = models.Business_categorys(
        name = request.name ,
        status  = True, 
        created_at = current_time , 
        updated_at = current_time )
    
    db.add(Business_category_post)
    db.commit()
    db.refresh(Business_category_post)
    return Business_category_post


# thsi api is  for update category 
@app.put('/category/{id}/' ,status_code=status.HTTP_202_ACCEPTED)
def category_update(id : int,  request : schema.category ,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db) ):
    fetch_data_category  = db.query(models.Business_categorys).filter(models.Business_categorys.id == id )
    print(fetch_data_category.exists())
    if not fetch_data_category.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
        
    else:
        fetch_data_category = db.query(models.Business_categorys).filter(models.Business_categorys.id == id ).update(dict(name = request.name ,updated_at =  current_time ))
        db.commit()
        print("/////////////////////////////")
        data =  db.query(models.Business_categorys).filter(models.Business_categorys.id == id ).first()
        return data


# this is for detele post
@app.delete('/category/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response ,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_category = db.query(models.Business_categorys).filter(models.Business_categorys.id == id)
    if not delete_data_category.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_category = db.query(models.Business_categorys).filter(models.Business_categorys.id == id ).update(dict(status = False ))
    db.commit()
    return "delete successfully"

# This is for return all data from category 
@app.get('/category/' , status_code=status.HTTP_200_OK)
def fetch_data(user : _schema.User = _fastapi.Depends(_services.get_current_user) , db : Session = Depends(get_db) ):
    result = db.query(models.Business_categorys).all()
    return result




#This is for return single data from category 
@app.get('/category/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int ,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog = db.query(models.Business_categorys).filter(models.Business_categorys.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
        
    return new_blog






# this post request is for add subcategory 
@app.post('/sub_category' , status_code=status.HTTP_201_CREATED)
async def  Business_sub_category_function(request : schema.sub_category,user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db), ):
    
    Business_sub_category_post = models.Business_sub_categorys(
    name = request.name ,
    status  = True, 
    created_at = current_time , 
    updated_at = current_time ,
    business_category_id =  request.business_category_id , 
    )

    db.add(Business_sub_category_post)
    db.commit()
    db.refresh(Business_sub_category_post)
    return Business_sub_category_post


# This request is for update sub_category 
@app.put('/sub_category/{id}/' ,status_code=status.HTTP_202_ACCEPTED)
def category_update(id : int,  request : schema.sub_category,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db) ):
    fetch_data_subcategory  = db.query(models.Business_sub_categorys).filter(models.Business_sub_categorys.id == id )
    print(fetch_data_subcategory.exists())
    if not fetch_data_subcategory.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_subcategory = db.query(models.Business_sub_categorys).filter(models.Business_sub_categorys.id == id ).update(dict(name = request.name , business_category_id= request.business_category_id,updated_at =  current_time ))
        db.commit()
        data =  db.query(models.Business_sub_categorys).filter(models.Business_sub_categorys.id == id ).first()
        return data
    
#This request is for delete subcategory 
@app.delete('/sub_category/{id}', status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_sub_category = db.query(models.Business_sub_categorys).filter(models.Business_sub_categorys.id == id)
    if not delete_data_sub_category.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    delete_data_sub_category = db.query(models.Business_sub_categorys).filter(models.Business_sub_categorys.id == id ).update(dict(status = False ))
    db.commit()
    return  "data delete successful"


#This request is for return all data from subcategory 

@app.get('/sub_category/', status_code=status.HTTP_200_OK)
def all_category(user : _schema.User = _fastapi.Depends(_services.get_current_user) ,db : Session = Depends(get_db)):
    new_blog =  db.query(models.Business_sub_categorys).all()
    return new_blog


#This request is for return one data from subcategory 
@app.get('/sub_category/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int ,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog = db.query(models.Business_sub_categorys).filter(models.Business_sub_categorys.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
        
    return new_blog




    
# This Instance/API is  for countries
@app.post('/countries/',status_code=status.HTTP_201_CREATED)
async def Countries_function( user : _schema.User = _fastapi.Depends(_services.get_current_user),
    name : Union[str, None] = Body(max_length=10 , min_length= 5,default=False),
    file : UploadFile = File(...) ,
    db : Session = Depends(get_db), 
):
    with open("media/"+ file.filename , 'wb') as image :    
        shutil.copyfileobj(file.file , image)

    url = str('media/' + file.filename)
    

    Countries_post = models.Countries(
        
        name = name ,
        flag_image = url ,
        status = True ,
        created_at= current_time , 
        updated_at= current_time                       
                                    )
    
    db.add(Countries_post)
    db.commit()
    db.refresh(Countries_post)
    return Countries_post









@app.put('/countries/{id}/',status_code=status.HTTP_202_ACCEPTED)
def Countries_update(
    id : int , 
    name : Union[str, None] = Body(max_length=10 , min_length= 5,default=None),
    file : UploadFile = File(...) ,
    user : _schema.User = _fastapi.Depends(_services.get_current_user),
    db : Session = Depends(get_db), 
):

    with open("media/"+ file.filename , 'wb') as image :
        shutil.copyfileobj(file.file , image)

    url = str('media/' + file.filename)
    
    fetch_data_coutries = db.query(models.Countries).filter(models.Countries.id == id )
    if not fetch_data_coutries.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_coutries = db.query(models.Countries).filter(models.Countries.id == id ).update(dict(name = name , flag_image = url ,updated_at =  current_time ))
        db.commit()
        data = db.query(models.Countries).filter(models.Countries.id == id ).first()
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(data)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
        return data




@app.delete('/contries/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response, user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_contries= db.query(models.Countries).filter(models.Countries.id == id)
    if not delete_data_contries.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_contries = db.query(models.Countries).filter(models.Countries.id == id ).update(dict(status = False))

    db.commit()
    return "delete successful"




# This request is responsible for return all data from countries
@app.get('/contries/', status_code=status.HTTP_200_OK)
def all_contries(  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    new_blog =  db.query(models.Countries).all()
    return new_blog

#This request is for return one data from contries 
@app.get('/contries/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int , user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog = db.query(models.Countries).filter(models.Countries.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
        
    return new_blog







# This instance/ APi is for states  
@app.post('/state/', status_code=status.HTTP_201_CREATED)
async def state_function(request : schema.state, user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db),):
    state_post = models.States(
    name = request.name ,
    countries_id = request.countries_id , 
    status  = True , 
    created_at = current_time , 
    updated_at = current_time ,

    )

    db.add(state_post)
    db.commit()
    db.refresh(state_post)
    return state_post


@app.put("/state/{id}/",status_code=status.HTTP_202_ACCEPTED)
def state_update(id : int,  request : schema.state, user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db) ):
    fetch_data_state = db.query(models.States).filter(models.States.id == id )
    
    if not fetch_data_state.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_state = db.query(models.States).filter(models.States.id == id ).update(dict(name = request.name  ,countries_id =  request.countries_id  ,updated_at =  current_time ))
        db.commit()
        data = db.query(models.States).filter(models.States.id == id ).first()
        return data

@app.get("/state/", status_code=status.HTTP_200_OK)
def state_get_all( user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    data = db.query(models.States).all()
    return data

#This request is for return one data from state  
@app.get('/state/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int ,  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    new_blog = db.query(models.States).filter(models.States.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
        
    return new_blog

@app.delete('/state/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response, user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_state= db.query(models.States).filter(models.States.id == id)
    if not delete_data_state.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_state = db.query(models.States).filter(models.States.id == id ).update(dict(status = False))
    db.commit()
    response.headers['delete_data'] = "data delete successful"












@app.post('/cities/', status_code=status.HTTP_201_CREATED)
async def cities_function(
    name : Union[str, None] = Body(default=None),
    state_id  : Union[int, None] = Body(default=None),
    user : _schema.User = _fastapi.Depends(_services.get_current_user),
    db : Session = Depends(get_db), 

):
    cities_post = models.Cities(
    name = name ,
    state_id = state_id , 
    status  = True , 
    created_at = current_time , 
    updated_at = current_time ,

    )

    db.add(cities_post)
    db.commit()
    db.refresh(cities_post)
    return cities_post


@app.put("/cities/{id}/",status_code=status.HTTP_202_ACCEPTED)
def city_update(id : int,  request : schema.city,  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db) ):
    fetch_data_city = db.query(models.Cities).filter(models.Cities.id == id )
    
    if not fetch_data_city.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_city = db.query(models.Cities).filter(models.Cities.id == id ).update(dict(name = request.name  ,state_id =  request.state_id  ,updated_at =  current_time ))
        db.commit()
        data = db.query(models.Cities).filter(models.Cities.id == id ).first()
        return data


    
    

@app.delete('/cities/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response, user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_city= db.query(models.Cities).filter(models.Cities.id == id)
    if not delete_data_city.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_city = db.query(models.Cities).filter(models.Cities.id == id ).update(dict(status = False))
    db.commit()
    return "delete data successfull "

@app.get("/cities/", status_code=status.HTTP_200_OK)
def city_get_all( user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    data = db.query(models.Cities).all()
    return data



#This request is for return one data from cities 
@app.get('/cities/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int ,  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    new_blog = db.query(models.Cities).filter(models.Cities.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog





@app.post('/businesses/' , status_code=status.HTTP_201_CREATED)
async def Businesses_function(    
    name : Union[str, None] = Body(default=None),
    category_id :Union[int, None] = Body(default=None),
    parent_id :Union[int, None] = Body(default=None),
    sub_category_id : Union[int, None] = Body(default=None),
    country_id :Union[int, None] = Body(default=None),
    state_id : Union[int, None] = Body(default=None),
    city_id : Union[int, None] = Body(default=None),
    information : Union[str, None] = Body(default=None),
    rating : Union[float, None] = Body(default=None),
    established_year : Union[datetime, None] = Body(default=None),
    address :Union[str, None] = Body(default=None),
    logo_large : UploadFile = File(...) ,
    logo_small : UploadFile = File(...),
     user : _schema.User = _fastapi.Depends(_services.get_current_user),
    db : Session = Depends(get_db), 
):
    with open("media/"+ logo_large.filename , 'wb') as image :
        shutil.copyfileobj(logo_large.file , image)
    with open("media/"+ logo_small.filename , 'wb') as image :
        shutil.copyfileobj(logo_small.file , image)

    url_for_large_logo = str('media/' + logo_large.filename)
    url_for_small_logo = str('media/' + logo_small.filename)
    
    
    data = {sub_category_id :sub_category_id }
    Business_post = models.Businesses(
        
        name = name ,
        category_id = category_id ,
        parent_id = parent_id,
        sub_category_id =data , 
        country_id = country_id ,
        state_id = state_id , 
        city_id = city_id, 
        logo_large = url_for_large_logo ,
        logo_small = url_for_small_logo,
        information =information,
        rating = rating,
        status = True ,
        established_year = established_year,
        address = address, 
        created_at= current_time , 
        updated_at= current_time       
                        
                                    )
    
    db.add(Business_post)
    db.commit()
    db.refresh(Business_post)
    return Business_post




@app.put('/businesses/{id}/',status_code=status.HTTP_202_ACCEPTED)
def Countries_update(
    id : int , 
    name : Union[str, None] = Body(default=None),
    category_id :Union[int, None] = Body(default=None),
    parent_id :Union[int, None] = Body(default=None),
    sub_category_id : Union[int, None] = Body(default=None),
    country_id :Union[int, None] = Body(default=None),
    state_id : Union[int, None] = Body(default=None),
    city_id : Union[int, None] = Body(default=None),
    information : Union[str, None] = Body(default=None),
    rating : Union[float, None] = Body(default=None),
    address :Union[str, None] = Body(default=None),
    logo_large : UploadFile = File(...) ,
    logo_small : UploadFile = File(...),
    user : _schema.User = _fastapi.Depends(_services.get_current_user),
    db : Session = Depends(get_db), 
):
    data = {sub_category_id :sub_category_id }
    with open("media/"+ logo_large.filename , 'wb') as image :
        shutil.copyfileobj(logo_large.file , image)
    with open("media/"+ logo_small.filename , 'wb') as image :
        shutil.copyfileobj(logo_small.file , image)

    url_for_large_logo = str('media/' + logo_large.filename)
    url_for_small_logo = str('media/' + logo_small.filename)
    
    
    
    fetch_data_business = db.query(models.Businesses).filter(models.Businesses.id == id )
    if not fetch_data_business.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_business = db.query(models.Businesses).filter(models.Businesses.id == id ).update(dict(name = name , category_id = category_id ,parent_id = parent_id ,sub_category_id = data ,country_id = country_id , state_id = state_id ,city_id = city_id ,information = information,rating = rating,address = address,logo_large = url_for_large_logo , logo_small = url_for_small_logo,updated_at =  current_time ))
        db.commit()
        return 'Data Updated'

@app.get("/businesses/", status_code=status.HTTP_200_OK)
def Business_get_all(user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    data = db.query(models.Businesses).all()
    return data

#This request is for return one data from businesses 
@app.get('/businesses/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int ,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog = db.query(models.Businesses).filter(models.Businesses.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog

@app.delete('/businesses/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_state= db.query(models.Businesses).filter(models.Businesses.id == id)
    if not delete_data_state.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_state = db.query(models.Businesses).filter(models.Businesses.id == id ).update(dict(status = False))
    db.commit()
    return "Detele Successfull"






@app.post('/businessfaqs/' , status_code=status.HTTP_201_CREATED)
async def  Business_faqs_function(request : schema.business_faqs,user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db), ):
    
    Business_faqs_post = models.Business_faqs(
    business_id = request.business_id ,
    question  = request.question , 
    answar = request.answar , 
    status  = True, 
    created_at = current_time , 
    updated_at = current_time ,
    )

    db.add(Business_faqs_post)
    db.commit()
    db.refresh(Business_faqs_post)
    return Business_faqs_post



@app.put('/businessfaqs/{id}/' ,status_code=status.HTTP_202_ACCEPTED)
def category_update(id : int,  request : schema.business_faqs, user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db) ):
    fetch_data_category  = db.query(models.Business_faqs).filter(models.Business_faqs.id == id )
    print(fetch_data_category.exists())
    if not fetch_data_category.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
        
    else:
        fetch_data_category = db.query(models.Business_faqs).filter(models.Business_faqs.id == id ).update(dict(business_id = request.business_id ,question = request.question,updated_at =  current_time ))
        db.commit()
        print("/////////////////////////////")
        data =  db.query(models.Business_faqs).filter(models.Business_faqs.id == id ).first()
        return data


@app.delete('/businessfaqs/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response, user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):    
    delete_data_Business_faqs = db.query(models.Business_faqs).filter(models.Business_faqs.id == id)
    if not delete_data_Business_faqs.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    delete_data_Business_faqs = db.query(models.Business_faqs).filter(models.Business_faqs.id == id ).update(dict(status = False ))
    db.commit()
    return "delete successful"


@app.get("/businessfaqs/", status_code=status.HTTP_200_OK)
def Business_get_all(user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    data = db.query(models.Business_faqs).all()
    return data

#This request is for return one data from businessfaqs 
@app.get('/businessfaqs/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int , user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    new_blog = db.query(models.Business_faqs).filter(models.Business_faqs.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog






@app.post('/business_products/' , status_code=status.HTTP_201_CREATED)
async def Business_products_function(    
    business_id : Union[int, None] = Body(default=None),
    name : Union[str, None] = Body(default=None),
    descriptions : Union[str, None] = Body(default=None),
    file : UploadFile = File(...) ,
    price : Union[float, None] = Body(default=None),
    user : _schema.User = _fastapi.Depends(_services.get_current_user),
    db : Session = Depends(get_db), 
):
    with open("media/"+ file.filename , 'wb') as image :
        shutil.copyfileobj(file.file , image)

    url = str('media/' + file.filename)
    

    Countries_post = models.Business_products(
        business_id = business_id ,
        name = name ,
        descriptions = descriptions ,
        image = url , 
        price = price , 
        status = True,
        created_at= current_time , 
        updated_at= current_time                       
                                    )
    
    db.add(Countries_post)
    db.commit()
    db.refresh(Countries_post)
    return Countries_post




@app.put('/business_products/{id}/',status_code=status.HTTP_202_ACCEPTED)
def Countries_update(
    id : int , 
    business_id : Union[int, None] = Body(default=None),
    name : Union[str, None] = Body(default=None),
    descriptions : Union[str, None] = Body(default=None),
    file : UploadFile = File(...) ,
    price : Union[float, None] = Body(default=None),
    user : _schema.User = _fastapi.Depends(_services.get_current_user),
    db : Session = Depends(get_db), 
):

    with open("media/"+ file.filename , 'wb') as image :
        shutil.copyfileobj(file.file , image)

    url = str('media/' + file.filename)
    
    fetch_data_Business_products = db.query(models.Business_products).filter(models.Business_products.id == id )
    if not fetch_data_Business_products.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_Business_products = db.query(models.Business_products).filter(models.Business_products.id == id ).update(dict(business_id = business_id ,name = name , descriptions = descriptions ,image = url,price = price ,updated_at =  current_time ))
        db.commit()
        data = db.query(models.Business_products).filter(models.Business_products.id == id ).first()
        return data



@app.delete('/business_products/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_Business_products= db.query(models.Business_products).filter(models.Business_products.id == id)
    if not delete_data_Business_products.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_Business_products = db.query(models.Business_products).filter(models.Business_products.id == id ).update(dict(status = False))
    db.commit()
    return "Delete successfull"


@app.get("/business_products/", status_code=status.HTTP_200_OK)
def Business_products_get_all(user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    data = db.query(models.Business_products).all()
    return data

#This request is for return one data from business_products 
@app.get('/business_products/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int ,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog = db.query(models.Business_products).filter(models.Business_products.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog                                             




@app.post("/amenities_services/" , status_code=status.HTTP_201_CREATED)
def Amenities_services(request : schema.Amenities_services  ,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    Amenities_services_post = models.Amenities_services(
        name = request.name ,
        status  = True, 
        created_at = current_time , 
        updated_at = current_time )
    
    db.add(Amenities_services_post)
    db.commit()
    db.refresh(Amenities_services_post)
    return Amenities_services_post



@app.put('/amenities_services/{id}/',status_code=status.HTTP_202_ACCEPTED)
def Amenities_services_update(id : int,  request : schema.Amenities_services,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db) ):
    fetch_data_Amenities_services = db.query(models.Amenities_services).filter(models.Amenities_services.id == id )
    print(fetch_data_Amenities_services.exists())
    if not fetch_data_Amenities_services.first():
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
        
    else:
        fetch_data_Amenities_services = db.query(models.Amenities_services).filter(models.Amenities_services.id == id ).update(dict(name = request.name ,updated_at =  current_time ))

        db.commit()
        data =  db.query(models.Amenities_services).filter(models.Amenities_services.id == id ).first()
        return data
    
    
    
@app.delete('/amenities_services/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response, user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):    
    delete_data_Amenities_services = db.query(models.Amenities_services).filter(models.Amenities_services.id == id)
    if not delete_data_Amenities_services.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_Amenities_services = db.query(models.Amenities_services).filter(models.Amenities_services.id == id ).update(dict(status = False ))
    db.commit()
    response.headers['delete_data'] = "data delete successful"


@app.get('/amenities_services/', status_code=status.HTTP_200_OK)

def all_category(user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog =  db.query(models.Amenities_services).all()
    return new_blog

#This request is for return one data from amenities_services 
@app.get('/amenities_services/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int , user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    new_blog = db.query(models.Amenities_services).filter(models.Amenities_services.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog                                             




@app.post("/business_amenities_services/" , status_code=status.HTTP_201_CREATED)
def Business_amenities_services_post(request : schema.Business_amenities_services  , user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    
    data = request.business_id
    data1 = {data : data}
    Business_amenities_services= models.Business_amenities_services(
        business_id = request.business_id ,
        amenity_service_id =data1,
        phone_number = request.phone_number ,
        status  = True, 
        created_at =current_time , 
        updated_at =current_time )
    
    db.add(Business_amenities_services)
    db.commit()
    db.refresh(Business_amenities_services)
    return Business_amenities_services



@app.put('/business_amenities_services/{id}/',status_code=status.HTTP_202_ACCEPTED)
def Business_amenities_services_updtae(id : int,  request : schema.Business_amenities_services,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db) ):
    fetch_data_Business_amenities_services = db.query(models.Business_amenities_services).filter(models.Business_amenities_services.id == id )
    print(fetch_data_Business_amenities_services.exists())
    if not fetch_data_Business_amenities_services.first():
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
        
    else:
        fetch_data_Business_amenities_services = db.query(models.Business_amenities_services).filter(models.Business_amenities_services.id == id ).update(dict(business_id = request.business_id ,amenity_service_id =  request.amenity_service_id , phone_number = request.phone_number , updated_at = current_time ))

        db.commit()
        data = db.query(models.Business_amenities_services).filter(models.Business_amenities_services.id == id ).first()
        return data
    
    

@app.delete('/business_amenities_services/{id}/', status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response,user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_Business_amenities_services = db.query(models.Business_amenities_services).filter(models.Business_amenities_services.id == id)
    if not delete_data_Business_amenities_services.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_Business_amenities_services = db.query(models.Business_amenities_services).filter(models.Business_amenities_services.id == id ).update(dict(status = False ))
    db.commit()
    response.headers['delete_data'] = "data delete successful"


@app.get('/business_amenities_services/', status_code=status.HTTP_200_OK)
def all_category(user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog =  db.query(models.Business_amenities_services).all()
    return new_blog

#This request is for return one data from business_amenities_services 
@app.get('/business_amenities_services/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int , user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    new_blog = db.query(models.Business_amenities_services).filter(models.Business_amenities_services.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog                                             





@app.post("/payment_method/" , status_code=status.HTTP_201_CREATED)
def payment_method_post(request : schema.Payment_methods  ,  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    payment_method= models.Payment_methods(
        name  = request.name ,
        status = True,
        created_at =current_time , 
        updated_at =current_time )
    
    db.add(payment_method)
    db.commit()
    db.refresh(payment_method)
    return payment_method



@app.put('/payment_method/{id}/' ,status_code=status.HTTP_202_ACCEPTED)
def payment_method_updtae(id : int,  request : schema.Payment_methods,  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db) ):
    fetch_data_payment_method = db.query(models.Payment_methods).filter(models.Payment_methods.id == id )
    print(fetch_data_payment_method.exists())
    if not fetch_data_payment_method.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_payment_method = db.query(models.Payment_methods).filter(models.Payment_methods.id == id ).update(dict(name  = request.name  , updated_at = current_time ))
        db.commit()
        data = db.query(models.Payment_methods).filter(models.Payment_methods.id == id ).first()
        return data
    

@app.delete('/payment_method/{id}/' , status_code=status.HTTP_200_OK)
def deleteblog(id ,response: Response,  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):    
    delete_data_payment = db.query(models.Payment_methods).filter(models.Payment_methods.id == id)
    if not delete_data_payment.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_payment = db.query(models.Payment_methods).filter(models.Payment_methods.id == id ).update(dict(status = False ))
    db.commit()
    return "Delete successfull"


@app.get('/payment_method/', status_code=status.HTTP_200_OK)
def all_category( user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog =  db.query(models.Payment_methods).all()
    return new_blog

#This request is for return one data from payment_method 
@app.get('/payment_method/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int , user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog = db.query(models.Payment_methods).filter(models.Payment_methods.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog                                             




#user group
@app.post("/user_group/" , status_code=status.HTTP_201_CREATED)
def user_group_upload(request : schema.User_group  , user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    payment_method= models.User_group_types(
        group_name  = request.group_name ,
        status = True,
        created_at =current_time , 
        updated_at =current_time )
    
    db.add(payment_method)
    db.commit()
    db.refresh(payment_method)
    return payment_method




@app.put('/user_group/{id}/' ,status_code=status.HTTP_202_ACCEPTED)
def user_group_updtae(id : int,  request : schema.User_group, user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db) ):
    fetch_data_payment_method = db.query(models.User_group_types).filter(models.User_group_types.id == id )
    print(fetch_data_payment_method.exists())
    if not fetch_data_payment_method.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_payment_method = db.query(models.User_group_types).filter(models.User_group_types.id == id ).update(dict(group_name  = request.group_name  , updated_at = current_time ))
        db.commit()
        data = db.query(models.User_group_types).filter(models.User_group_types.id == id ).first()
        return data

@app.delete('/user_group/{id}/' , status_code=status.HTTP_200_OK)
def deleteuser(id ,response: Response,  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):    
    delete_data_payment = db.query(models.User_group_types).filter(models.User_group_types.id == id)
    if not delete_data_payment.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_payment = db.query(models.User_group_types).filter(models.User_group_types.id == id ).update(dict(status = False ))
    db.commit()
    return "Delete successfull"


@app.get('/user_group/', status_code=status.HTTP_200_OK)
def all_category(  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    new_blog =  db.query(models.User_group_types).all()
    return new_blog

#This request is for return one data from user_group 
@app.get('/user_group/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int , user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog = db.query(models.User_group_types).filter(models.User_group_types.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog                                             



# @app.post("/usertest")
# async def create_user(
#     username: str , 
#     password: SecretStr 
 
# ):
#     print(username)
#     print(password)



# @app.post("/user/" , status_code=status.HTTP_201_CREATED)
# async def user_upload(
#     f_name : str,
#     l_name : str , 
#     email : EmailStr ,
#     User_group : int,
#     password :SecretStr,
#     db : Session = Depends(get_db)

    
#     ):
#     print('$$$$$$$$$$$$$$$$$$$$$$$$$$$' , password)
#     payment_method= models.Users(
#         f_name  = f_name ,
#         l_name = l_name , 
#         email = email , 
#         User_group = User_group ,
#         password = password , 
#         status = True,
#         created_at =current_time , 
#         updated_at =current_time )
    
#     db.add(payment_method)
#     db.commit()
#     db.refresh(payment_method)
#     return payment_method




@app.put('/user/{id}/' ,status_code=status.HTTP_202_ACCEPTED)
def user_updtae(id : int,  request : schema.UserCreateschema, user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db) ):
    fetch_data_payment_method = db.query(models.User).filter(models.User.id == id )
    print(fetch_data_payment_method.exists())
    if not fetch_data_payment_method.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'blog with this id{id} not found ')
    else:
        fetch_data_payment_method = db.query(models.User).filter(models.User.id == id ).update(dict(f_name  = request.f_name,l_name = request.l_name,email = request.email,User_group_types_id = request.user_group , updateed_at = current_time ))
        db.commit()
        data = db.query(models.User).filter(models.User.id == id ).first()
        return data
    


@app.delete('/user/{id}/' , status_code=status.HTTP_200_OK)
def user_delete(id ,response: Response, user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):    
    delete_data_payment = db.query(models.Users).filter(models.Users.id == id)
    if not delete_data_payment.first():
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')
    
    delete_data_payment = db.query(models.User).filter(models.User.id == id ).update(dict(status = False ))
    db.commit()
    return "Delete successfull"



@app.get('/user/', status_code=status.HTTP_200_OK)
def all_category(  user : _schema.User = _fastapi.Depends(_services.get_current_user),db : Session = Depends(get_db)):
    new_blog =  db.query(models.User).all()
    return new_blog

#This request is for return one data from user
@app.get('/user/{id}/' , status_code=status.HTTP_200_OK)
def by_id(  id : int , user : _schema.User = _fastapi.Depends(_services.get_current_user), db : Session = Depends(get_db)):
    new_blog = db.query(models.User).filter(models.User.id == id).first()
    if not new_blog:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with this id {id} not found ')

    return new_blog                                             

import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

from schema import UserCreate 
import services as _services
import schema as _schema

@app.post("/api/users")
async def create_user (user : _schema.UserCreate , db : _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(email = user.email  , db = db )
    if db_user:
        raise _fastapi.HTTPException(
            status_code= 400 , detail= "User with that email already exists"
        )    
    
    
    #create user
    
    user  = await _services.create_user(user = user , db = db )
    
    #return token 
    return await _services.create_torken(user = user )

@app.post("/api/token/")
async def generate_token(
    form_data  : _security.OAuth2PasswordRequestForm = _fastapi.Depends()  ,
    db : _orm.Session = _fastapi.Depends(_services.get_db)):
    
    user = await _services.authenticate_user(email = form_data.username , password= form_data.password , db = db )
    
    if not user :
        raise _fastapi.HTTPException(status_code=  401 , detail = "invalid Creadentials ")
    return await _services.create_torken(user = user )




#get current user 
# @app.get("/api/users/me" , response_model= _schema.User)
# async def get_user(user : _schema.User = _fastapi.Depends(_services.get_current_user)):
#     return user 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# this is for password varification 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#password change form after login 
@app.post('/passwordchange')
async def passchange(
    request : _schema.passchange ,
    user : _schema.User = _fastapi.Depends(_services.get_current_user),
    db : Session = Depends(get_db)):
    
    
    data = db.query(models.User).filter(models.User.email == user.email).first()
    if not verify_password(request.current_password, data.hashed_password):
        raise _fastapi.HTTPException(status_code=404 , detail= "password not match")
    else:
        print("match")
        hashed_password1 = _hash.bcrypt.hash(request.new_password)
        
        db.query(models.User).filter(models.User.email == user.email ).update(dict(hashed_password = hashed_password1 ,updateed_at = current_time ))
        db.commit()

    return "update_password"


templates = Jinja2Templates(directory="templates")


# this is for email field 
    
    
    
    
otpnumber=""
for i in range(6):
    otpnumber+=str(r.randint(1,9))



@app.post("/forgate_email/")
def read_item(email : Union[str, None] = Body(default=None), db : Session = Depends(get_db)):

    try :
        valid = _email_check.validate_email(email =email)
        email = valid.email
    except _email_check.EmailNotValidError:
        raise _fastapi.HTTPException(status_code=404 , detail= "please enter a valid email ")
    
    data = db.query(models.User).filter(models.User.email == email).first()
    if data :
        print("email found successfully")
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "hanishkaushal00@gmail.com"
        receiver_email = str(email)
        password = "ndqgzekzsgbkjqnd"
        SUBJECT = "varification mail"
        TEXT = f"http://localhost:8000/varification/{receiver_email}"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            
        data = models.Otp_table(
            email = str(email) , 
            otp = str(otpnumber)
        )
        
            
        db.add(data)
        db.commit()
        db.refresh(data)
        return email
    else:
        return 'mail not found'


@app.get("/varification/{email}", response_class=HTMLResponse)
async def read_item(request: Request , email , db : Session = Depends(get_db)):
    
    send_creadential = models.Otp_table(
        email = email ,
        status = False
    )
    db.add(send_creadential)
    db.commit()
    db.refresh(send_creadential)
    data = db.query(models.Otp_table).filter(models.Otp_table.status == False).first()
    if not data:
        
        return templates.TemplateResponse("forgate.html", {"request": request  , "email"  : email })

    else:
        return "your link expaired"
# check the otp is matched or not 
@app.post('/otpvalidation')
async def validation_otp(otp : int):
    print(otp , type(otp))
    print(otpnumber , type(otpnumber))
    if str(otp) == otpnumber :
        print('otp match successfully ')
        return "otp match successfully "
    else:
        print("otp did not match ")
        return "otp didn't match"
        
        
        
@app.post('/after_otp_set_password/')
async def set_password(
    password : str , 
    conf_password : str , 
    db : Session = Depends(get_db)):
        mail = read_item()
        print(mail , " $$$$$$$$$$")
        if len(password) < 4 :
            raise _fastapi.HTTPException(status_code=404 , detail= "password should be gretter than 4charcter and number  ")
        if password == conf_password:
            hashed_password = _hash.bcrypt.hash(password)
            db.query(models.User).update(dict(hashed_password =hashed_password  ))
            db.commit()
            return "password saved "
        
        else:
            raise _fastapi.HTTPException(status_code=404 , detail= "password should be gretter than 5 charcter and number  ")
            



@app.post("/Business_reaction/")
async def business_reactionn(request : schema.Business_reaction,user : _schema.User = _fastapi.Depends(_services.get_current_user) ,db : Session = Depends(get_db)):
    dict1 = {request.reaction_types_id : request.reaction_types_id }
    print('dsgdfnghjdfcjk')
    business_reactionn_post = models.Business_reaction(
        business_id = request.business_id ,
        reaction_types_id = dict1 ,
        user_id = request.user_id ,
        status  = True, 
        created_at = current_time , 
        updated_at = current_time )

    db.add(business_reactionn_post)
    db.commit()
    db.refresh(business_reactionn_post)
    
    
    return business_reactionn_post



@app.get("/Business_reaction/")
async def business_reaction_get(user : _schema.User = _fastapi.Depends(_services.get_current_user)  ,db : Session = Depends(get_db)):
    new_blog =  db.query(models.Business_reaction).all()
    return new_blog
    
    
