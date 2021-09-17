import click
import uvicorn


@click.group()
def commands():
    pass


@click.command(help='Run server')
@click.option('--app', type=str, default='tortoise', help='App')
@click.option('--port', type=int, default=8000, help='Server port')
@click.option('--host', type=str, default='0.0.0.0', help='Server host')
@click.option('--debug', type=bool, default=True, help='True for development mode')
@click.option('--reload', type=bool, default=True, help='Reload server after file changed')
def serve(app, port, host, debug, reload):

    uvicorn.run(
        f'{app}.main:app',
        port=port,
        host=host,
        debug=debug,
        reload=reload
    )


commands.add_command(serve)

if __name__ == '__main__':
    commands()
