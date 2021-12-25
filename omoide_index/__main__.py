# -*- coding: utf-8 -*-
"""Entry point.
"""
import click
import uvicorn


@click.command(help='Start omoide index server')
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=9000)
def main(host: str, port: int):
    """Entry point.
    """
    uvicorn.run('omoide_index.app:app', host=host, port=port)


if __name__ == '__main__':
    main()
