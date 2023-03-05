import logging
import logging.config
from typing import Callable

from fastapi import Request, Response, status

from core.logger import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class BlackListMiddleware:

    def __init__(self, black_list: list[str]):
        self._black_list = black_list

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        if request.client and request.client.host in self._black_list:
            logger.info(f'Client {request.client.host} from black list send request')
            return Response('Access denied', status_code=status.HTTP_403_FORBIDDEN)
        return await call_next(request)
