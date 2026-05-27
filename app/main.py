from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def health():
    return {"status": "Healthy"}

@app.post("/employees")
def create_employee():
    pass

@app.get("/employees")
def get_employee():
    pass

@app.delete("/employees/{id}")
def delete_employee(id: int):
    pass