from fastapi import FastAPI ,Path
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
    return{"error" : "patient not found"}
    
@app.get('/patient_name/{patient_id}')
def view_patient_name(patient_id : str = Path(..., description = 'Enter the ID of patient to get their only name' ,example = 'P001')):
    data = load_data()

    if patient_id in data:
        return {
            "name" : data[patient_id]["name"],
            "age" : data[patient_id]["age"],
            "city" : data[patient_id]["city"]
            }
    return{"error" : "patient not found"}