# import click
# import os
# from flaskserver.extensions import db, bootstrap
#
# def register_commands(app):
#     @app.cli.command()
#     @click.option('--drop', is_flag=True, help='Create after drop.')
#     def forge(drop):
#         """Initialize the database."""
#         from flaskserver.fakes import fake_admin, fake_admission
#
#         db.drop_all()
#         db.create_all()
#
#         click.echo('Generating the administrator..')
#         fake_admin()
#
#         click.echo('Generating the admission')
#         fake_admission()
#
#         click.echo('Done.')