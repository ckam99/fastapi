import os
from schemas.base import ValidationSchema


def load_models(directory: str = 'models'):
    files = ['{}.{}'.format(directory, x.name.split('.')[0]) for x in os.scandir(
        'models') if x.is_file() and x.name.endswith('.py')]
    return files


def format_validation_errors(errors):
    err = [ValidationSchema(
        field=e['loc'][-1], type=e['type'], msg=e['msg']).dict() for e in errors]
    return err
