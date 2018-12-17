from logging import getLogger

from .interfaces import BaseCriticalChecker, BaseReportSender

logger = getLogger('main')


class BaseExceptionManager(object):
    counters: dict = None

    def __init__(self, critical_checker: BaseCriticalChecker, report_sender: BaseReportSender):
        self.critical_checker = critical_checker
        self.report_sender = report_sender
        self.counters = {key: 0 for key in self.critical_checker.exception_groups}

    def process_exception(self, exception: Exception):
        if not isinstance(exception, Exception):
            raise TypeError(f'Exception "{exception!r}" has wrong base class')

        try:
            if self.critical_checker.is_critical(exception):
                self.counters['critical'] += 1
                self.report_sender.send_report(exception)
            else:
                self.counters['regular'] += 1
        except IOError:
            self.counters['io'] += 1
