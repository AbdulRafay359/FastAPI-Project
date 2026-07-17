from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int  

def inserting_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted")


patient_info = {
    "name": "Abdul Rafay",
    "age": 22
}


patient = Patient(**patient_info)
inserting_data(patient)