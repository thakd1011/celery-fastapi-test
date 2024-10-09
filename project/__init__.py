from fastapi import FastAPI

def create_app() -> FastAPI:
    """
    Create FastAPI app using factory pattern
    """
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app