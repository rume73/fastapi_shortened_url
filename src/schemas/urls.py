from datetime import datetime

from pydantic import BaseModel, HttpUrl


class OriginalUrl(BaseModel):
    """Изначальный урл"""
    original_url: HttpUrl

    class Config:
        orm_mode = True


class ShortUrl(BaseModel):
    """Укороченый урл"""
    url_id: str
    short_url: HttpUrl

    class Config:
        orm_mode = True


class UrlHistoryShortInfo(BaseModel):
    """Колличесво переходов"""
    usages_count: int

    class Config:
        orm_mode = True


class UrlHistoryInfo(BaseModel):
    """Подробная история переходов"""
    use_at: datetime
    client: str
    id: str
    short_url: str

    class Config:
        orm_mode = True


class UrlHistoryFullInfo(BaseModel):
    """Подробная история переходов"""
    __root__: list[UrlHistoryInfo]


class OriginalUrlsList(BaseModel):
    """Пачка урлов"""
    __root__: list[OriginalUrl]


class ShortUrlsList(BaseModel):
    """Пачка сокращенных урлов"""
    __root__: list[ShortUrl]
