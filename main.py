from fastapi import FastAPI, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import json
from random import choice
from sqlmodel import select, SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from typing import Annotated
from joke import Joke
from sqlalchemy import func


sqlite_file_name = "jokes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
   with Session(engine) as session:
      yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_database_and_tables():
   SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
   create_database_and_tables()
   yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory='templates')

def get_random_joke(session: SessionDep) -> Joke | None:
    return session.exec(select(Joke).order_by(func.random())).first()

@app.get('/')
def get_joke(session: SessionDep):
  joke = get_random_joke(session=session)
  return JSONResponse(status_code=200, content={"joke": joke.content})


@app.get('/text/')
def greet_text(session: SessionDep) -> str | None:
  joke = get_random_joke(session=session)
  return joke.content


@app.get('/pretty/', response_class=HTMLResponse)
def greet_pretty(request: Request, session: SessionDep):
  joke = get_random_joke(session=session)
  return templates.TemplateResponse('joke_template.html', {'request': request, 'joke': joke.content})

@app.post('/')
def post_joke(joke: Joke, session: SessionDep) -> Joke:
    session.add(joke)
    session.commit()
    session.refresh(joke)
    return joke
