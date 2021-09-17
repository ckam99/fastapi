import os


def auto_load_models():
    files = ['models.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'models') if x.is_file() and x.name.endswith('.py')]
    return files
