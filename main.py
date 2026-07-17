from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, computed_field
from typing import Optional

app = FastAPI()

class Patient(BaseModel):
    id: str
    name: str
    city: str
    age: int
    gender: str
    height: float
    weight: float

    @computed_field
    @property
    def bmi(self) -> float:
        # Prevent division by zero if height is incorrectly set to 0
        if self.height <= 0:
            return 0.0
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'  # Fixed logic error here
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None

def load_data():
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty dict if the file doesn't exist or is empty
        return {}

def save_data(data):
    with open('patients.json', 'w') as f:
        # Added indentation for readability in the JSON file
        json.dump(data, f, indent=4)

@app.get("/")
def patient():
    return {'message': 'Patient management system API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional patient management API'}

@app.get('/view_all_patients')
def view_all_patients():
    return load_data()

@app.get('/view_patient/{patient_id}')
def view_patient_patient(patient_id: str = Path(..., description='Enter the ID of patient', example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')
    
@app.get('/patient_name/{patient_id}')
def view_patient_name(patient_id: str = Path(..., description='Enter the ID of patient to get their only name', example='P001')):
    data = load_data()

    if patient_id in data:
        return {
            "name": data[patient_id]["name"],
            "age": data[patient_id]["age"],
            "city": data[patient_id]["city"]
        }
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str, order: str):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        # Fixed missing f-string syntax
        raise HTTPException(status_code=400, detail=f"Enter from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Enter valid order like asc or desc")
    
    data = load_data()

    sorted_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sorted_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Given ID already exists in database')
    
    # exclude is typically passed as a set in Pydantic V2
    data[patient.id] = patient.model_dump(exclude={'id'})

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

@app.put('/update/{patient_id}')
def updated_patient(patient_id: str, patient: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        # Fixed incorrect detail message and status code
        raise HTTPException(status_code=404, detail='Patient ID does not exist in database')
    
    extract_patient_info = data[patient_id]
    updated_patient_info = patient.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        extract_patient_info[key] = value
    
    extract_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**extract_patient_info)
    extract_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})

    data[patient_id] = extract_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient data updated successfully'})