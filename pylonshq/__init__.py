def main(global_config, **settings):
    """ This function returns a Pylons WSGI application.
    """
    from paste.deploy.converters import asbool
    from pylons.configuration import Configurator
    from pylonshq.models import initialize_sql
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application "
                         "configuration.")
    initialize_sql(db_string, asbool(settings.get('db_echo')))
    config = Configurator(settings=settings)
    config.begin()
    config.add_cache()
    config.add_sessions()
    config.add_static_view(
        'static',
        'pylonshq:static/'
        )
    config.add_handler(
        'main',
        '/{action}',
        'pylonshq.handlers:MyHandler',
        )
    config.add_handler(
        'home',
        '/',
        'pylonshq.handlers:MyHandler',
        action='index'
        )
    config.end()
    return config.make_wsgi_app()
