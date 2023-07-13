from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from .user_router import router as user_router

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


app.include_router(user_router)

def openapi_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="FastAPI Swagger UI"
    )

app.add_route("/docs", openapi_html, name="swagger_ui")
