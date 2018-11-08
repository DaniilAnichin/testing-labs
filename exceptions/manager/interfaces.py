import json
from logging import getLogger


logger = getLogger('main')


class BaseCriticalChecker(object):
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
            self.group_types = group_types.copy()
        else:
            raise ValueError('Either group_types or config_path should be provided')

    def is_critical(self, exception: Exception) -> bool:
        if isinstance(exception, self.group_types['critical']):
            return True
        return False
