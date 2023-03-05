import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.v1 import base
from core import config
from core.config import app_settings
from core.middleware import BlackListMiddleware

app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/swagger',
    openapi_url='/api/swagger.json',
    default_response_class=ORJSONResponse,
)

black_list = BlackListMiddleware(black_list=app_settings.black_list)

app.add_middleware(BaseHTTPMiddleware, dispatch=black_list)
app.include_router(base.router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.project_host,
        port=app_settings.project_port,
    )
