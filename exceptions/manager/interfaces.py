import json
from logging import getLogger
from abc import ABC

logger = getLogger('main')


class BaseCriticalChecker(ABC):
    exception_groups: list = ['critical', 'regular', 'io']
    group_types: dict = None

    def is_critical(self, exception: Exception) -> bool:
        raise NotImplementedError


class CriticalChecker(BaseCriticalChecker):
    def __init__(self, config_path: str=None, group_types: dict=None):
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
        elif group_types:
            self.group_types = {
                key: tuple(group_types[key])
                for key
                in group_types.keys()
                if key in self.exception_groups
            }
        else:
            raise ValueError('Either group_types or config_path should be provided')

    def is_critical(self, exception: Exception) -> bool:
        if isinstance(exception, self.group_types['critical']):
            return True
        return False


class BaseReportSender(ABC):
    def send_report(self, exception):
        raise NotImplementedError


class ServerMailReportSender(BaseReportSender):
    def send_report(self, exception: Exception):
        logger.error(f'Note: "{exception!r}" occurred!')
        if False:
            # Simulating IOError
            raise IOError
