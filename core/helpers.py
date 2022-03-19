
from importlib import import_module
import os


root_dir = os.path.dirname(os.path.abspath(__file__))


def load_models():
    files = ['models.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'models') if x.is_file() and x.name.endswith('.py')]
    return files


def load_tasks():
    files = ['tasks.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'tasks') if x.is_file() and x.name.endswith('.py')]
    return files


def load_signals():
    files = ['signals.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'signals') if x.is_file() and x.name.endswith('.py')]
    return files


def register_signals():
    for signal in load_signals():
        import_module(signal)
