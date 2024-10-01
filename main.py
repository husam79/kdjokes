from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
templates = Jinja2Templates(directory='templates')

def get_joke():
    return "This is my new joke!!"

@app.get('/')
def greet():
  return JSONResponse(status_code=200, content={"joke": get_joke()})


@app.get('/text/')
def greet_text():
  return get_joke()


@app.get('/pretty/', response_class=HTMLResponse)
def greet_pretty(request: Request):
  return templates.TemplateResponse('joke_template.html', {'request': request, 'joke': get_joke()})


