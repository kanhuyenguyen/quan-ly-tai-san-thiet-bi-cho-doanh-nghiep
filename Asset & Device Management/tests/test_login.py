import pytest
from playwright.sync_api import expect

class TestLogin:
    
    def test_login_success_employee(self, page):
        """TC-LOGIN-01: Đăng nhập thành công với tài khoản Nhân viên"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.uncheck('input[name="is_admin"]')
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        assert page.url == "http://localhost:5000/"
    
    def test_login_success_admin(self, page):
        """TC-LOGIN-02: Đăng nhập thành công với tài khoản Admin"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.check('input[name="is_admin"]')
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/admin")
        assert page.url == "http://localhost:5000/admin"
    
    def test_login_wrong_username(self, page):
        """TC-LOGIN-03: Đăng nhập với username không tồn tại"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "nonexist")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        # Lấy element thứ 2 (server error)
        error = page.locator('.error-message').nth(1)
        expect(error).to_contain_text("Sai tên đăng nhập hoặc mật khẩu")
    
    def test_login_wrong_password(self, page):
        """TC-LOGIN-04: Đăng nhập với sai mật khẩu"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "wrongpassword")
        page.click('button[type="submit"]')
        error = page.locator('.error-message').nth(1)
        expect(error).to_contain_text("Sai tên đăng nhập hoặc mật khẩu")
    
    def test_login_admin_without_checkbox(self, page):
        """TC-LOGIN-05: Đăng nhập Admin nhưng không tick checkbox"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.uncheck('input[name="is_admin"]')
        page.click('button[type="submit"]')
        error = page.locator('.error-message').nth(1)
        expect(error).to_contain_text("Admin cần tick chọn")
    
    def test_login_employee_with_admin_checkbox(self, page):
        """TC-LOGIN-06: Đăng nhập Nhân viên nhưng tick checkbox Admin"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.check('input[name="is_admin"]')
        page.click('button[type="submit"]')
        error = page.locator('.error-message').nth(1)
        expect(error).to_contain_text("không có quyền Quản trị viên")
    
    def test_login_username_has_space(self, page):
        """TC-LOGIN-07: Username chứa khoảng trắng - Lỗi Frontend"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee 1")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Tên đăng nhập không được chứa khoảng trắng")
    
    def test_login_username_has_emoji(self, page):
        """TC-LOGIN-08: Username chứa emoji - Lỗi Frontend"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee😀")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Tên đăng nhập không được chứa emoji")
    
    def test_login_username_special_chars(self, page):
        """TC-LOGIN-09: Username chứa ký tự đặc biệt - Lỗi Frontend"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee@#")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Tên đăng nhập chỉ được chứa chữ cái, số, dấu gạch dưới (_) và dấu chấm (.)")
    
    def test_login_password_too_short(self, page):
        """TC-LOGIN-10: Password quá ngắn (<6 ký tự) - Lỗi Frontend"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Mật khẩu phải có ít nhất 6 ký tự")
    
    def test_login_password_has_space(self, page):
        """TC-LOGIN-11: Password chứa khoảng trắng - Lỗi Frontend"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123 456")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Mật khẩu không được chứa khoảng trắng")
    
    def test_login_empty_username(self, page):
        """TC-LOGIN-12: Để trống username - Lỗi Backend"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        # Lỗi từ backend (required attribute của HTML)
        # Browser sẽ tự bắt lỗi required, không có message cụ thể
        # Kiểm tra xem có còn ở trang login không
        page.wait_for_timeout(500)
        assert "login" in page.url
    
    def test_login_empty_password(self, page):
        """TC-LOGIN-13: Để trống password - Frontend Validation"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "")
        page.click('button[type="submit"]')
        page.wait_for_timeout(500)
        assert "login" in page.url
    
    def test_logout(self, page):
        """TC-LOGOUT-01: Đăng xuất thành công"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        
        page.click('.logout-btn')
        page.wait_for_url("http://localhost:5000/login")
        assert "login" in page.url