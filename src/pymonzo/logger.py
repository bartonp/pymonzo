import logging

# Add some custom levels. Confidential will do everything including tokens.
logging.PRIVATE = 5
logging.addLevelName(logging.PRIVATE, 'PRIVATE')


def confidential(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.PRIVATE):
        self._log(logging.PRIVATE, message, args, **kwargs)


logging.Logger.confidential = confidential

# Default setup of some other loggers used.
for l in ['requests_oauthlib.oauth2_session', 'urllib3.connectionpool']:
    i = logging.getLogger(l)
    i.disabled = True

max_name_length = max([len(n) for n in logging._levelNames.keys() if isinstance(n, str)])
# Default logging setup with the formatting of the log
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)-{0}s] [%(name)s] [%(pathname)s:%(lineno)d] %(message)s'.format(max_name_length),
                    datefmt='%Y-%m-%dT%H:%M:%S')

__all__ = ['logging']
