import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from e2e.pages import MainPage


chrome_options = Options()
chrome_options.add_argument("--headless")
CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH', '/home/daniil/3dparty/chromedriver')


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=chrome_options)
        self.driver.get('http://todomvc.com/examples/angularjs/#/')

    def test_add_task_success(self):
        main_page = MainPage(self.driver)
        main_page.add_task('task1')
        assert main_page.check_task_by_id('task1', 0), 'task in not added'

    def test_add_tasks_success(self):
        main_page = MainPage(self.driver)
        tasks = ['task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7']
        main_page.add_tasks(tasks)
        assert main_page.check_all_tasks_by_id(tasks), 'task in not added'

    def test_delete_task_success(self):
        main_page = MainPage(self.driver)
        tasks = ['task0', 'task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7']
        main_page.add_tasks(tasks)
        num_of_tasks = main_page.num_of_tasks()
        main_page.delete_task(1)
        num_of_tasks_changed = main_page.num_of_tasks()

        assert not main_page.check_task_by_id('task1', 1), 'task is not deleted not added'
        assert num_of_tasks - num_of_tasks_changed == 1, 'task is not deleted not added'

    def test_check_out_task_success(self):
        main_page = MainPage(self.driver)
        tasks = ['task0', 'task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7']
        main_page.add_tasks(tasks)

        main_page.check_task(2)
        main_page.check_task(3)
        main_page.check_task(4)
        i = 2

        comp_tasks = main_page.get_completed_tasks()
        for task in comp_tasks:
            assert task.text == tasks[i], 'task is not checked'
            i += 1

        i = 0
        uncomp_tasks = main_page.get_uncompleted_tasks()
        for task in uncomp_tasks:
            assert task.text == tasks[i], 'task is checked, but don\'t has to be checked'
            if i == 1:
                i += 3
            i += 1

    def test_check_active(self):
        main_page = MainPage(self.driver)
        tasks = ['task0', 'task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7']
        main_page.add_tasks(tasks)

        main_page.check_task(4)
        main_page.check_task(5)
        main_page.check_task(6)

        uncomp_tasks = main_page.get_uncompleted_tasks()
        uncomp_tasks_text = main_page.tasks_to_text(uncomp_tasks)
        main_page.see_active_tasks()
        active_tasks = main_page.read_tasks()
        active_tasks_text = main_page.tasks_to_text(active_tasks)
        assert uncomp_tasks_text == active_tasks_text, 'active button does not work'

    def test_check_completed(self):
        main_page = MainPage(self.driver)
        tasks = ['task0', 'task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7']
        main_page.add_tasks(tasks)

        comp_tasks = main_page.get_completed_tasks()
        comp_tasks_text = main_page.tasks_to_text(comp_tasks)
        main_page.see_completed_tasks()
        c_tasks = main_page.read_tasks()
        c_tasks_text = main_page.tasks_to_text(c_tasks)
        assert comp_tasks_text == c_tasks_text, 'completed button does not work'

    def test_check_all(self):
        main_page = MainPage(self.driver)
        tasks = ['task0', 'task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7']
        main_page.add_tasks(tasks)

        main_page.see_completed_tasks()
        main_page.see_all_tasks()
        all_tasks = main_page.read_tasks()
        all_tasks_text = main_page.tasks_to_text(all_tasks)
        assert all_tasks_text == tasks, 'all button does not work'

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
