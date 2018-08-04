import os
import logging
import logging.config
import flask


def make_app():

    app = flask.Flask(import_name='unigator_ctl')

    # Get application configuration.
    app.config.from_object('unigator_ctl.settings.default')
    if os.environ.get('UNIGATOR_SETTINGS'):
        app.config.from_envvar('UNIGATOR_SETTINGS')

    # Get logging configuration.
    app.config.from_object('unigator.logconfig.default')
    if os.environ.get('UNIGATOR_LOGCONFIG'):
        app.config.from_envvar('UNIGATOR_LOGCONFIG')

    # Apply logging configuration.
    logging.config.dictConfig(app.config['LOGGING'])
