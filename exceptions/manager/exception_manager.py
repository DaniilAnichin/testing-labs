import json
from logging import getLogger

from .interfaces import BaseCriticalChecker

logger = getLogger('main')


class BaseExceptionManager(object):
    counters: dict = None

    def __init__(self, critical_checker: BaseCriticalChecker):
        self.critical_checker = critical_checker
        self.counters = {key: 0 for key in self.critical_checker.exception_groups}

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
        return self.critical_checker.is_critical(exception)

    def send_report(self, exception: Exception):
        logger.error(f'Note: "{exception!r}" occurred!')
        if False:
            # Simulating IOError
            raise IOError
