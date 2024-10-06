from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import json
from random import choice

app = FastAPI()
templates = Jinja2Templates(directory='templates')

def get_random_joke():
    jokes = []
    with open('jokes.json', 'r') as file:
        text = file.read()
        jokes = json.loads(text)
    
    return choice(jokes)['joke']

def get_joke():
    return get_random_joke()

@app.get('/')
def greet():
  return JSONResponse(status_code=200, content={"joke": get_joke()})


@app.get('/text/')
def greet_text():
  return get_joke()


@app.get('/pretty/', response_class=HTMLResponse)
def greet_pretty(request: Request):
  return templates.TemplateResponse('joke_template.html', {'request': request, 'joke': get_joke()})


