from fastapi import FastAPI, status,Depends,HTTPException,  File, UploadFile
import jwt
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional,Dict,Union
from typing_extensions import Annotated
from pydantic import BaseModel, AnyUrl
from fastapi.encoders import jsonable_encoder

from fastapi.responses import JSONResponse
from owlready2 import onto_path, get_ontology, destroy_entity, DataProperty
from owlready2.namespace import Thing
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
#from tortoise import fields 
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_queryset_creator
import itertools

import os
from conf import *
from owl_class import *
#from api_class import *
#from license_oper import *
from api_license_class_oper import *
from util import *
#JWT_SECRET = 'myjwtsecret'

app = FastAPI(
    title="License Checker",
    description="The License Checker provides information about FLOSS software licenses and helps you to identify compatible licenses.",
    version="version tbd"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
#license_request = pydantic_model_creator(CompLic)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
sql_conn = create_connection()
async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    log.debug("Fetching token...")
    user = await authenticate_user(form_data.username, form_data.password)
    log.debug("Fetching token...")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    user_obj = await User_Pydantic.from_tortoise_orm(user)
    log.debug("User:{}".format(user))
    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {'access_token' : token, 'token_type' : 'bearer'}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
       
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
        print(User.get(id=payload.get('id')))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return await User_Pydantic.from_tortoise_orm(user)
    
async def get_user_meta(username):
    """
    To Fetch current user metaData
    """
    
    

    
    '''
    user = await User_Pydantic.from_queryset_single(User.get(username=username))
   
    return user.dict()
    user = await User_Pydantic.from_tortoise_orm(user)
    return user.dict()
    #return await User.get(username=username)
    '
    test = await User_Pydantic.from_queryset_single(User.get(id=1))
    if test == "admin":
        log.debug(".....................Passs")
    log.debug(test)
    '''
    user = await User.get(username=username)
    if user.verify_role("admin"):
        log.debug("Yes, it is admin...")    
    else:
        print("role is:{}".format(user))
    return user
@app.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash), role=user.role)
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user    

register_tortoise(
    app, 
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)

@app.post("/licenses/add/", tags=["Changing the license ontology - for admins only"])
def add_license(newLicense: License, user: User_Pydantic = Depends(get_current_user) ):
    '''
    Adds a license to the ontology. Only for admins.

    **work in progress, not working yet**
    '''
    
    # fetching USER role from DB
    
    #if user.role == "admin"
    roles = user.role.split(',')
    log.debug(roles)
    if "admin"  in roles or "write" in roles:
        create_new_license_object(newLicense)
        return get_license_object(newLicense.id) 
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Not Authorized For Making Changes In Ontology')
    


@app.get("/licenses/", response_model=List[License], tags=["Accessing information from the license ontology"])
def get_all_licenses():
    '''
    Returns all available software licenses as License-Objects
    '''
    licenses = []
    for lic in lic_list():
        if get_license_object(lic) is not None:
            licenses.append(get_license_object(lic))
    return licenses


@app.get("/licenseList/", tags=["Accessing information from the license ontology"])
def get_license_list():
    '''
    Returns all available software licenses as strings
    '''
    return list_all_licenses_as_strings()


@app.get("/licenses/{license_id}", tags=["Accessing information from the license ontology"])
def get_license(license_id: str):
    '''
    Returns a certain license as a License-Object
    '''
    var = get_license_object(license_id)
    if var is not None:
        return var
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"The license id {license_id} does not exist")


@app.get("/licenses/{license_id}/conditions", tags=["Accessing information from the license ontology"])
def get_license_conditions(license_id: str):
    '''
    Returns the conditions of a certain license.
    '''
    var = get_license_object(license_id)
    if var is not None:
        return var.conditions
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"The license id {license_id} does not exist")


@app.get("/licenses/{license_id}/limitations", tags=["Accessing information from the license ontology"])
def get_license_limitations(license_id: str):
    '''
    Returns the limitations of a certain license.
    '''
    var = get_license_object(license_id)
    if var is not None:
        return var.limitations
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"The license id {license_id} does not exist")


@app.get("/licenses/{license_id}/permissions", tags=["Accessing information from the license ontology"])
def get_license_permissions(license_id: str):
    '''
    Returns the permissions of a certain license.
    '''
    var = get_license_object(license_id)
    if var is not None:
        return var.permissions
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"The license id {license_id} does not exist")


