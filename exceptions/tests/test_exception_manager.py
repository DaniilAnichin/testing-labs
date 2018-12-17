import unittest

from exceptions.manager import BaseExceptionManager
from exceptions.manager.interfaces import CriticalChecker, BaseReportSender, ServerMailReportSender


class IsCriticalTestCase(unittest.TestCase):
    def setUp(self):
        self.critical_checker = CriticalChecker(group_types={
            "critical": [RecursionError, TypeError, ValueError]})
        self.exceptions = [RecursionError(), TypeError(), ValueError()]
        self.regular_exceptions = [IndexError(), NotImplementedError()]

    def test_IsCritical_critical(self):
        for exception in self.exceptions:
            with self.subTest(f'Testing {exception!r} is critical'):
                is_critical = self.critical_checker.is_critical(exception)
                assert is_critical is True, f'{exception!r} is not critical'

    def test_IsCritical_critical_wrong(self):
        for exception in self.regular_exceptions:
            with self.subTest(f'Testing {exception!r} is not critical'):
                is_critical = self.critical_checker.is_critical(exception)
                assert is_critical is False, f'{exception!r} is critical'


class BaseExceptionManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.critical_checker = CriticalChecker(config_path='config.json')
        self.report_sender = ServerMailReportSender()
        self.manager = BaseExceptionManager(self.critical_checker, self.report_sender)
        self.exceptions = [RecursionError(), TypeError(), ValueError()]
        self.regular_exceptions = [IndexError(), NotImplementedError()]

    def test_BaseExceptionManager_init(self):
        assert not any(self.manager.counters.values()), \
            'Some counters are not initially set to 0'

    def test_BaseExceptionManager_wrong_base(self):
        self.assertRaises(TypeError, self.manager.process_exception,
                          {'message': 'Error imitation'})

    def test_BaseExceptionManager_process_critical(self):
        for exception in self.exceptions:
            with self.subTest(f'Testing {exception!r} increases counter'):
                before_counter = self.manager.counters['critical']
                self.manager.process_exception(exception)
                delta = self.manager.counters['critical'] - before_counter
                assert delta == 1, f'Critical counter increased by {delta} when expected by 1 after {exception!r}'

    def test_BaseExceptionManager_process_regular(self):
        for exception in self.regular_exceptions:
            with self.subTest(f'Testing {exception!r} not increases counter'):
                before_counter = self.manager.counters['regular']
                self.manager.process_exception(exception)
                delta = self.manager.counters['regular'] - before_counter
                assert delta == 1, f'Regular counter increased by {delta} when expected by 1 after {exception!r}'

    def test_BaseExceptionManager_process_io(self):
        class FakeReporter(BaseReportSender):
            def send_report(self, exception):
                raise IOError(f'Cannot send {exception!r};')
        self.manager.report_sender = FakeReporter()
        for exception in self.exceptions:
            with self.subTest(f'Testing {exception!r} + IOError() increases both counters'):
                before_counter = self.manager.counters['io']
                before_crit = self.manager.counters['critical']
                self.manager.process_exception(exception)
                delta = self.manager.counters['io'] - before_counter
                assert delta == 1, f'IO counter increased by {delta} when expected by 1 after {exception!r}'
                delta = self.manager.counters['critical'] - before_crit
                assert delta == 1, f'Critical counter increased by {delta} when expected by 1 after {exception!r}'


if __name__ == '__main__':
    unittest.main()
