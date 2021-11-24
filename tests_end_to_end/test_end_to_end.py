from todo_app.mongo_service import MongoService
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
from todo_app import app
import pytest
import time


@pytest.fixture(scope="module")
def test_app():
    application = app.create_app('test-db')

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    thread.join(1)
    MongoService.delete_database('test-db')


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=options) as driver:
        yield driver


def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

    # Add new task.
    task_title = 'Test-Task'
    new_task_input = driver.find_element_by_name('new_task')
    new_task_input.send_keys(task_title)
    new_task_input.send_keys(Keys.RETURN)
    time.sleep(2)
    assert check_task_displayed_under_correct_status_heading(driver, 'Not Started', task_title)

    # Start task
    start_button = get_button(driver, 'Start')
    start_button.click()
    time.sleep(2)
    assert check_task_displayed_under_correct_status_heading(driver, 'In Progress', task_title)


    # Stop task
    stop_button = get_button(driver, 'Stop')
    stop_button.click()
    time.sleep(2)
    assert check_task_displayed_under_correct_status_heading(driver, 'Not Started', task_title)


    # Finish task
    finish_button = get_button(driver, 'Finish')
    finish_button.click()
    assert check_task_displayed_under_correct_status_heading(driver, 'Complete', task_title)

    # Delete task
    delete_button = get_button(driver, 'Delete')
    delete_button.click()
    time.sleep(2)
    assert check_task_not_present(driver, 'Test-Task')

# Helper functions
def get_button(driver, button_action):
    try:
        button = driver.find_element_by_xpath(f'//button[text()="{button_action}"]')
    except NoSuchElementException:
        return None
    return button

def check_task_displayed_under_correct_status_heading(driver, status, task_title):
    try:
        driver.find_element_by_xpath(
            f'//div[h2/span[contains(text(), "{status}")]]//div[contains(text(), "{task_title}")]'
        ).is_displayed()
    except NoSuchElementException:
        return False
    return True

def check_task_not_present(driver, task_title):
    try:
        driver.find_element_by_xpath(f"div[contains(text(), '{task_title}')]")
    except NoSuchElementException:
        return True
    return False