@app.get("/licenses/{license_id}/license_type", tags=["Accessing information from the license ontology"])
def get_license_type(license_id: str):
    '''
    Returns the type of a certain license.
    '''
    var = get_license_object(license_id)
    if var is not None:
        kkk = return_correct_case(license_id)
        fff = slo[kkk]
        return fff.hasLicenseType[0].name
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"The license id {license_id} does not exist")


@app.get("/licenses/{license_id}/osi_popular", tags=["Accessing information from the license ontology"])
def check_osi_popularity(license_id: str):
    '''
    Returns TRUE if the license is among the popular licenses according to the Open Software Initiative.
    '''
    var = get_license_object(license_id)
    if var is not None:
        kkk = return_correct_case(license_id)
        fff = slo[kkk]
        return fff.isOsiPopular
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"The license id {license_id} does not exist")


@app.get("/condition", tags=["Accessing information from the license ontology"])
def get_condition():
    '''
    Returns all popular licenses according to the Open Software Initiative.
    '''
    iris = list(slo.search(type=slo.Condition))
    conditions = clean_iri(iris)

    return conditions
    
    
@app.get("/permission", tags=["Accessing information from the license ontology"])
def get_permission():
    '''
    Returns all popular licenses according to the Open Software Initiative.
    '''
    iris = list(slo.search(type=slo.Permission))
    permission = clean_iri(iris)

    return permission
    

@app.get("/limitation", tags=["Accessing information from the license ontology"])
def get_limitation():
    '''
    Returns all popular licenses according to the Open Software Initiative.
    '''
    iris = list(slo.search(type=slo.Limitation))
    limitation = clean_iri(iris)

    return limitation
    

@app.get("/popular", tags=["Accessing information from the license ontology"])
def return_osi_popular_licenses():
    '''
    Returns all popular licenses according to the Open Software Initiative.
    '''
    uuu = slo.search(isOsiPopular=True)
    popular_list = []
    for x in uuu:
        popular_list.append(x.name)

    return popular_list

@app.get("/types/{license_type}", tags=["Accessing information from the license ontology"])
def return_licenses_for_type(license_type: str):
    '''
    Returns a list of licenses of a certain type.
    '''
    valid = {"permissive", "public domain", "copyleft"}
    x = license_type.lower()
    if x not in valid:
        raise ValueError("License Type must be one of %r." % valid)
    else:
        if x == "permissive" or x == "copyleft":
            y = x.capitalize()
        elif x == "public domain":
            y = x.title().replace(" ", "")

        uuu = slo.search(hasLicenseType=slo[y])
        list = []
        for z in uuu:
            list.append(z.name)
        return list


@app.post("/licenses/check/detail", tags=["Accessing information from the license ontology"])
def check_license(usedLicenses: List[str]):
#def check_license(usedLicenses: license_request):
#def check_license(usedLicenses: CompLic):

    '''
    # two endpoint
    1. only compatible
    2. all result
    Returns which licenses are compatible with a certain license.

    **Basic functionality is working. Currently returns hard coded compatibilities.**
    <reason>" → "X is compatible with y, see <reason> for details."
    '''
    #usedLicenses = license_request['license']
    #log.debug(license_request)
    output = {}
    compatibleLicenses = []
    unknownLicenses = []
    
    for licId in usedLicenses:
        lic = get_license_object(licId)
        if lic is  None:
            unknownLicenses.append(licId)
        else:
            comp_lics = check_compatiblity(licId)
            compatibleLicenses = comp_lics if len(compatibleLicenses) == 0 else intersection(compatibleLicenses,
                                                                                             comp_lics)
    if len(unknownLicenses) > 0:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            content=f"{unknownLicenses} is/are not a part of the Software License API")    
    
    output["compatible"] = compatibleLicenses
    output["reasons"] = []
    cartesian_product =  itertools.product(usedLicenses, compatibleLicenses)
    for lg in cartesian_product:
        out = query(sql_conn, lg[0],lg[1])
        if len(out) !=0:
            message = lg[0]+" is compatible with "+lg[1] + ", and Reason:"+out[0][0]
            output["reasons"].append(message)
        log.debug(out)
    
    possible_licenses = []
    for x in list_all_licenses_as_objects():
        if x not in find_incompatible_licenses_all(usedLicenses):
            possible_licenses.append(x.name)
            
    output["possible compatible"] = possible_licenses
    incompatible_license = []
    incompatible_license = find_incompatible_licenses_all(usedLicenses)
    #output['Not compatible'] = incompatible_license
    log.debug(output)
    #json_compatible_item_data = jsonable_encoder(output)
    return output
    #return json.dumps(output)
    #return output

