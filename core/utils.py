from importlib import import_module
import os
from schemas.base import ValidationSchema

# base_dir = os.path.dirname(os.path.abspath(__file__))


def load_models(directory: str = 'models') -> list[str]:
    files = ['{}.{}'.format(directory, x.name.split('.')[0]) for x in os.scandir(
        'models') if x.is_file() and x.name.endswith('.py')]
    return files


def format_validation_errors(errors):
    err = [ValidationSchema(
        field=e['loc'][-1], type=e['type'], msg=e['msg']).dict() for e in errors]
    return err


def load_signals() -> list[str]:
    files = ['signals.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'signals') if x.is_file() and x.name.endswith('.py')]
    return files


def register_signals() -> None:
    for signal in load_signals():
        import_module(signal)
