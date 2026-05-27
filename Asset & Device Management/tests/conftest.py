import pytest
from playwright.sync_api import sync_playwright

def pytest_configure(config):
    """Cấu hình HTML report"""
    if not hasattr(config, 'slaveinput'):
        config.option.htmlpath = 'report.html'

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False để xem trình duyệt
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def admin_page(page):
    """Đăng nhập với tài khoản Admin trước khi test"""
    page.goto("http://localhost:5000/login")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin123")
    page.check('input[name="is_admin"]')
    page.click('button[type="submit"]')
    page.wait_for_url("http://localhost:5000/admin")
    return page

@pytest.fixture
def employee_page(page):
    """Đăng nhập với tài khoản Nhân viên trước khi test"""
    page.goto("http://localhost:5000/login")
    page.fill('input[name="username"]', "employee1")
    page.fill('input[name="password"]', "123456")
    page.uncheck('input[name="is_admin"]')
    page.click('button[type="submit"]')
    page.wait_for_url("http://localhost:5000/")
    return page