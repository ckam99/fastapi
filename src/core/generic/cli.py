import click
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv('.env')


@click.group()
def commands():
    pass


@click.command(help='Run server')
@click.option('--port', type=int, default=8000, help='Server port')
@click.option('--host', type=str, default='0.0.0.0', help='Server host')
@click.option('--reload', type=bool, default=True, help='Reload server after file changed')
def serve(port, host, reload):
    debug = os.environ.get('DEBUG', True)
    uvicorn.run(
        'core:app',
        port=port,
        host=host,
        debug=debug,
        reload=reload,
        # lifespan='on'
    )


commands.add_command(serve)
