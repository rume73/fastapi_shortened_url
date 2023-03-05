import logging
from logging import config as logging_config
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import LOGGING
from db.db import get_session
from schemas.urls import OriginalUrl, OriginalUrlsList, ShortUrl, ShortUrlsList
from services.short_url import urls_crud

logging_config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
router = APIRouter()

API_TAG_HEALTH = 'Service health'
API_TAG_URLS = 'Urls'


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ShortUrl,
    description='Получить сокращенный вариант переданного URL.',
    tags=[API_TAG_URLS]
)
async def create_short_url(
    original_url: OriginalUrl,
    db: AsyncSession = Depends(get_session)
) -> Any:
    """Получить сокращенный вариант переданного URL"""
    obj = await urls_crud.create(db=db, obj_in=original_url)
    logger.info(f'Short url created {obj.original_url} -> {obj.short_url}')
    return obj


@router.get(
    '/{url_id}/status',
    description="Вернуть статус использования URL",
    tags=[API_TAG_URLS],
)
async def get_url_status(
    url_id: str,
    full_info: bool = Query(default=False, alias='full-info'),
    max_size: int = Query(
        default=10,
        ge=1,
        alias='max-size',
        description='Query max size.'
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description='Query offset.'
    ),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """Вернуть статус использования URL."""
    obj = await urls_crud.get(db=db, url_id=url_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Url not found'
        )
    res = await urls_crud.get_status(
        db=db,
        db_obj=obj,
        limit=max_size,
        offset=offset,
        full_info=full_info
    )
    if isinstance(res, int):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'usages_count': res}
        )
    return res


@router.get(
    '/ping',
    description='Возвращает информацию о статусе доступности БД.',
    tags=[API_TAG_HEALTH],
)
async def health_db(db: AsyncSession = Depends(get_session)) -> Any:
    """Возвращает информацию о статусе доступности БД"""
    conn = await urls_crud.ping_db(db=db)
    return {'connection_db': conn}


@router.post(
    '/shorten',
    status_code=status.HTTP_201_CREATED,
    response_model=ShortUrlsList,
    description='Массовое сокращение ссылок.',
    tags=[API_TAG_URLS],
)
async def create_short_urls(
        target_urls: OriginalUrlsList,
        db: AsyncSession = Depends(get_session)
) -> Any:
    """Массовое сокращение ссылок"""
    return await urls_crud.bulk_create(db=db, obj_in=target_urls)


@router.get('/', description='Версия api.', tags=[API_TAG_HEALTH])
async def api_version():
    return {'version': 'v1'}


@router.get(
    '/{url_id}',
    response_class=RedirectResponse,
    description='Вернуть оригинальный URL.',
    tags=[API_TAG_URLS],
)
async def get_url(
    url_id: str,
    request: Request,
    db: AsyncSession = Depends(get_session)
) -> Any:
    """Вернуть оригинальный URL"""
    obj = await urls_crud.get(db=db, url_id=url_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Url not found'
        )
    await urls_crud.update_usage_count(db=db, db_obj=obj)
    client = f'{request.client.host}:{request.client.port}'
    await urls_crud.create_history(
        db=db,
        url_id=obj.id,
        client=client,
    )
    logger.info(f'Redirect {obj.short_url} -> {obj.original_url}')
    return obj.original_url
