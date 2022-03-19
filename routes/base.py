from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from core.views import render_template
from .auth import router as auth
from tasks.users import send_confirmation_email

router = APIRouter()
router.include_router(auth, prefix='/auth', tags=['Authentication'])


@router.get('/', include_in_schema=False, )
def home(request: Request):
    return render_template(request, "index.html", {"request": request})


@router.post("/email")
async def simple_send(
    email: str
) -> JSONResponse:
    send_confirmation_email.delay(email)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
