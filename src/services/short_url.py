from models.urls import ShortUrl as ShortUrlModel
from models.urls import ShortUrlHistory
from schemas.urls import OriginalUrl, ShortUrl

from .base import RepositoryDB


class Repository(RepositoryDB[ShortUrlModel, ShortUrlHistory, ShortUrl, OriginalUrl]):
    pass


urls_crud = Repository(ShortUrlModel, ShortUrlHistory)
