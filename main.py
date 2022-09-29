# import uvicorn
from fastapi import FastAPI
from routes.cities_routes import router


def setup_routes(route_app: FastAPI):
    route_app.include_router(router)


def create_app() -> FastAPI:
    app_instance = FastAPI()
    setup_routes(route_app=app_instance)
    return app_instance


app = create_app()

# if __name__ == "__main__":
#     app = create_app()
#     uvicorn.run(app=app, host="0.0.0.0", port=8000)
