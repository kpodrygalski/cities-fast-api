# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.cities_routes import router

origins = ["http://127.0.0.1:5173", "localhost:5173", "http://localhost:5173"]


def setup_routes(route_app: FastAPI):
    route_app.include_router(router)


def create_app() -> FastAPI:
    app_instance = FastAPI()
    setup_routes(route_app=app_instance)
    return app_instance


app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if __name__ == "__main__":
#     app = create_app()
#     uvicorn.run(app=app, host="0.0.0.0", port=8000)
