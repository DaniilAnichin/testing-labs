import json
from logging import getLogger


logger = getLogger('main')


class BaseExceptionManager(object):
    exception_groups: list = ['critical', 'regular', 'io']
    group_types: dict = None
    counters: dict = None

    def __init__(self, config_path: str=None):
        self.counters = {key: 0 for key in self.exception_groups}

        if config_path:
            with open(config_path, 'r') as f:
                data = json.load(f)
            self.group_types = {
                key: tuple(
                    [
                        eval(err)
                        for err
                        in data.get(key, [])
                    ]
                )
                for key
                in self.exception_groups
            }

    def process_exception(self, exception: Exception):
        if not isinstance(exception, Exception):
            raise TypeError(f'Exception "{exception!r}" has wrong base class')

        try:
            if self.is_critical(exception):
                self.counters['critical'] += 1
                self.send_report(exception)
            else:
                self.counters['regular'] += 1
        except IOError:
            self.counters['io'] += 1

    def is_critical(self, exception: Exception) -> bool:
        if isinstance(exception, self.group_types['critical']):
            return True
        return False

    def send_report(self, exception: Exception):
        logger.error(f'Note: "{exception!r}" occurred!')
        if False:
            # Simulating IOError
            raise IOError
