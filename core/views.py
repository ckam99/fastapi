from fastapi.templating import Jinja2Templates
from fastapi import Request

template = Jinja2Templates(directory='resources/templates')


def render_template(request: Request, template_name: str, context: dict = None):
    context = {} if context is None else context
    context['request'] = request
    return template.TemplateResponse(template_name, context)
