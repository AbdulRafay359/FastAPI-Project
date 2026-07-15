from fastapi import FastAPI ,Path, HTTPException
import json

app = FastAPI()


def load_data():
    with open('patients.json' , 'r') as f:
        data = json.load(f)

    return data


@app.get("/")
def patient():
    return {'message' : 'Patient management system API'}

@app.get('/about')
def about():
    return {'message' : 'A fully functional patient management API'}

@app.get('/view_all_patients')
def view_all_patients():
    data = load_data()

    return data

@app.get('/view_patient/{patient_id}')
def view_patient_patient(patient_id : str = Path(..., description = 'Enter the ID of patient' ,example = 'P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404 , detail = 'patient not found')
    
@app.get('/patient_name/{patient_id}')
def view_patient_name(patient_id : str = Path(..., description = 'Enter the ID of patient to get their only name' ,example = 'P001')):
    data = load_data()

    if patient_id in data:
        return {
            "name" : data[patient_id]["name"],
            "age" : data[patient_id]["age"],
            "city" : data[patient_id]["city"]
            }
    raise HTTPException(status_code = 404 , detail = 'patient not found')





@app.get('/sort')
def sort_patients(sort_by : str , order : str):
    valid_fields = ['height' , 'weight' , 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400 , detail = "Enter from {valid_fields}")
    
    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code = 400 , detail = "Enter valid order like asc or desc")
    
    data = load_data()

    sorted_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sorted_order)

    return sorted_data