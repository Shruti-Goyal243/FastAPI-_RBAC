# import motor.motor_asyncio
from pymongo import MongoClient
from sqlmodel import Session
# MONGO_DETAILS = "mongodb://localhost:27017"

client = MongoClient("mongodb://localhost:27017",8000)

database = client.students

student_collection = database.get_collection("students_collection")
user_collection = database.get_collection("user_collection")
# user_role_collection = database.get_collection("user_role_collection")


# def get_db():
#     with Session(database) as session:
#         yield session
# helpers
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname" : student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "gpa": student["gpa"]
    }
    

def user_helper(user) -> dict:
    return{
        "fullname": user["fullname"],
        "email": user["email"],
        "password": user['password']

    }