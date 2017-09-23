import logging


def getLogger(level=logging.INFO):
    logging.basicConfig(level=level,
                        format='[%(asctime)s] [%(name)s] [%(pathname)s:%(lineno)d] %(levelname)s :- %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')

    # Default setup of some other loggers used.
    for l in ['requests_oauthlib.oauth2_session', 'urllib3.connectionpool']:
        i = logging.getLogger(l)
        i.setLevel(level=logging.CRITICAL)

    return logging
