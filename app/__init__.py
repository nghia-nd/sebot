from fastapi import FastAPI

api = FastAPI()


def register_routes():
    from .routes import create_chat


register_routes()
