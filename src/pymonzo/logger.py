import logging


def getLogger(level=logging.INFO):
    logging.basicConfig(level=level,
                        format='%(asctime)s | %(name)s | %(levelname)s :- %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')

    for l in ['requests_oauthlib.oauth2_session', 'urllib3.connectionpool']:
        i = logging.getLogger(l)
        i.setLevel(level=logging.CRITICAL)


    return logging

if __name__ == '__main__':
    logger = getLogger(level=logging.DEBUG)
    logger.info('Bacon')
    logger.debug('Cheese')
