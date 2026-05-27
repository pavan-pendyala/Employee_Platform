from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
app = FastAPI()

Instrumentator().instrument(app).expose(app)
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