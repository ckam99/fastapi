from fastapi.templating import Jinja2Templates
from core.settings import TEMPLATE_FOLDER

view = Jinja2Templates(directory=TEMPLATE_FOLDER)
