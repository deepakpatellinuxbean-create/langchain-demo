from pydantic import BaseModel

class Student(BaseModel):
    name: str

new_student = {"name": "nitish"}

student = Student(**new_student)

print(student)