@app.post("/licenses/check/", response_model=List[str], tags=["Accessing information from the license ontology"])
def check_license(usedLicenses: List[str]):
#def check_license(usedLicenses: license_request):
#def check_license(usedLicenses: CompLic):

    '''
    # two endpoint
    1. only compatible
    2. all result
    Returns which licenses are compatible with a certain license.


   
    **Basic functionality is working. Currently returns hard coded compatibilities.**
    '''
    #usedLicenses = license_request['license']
    #log.debug(license_request)
 
    output = {}
    compatibleLicenses = []
    unknownLicenses = []
    usedLicenses.sort()
    #print("Used Licenses",usedLicenses)
    

    for licId in usedLicenses:
        lic = get_license_object(licId)
        
        
        if lic is  None:
            unknownLicenses.append(licId)
        else:
            
            comp_lics = check_compatiblity(licId)
            compatibleLicenses = comp_lics if len(compatibleLicenses) == 0 else intersection(compatibleLicenses,
                                                                                             comp_lics)
    if len(unknownLicenses) > 0:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            content=f"{unknownLicenses} is/are not a part of the Software License API")    
    
   
    print(compatibleLicenses)
    return compatibleLicenses



@app.put("/licenses/{license_id}", tags=["Changing the license ontology - for admins only"])
def update_license(license_id: str, newLicense: License, user: User_Pydantic = Depends(get_current_user)):
    '''
    Changes the properties of a certain license. Only for admins.

    **work in progress, not working yet**
    '''
    roles = user.role.split(',')
    if "admin"  in roles or "update" in roles:
        case = return_correct_case(license_id)
        lic_upd = get_license_object(license_id)
        if case not in license_list_upper:
            if lic_upd is not None:
                destroy_entity(slo[license_id])
                slo.save()
                create_new_license_object(newLicense)
                return get_license_object(license_id)
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                    content=f"The license id {license_id} does not exist")
        else:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f"The license id {license_id} cannot be updated")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Not Authorized For Making Changes In Ontology')

@app.delete("/licenses/{license_id}", tags=["Changing the license ontology - for admins only"])
def delete_license(license_id: str, user: User_Pydantic = Depends(get_current_user)):
    '''
    Deletes a certain license. Only for admins.

    **work in progress, not working yet**
    '''
    roles = user.role.split(',')
    if "admin" in roles or "delete"  in roles:
        
        case = return_correct_case(license_id)
        lic_del = get_license_object(case)
        if case not in license_list_upper:
            if lic_del is not None:
                destroy_entity(slo[case])
                slo.save()
                return get_all_licenses()
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                    content=f"The license id {license_id} does not exist")
        else:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f"The license id {license_id} cannot be deleted")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Not Authorized For Making Changes In Ontology'
        )
        

@app.post("/licenses/rank/", response_model=List[str], tags=["Accessing information from the license ontology"])
def rank(license_name, counts):
#def check_license(usedLicenses: license_request):
#def check_license(usedLicenses: CompLic):

    '''
    # two endpoint
    1. only compatible
    2. all result
    Returns which licenses are compatible with a certain license.


   
    **Basic functionality is working. Currently returns hard coded compatibilities.**
    '''
    #usedLicenses = license_request['license']
    #log.debug(license_request)
    all_licenses_object_list = slo.search(type=slo.SoftwareLicense)
    ids = []
    names = []
    for ls in all_licenses_object_list:
        ids.append(remove_prefix(str(ls)))
        names.append(ls.licenseName)
    
    lic_2_vec = {}
    for id in ids:
        lic_2_vec[id] = word2vec(id)
    scores = []
    
    ipn_word2vec = word2vec(license_name)
    for key, val in lic_2_vec.items():
        scores.append((key, cosdis(ipn_word2vec,val)))
    scores.sort(key=lambda tup: tup[1],reverse=True)
    #print(scores)
    ranked = []
    scored = []
    for val in scores:
        print(val)
        ranked.append(val[0])
        scored.append(val[1])
    rslt = ranked[:int(counts)]
    return rslt


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    lic_info=check_python_dependency(contents)
    return {"filename": file.filename,
            "Content": lic_info
            }




