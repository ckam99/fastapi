
from fastapi import APIRouter, Request
from auth.urls import router as auth_urls
from books.urls import router as book_urls
from core.config.generics import view

router = APIRouter()

router.include_router(auth_urls)
router.include_router(book_urls, prefix='/books')
# router.include_router(
#     auth_urls,
#     responses={404: {"description": "Not found"}},
# )


@router.get('/', include_in_schema=False)
def index(request: Request):
    return view.TemplateResponse('index.html', {'request': request})
