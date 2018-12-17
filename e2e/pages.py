from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""
    def __init__(self, driver):
        self.driver = driver

    def _find_edit_text_bar(self, locator):
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        return elem

    edit_text_locator = (By.CLASS_NAME, 'new-todo')

    def add_tasks(self, tasks_to_load):
        """Adding tasks"""
        for task in tasks_to_load:
            self.add_task(task)

    def add_task(self, task):
        edit_text = self._find_edit_text_bar(self.edit_text_locator)
        edit_text.send_keys(task)
        edit_text.send_keys(Keys.ENTER)

    def read_tasks(self):
        return self.driver.find_elements_by_css_selector('li .view')

    def read_task(self, task_id):
        xpath_selector = f'//li[{task_id + 1}]/div/label'
        return self.driver.find_element_by_xpath(xpath_selector)

    def num_of_tasks(self):
        all_tasks = self.read_tasks()
        return len(all_tasks)

    def delete_task(self, task_id):
        xpath_selector = f'//li[{task_id + 1}]/div/button'
        del_button = self.driver.find_element_by_xpath(xpath_selector)
        self.driver.execute_script('arguments[0].click();', del_button)

    def check_task(self, task_id):
        xpath_selector = f'(//input[@type="checkbox"])[{task_id + 2}]'
        self.driver.find_element_by_xpath(xpath_selector).click()

    def get_completed_tasks(self):
        return self.driver.find_elements_by_css_selector('li.completed .view')

    def get_uncompleted_tasks(self):
        return self.driver.find_elements_by_css_selector('li:not(.completed) .view')

    def see_all_tasks(self):
        self.driver.find_element_by_xpath('//footer/ul/li/a').click()

    def see_active_tasks(self):
        self.driver.find_element_by_xpath('//footer/ul/li[2]/a').click()

    def see_completed_tasks(self):
        self.driver.find_element_by_xpath('//footer/ul/li[3]/a').click()


class MainPage(BasePage):
    def task_exist(self, task):
        all_tasks = self.read_tasks()
        text_tasks = self.tasks_to_text(all_tasks)
        return task in text_tasks

    def check_task_by_id(self, task_to_check, task_id):
        text_tasks = self.read_task(task_id).text
        return text_tasks == task_to_check

    def check_all_tasks_by_id(self, tasks_to_check):
        for i, task in enumerate(tasks_to_check):
            if not self.check_task_by_id(task, i):
                return False
        return True

    @staticmethod
    def tasks_to_text(tasks):
        return [single_task.text for single_task in tasks]
