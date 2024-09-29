from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get_joke():
    return "This is a joke!"