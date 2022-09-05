from re import A
from fastapi import FastAPI, Body, Depends
from bson.objectid import ObjectId
from .model import UserSchema, UserLoginSchema
from .database import student_collection, student_helper, user_collection
from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import JWT_ALGORITHM, JWT_SECRET, signJWT
import json
from bson import json_util
import json
import jwt

app = FastAPI()

# PERMISSION = {"1" : "admin",
#               "2" : "student"}

@app.post("/user/signup", tags=["User"])
async def create_user(user: UserSchema = Body(...)):
    user_emails = []
    
    result = user_collection.find()
    for i in result:
        user_emails.append(i["email"])
        user_data = json.loads(user.json())
        if user_data["email"] not in user_emails:
            user_details = user_collection.insert_one(user_data)
            # import pdb; pdb.set_trace() 
            # user_role_detail = user_role_collection.insert_one({"role":user_data["role"], "email":user_data["email"]})   
        else:
            return {"result": "This Email is Already Exist.."}
    create_data = user_collection.find({"_id": user_details.inserted_id})
    result = {}
    for data in create_data:
        result.update(data)
    return {'result': json.loads(json_util.dumps(result))}


def check_user(data: UserLoginSchema):
    check_data = user_collection.find({"email": data.email, "password": data.password})
    user_details = list(check_data)
    if len(user_details) != 0:
        return True
    return False

@app.post("/user/login", tags=["User"])
async def user_login(user : UserLoginSchema = Body(...)):
    # user_data = user.json()
    if check_user(user):
        return signJWT(user.email)
    else:
        return {"message" : "Invalid Credentials"}
    

# def get_user_by_email(email:str)->Optional[User]:
#     # import pdb;pdb.set_trace()
#     user = user_collection.find_one({"email": email})
#     if user["role" == "admin"]:
#         return True
#     return False

    
    
async def get_current_user_admin(token: str = Depends(JWTBearer())) -> UserSchema:
    payload = jwt.decode(
        token, JWT_SECRET , algorithms=[JWT_ALGORITHM]
    )
    user = user_collection.find_one({"email": payload['email']})
    if user["role"] == 'admin':
        return True
    return False

async def get_current_user_superadmin(token: str = Depends(JWTBearer())) -> UserSchema:
    payload = jwt.decode(
        token, JWT_SECRET , algorithms=[JWT_ALGORITHM]
    )
    user = user_collection.find_one({"email" : payload['email']})
    if user["role"] == 'superAdmin':
        return True
    return False
    
async def get_current_user_manager(token: str = Depends(JWTBearer())) -> UserSchema:
    payload = jwt.decode(
        token, JWT_SECRET , algorithms=[JWT_ALGORITHM]
    )
    user = user_collection.find_one({"email": payload['email']})
    if user["role"] == 'manager':
        return True
    return False

    # token_data = TokenPayload(**payload)
    
    # user = get_user_by_email(payload['email'])
    # if not user:
    #      raise HTTPException(
    #         status_code = status.HTTP_403_FORBIDDEN,
    #         detail="Could not validate credentials",
    #      )

# @app.post('/test-token', summary="Test if the access token is valid")
# def test_token(user: User = Depends(get_current_user)):
#     return user

@app.post("/student", dependencies=[Depends(JWTBearer())], tags=["Student Details"], response_description=" Add Student")
async def add_student(student: dict, current_user_admin: UserSchema = Depends(get_current_user_admin), current_superadmin:UserSchema=Depends(get_current_user_superadmin)):
    if current_user_admin or current_superadmin:
        student = student_collection.insert_one(student)
        new_student = student_collection.find_one({"_id": student.inserted_id})
        return student_helper(new_student)
    else:
        return {"result" : "User not Authorized for this Task!!!"}

    

@app.get("/student", dependencies=[Depends(JWTBearer())], tags=["Student Details"], response_description="All Student List.")
async def student_list( current_user_admin: UserSchema = Depends(get_current_user_admin),current_user_manager: UserSchema = Depends(get_current_user_manager), current_superadmin:UserSchema=Depends(get_current_user_superadmin)):
    if current_user_admin or current_user_manager or current_superadmin:
        students = []
        for student in student_collection.find():
            students.append(student_helper(student))
        return students
    else:
        return {"result" : "User not Authorized for this Task!!!!!"}


@app.get("/student/{id}", dependencies=[Depends(JWTBearer())], tags=["Student Details"], response_description="Student data retrieved")
async def get_student(student_id,current_user_admin: UserSchema = Depends(get_current_user_admin),current_user_manager:UserSchema = Depends(get_current_user_manager), current_superadmin:UserSchema=Depends(get_current_user_superadmin)):
    if current_user_admin or current_user_manager or current_superadmin:
        student = student_collection.find_one({"_id": ObjectId(student_id)})
        if student:
            return student_helper(student)
        else:
            return "Student doesn't exist."
    else:
        return {"result" : "User not Authorized for this Task!!!!!"}




@app.patch("/{id}", dependencies=[Depends(JWTBearer())], tags=["Student Details"])
async def update_student(student_id: str, data: dict,current_user_manager: UserSchema = Depends(get_current_user_manager), current_superadmin:UserSchema=Depends(get_current_user_superadmin)):
    if current_user_manager or current_superadmin:
        if len(data) < 1:
            return False
        student = student_collection.find_one({"_id": ObjectId(student_id)})
        if student:
            updated_student = student_collection.update_one(
                {"_id": ObjectId(student_id)}, {"$set": data}
            )
            if updated_student:
                return "Student update successfully"
            return False
    else:
        return {"result" : "User not Authorized for this Task!!!!!"}


@app.delete("/{id}", dependencies=[Depends(JWTBearer())], tags=["Student Details"], response_description="Student data deleted from the database")
async def delete_student_data(student_id: str,current_user_manager: UserSchema = Depends(get_current_user_manager), current_superadmin:UserSchema=Depends(get_current_user_superadmin)):
    if current_user_manager or current_superadmin:
        student = student_collection.find_one({"_id": ObjectId(student_id)})
        if student:
            student_collection.delete_one({"_id": ObjectId(student_id)})
            return "Student deleted successfully"
    else:
        return {"result"  :"USer not authorized for this task!!!"}
