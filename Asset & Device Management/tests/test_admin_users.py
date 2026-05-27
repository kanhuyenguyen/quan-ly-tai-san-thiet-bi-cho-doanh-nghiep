import pytest
from playwright.sync_api import expect
import random

class TestAdminUsers:
    
    def test_view_users_list(self, admin_page):
        """TC-USER-01: Xem danh sách người dùng"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        
        users_list = admin_page.locator('#usersList')
        expect(users_list).to_be_visible()
        expect(users_list).not_to_contain_text("Đang tải")
    
    def test_search_user(self, admin_page):
        """TC-USER-02: Tìm kiếm người dùng"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.fill('#searchUser', "admin")
        admin_page.wait_for_timeout(500)
        
        user_cards = admin_page.locator('.user-card')
        if user_cards.count() > 0:
            expect(user_cards.first).to_contain_text("admin")
    
    def test_add_user_success(self, admin_page):
        """TC-USER-03: Thêm user mới thành công"""
        random_suffix = random.randint(1000, 9999)
        
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#username', f"testuser{random_suffix}")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', f"Test User {random_suffix}")
        admin_page.fill('#department', "Test Department")
        admin_page.select_option('#role', "Employee")
        
        def handle_dialog(dialog):
            assert "thành công" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1500)
    
    def test_add_user_duplicate_username(self, admin_page):
        """TC-USER-04: Thêm user với username đã tồn tại"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#username', "employee1")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "Duplicate User")
        admin_page.fill('#department', "Test")
        
        def handle_dialog(dialog):
            assert "đã tồn tại" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_add_user_username_too_short(self, admin_page):
        """TC-USER-05: Username quá ngắn (<3 ký tự)"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#username', "ab")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "Short User")
        
        def handle_dialog(dialog):
            assert "ít nhất 3 ký tự" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_add_user_username_has_space(self, admin_page):
        """TC-USER-06: Username có khoảng trắng"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#username', "test user")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "Space User")
        
        def handle_dialog(dialog):
            assert "không được chứa khoảng trắng" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_add_user_username_has_emoji(self, admin_page):
        """TC-USER-07: Username có emoji"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#username', "test😀user")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "Emoji User")
        
        def handle_dialog(dialog):
            assert "không được chứa emoji" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_add_user_username_special_chars(self, admin_page):
        """TC-USER-08: Username có ký tự đặc biệt"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#username', "test@user")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "Special User")
        
        def handle_dialog(dialog):
            assert "chỉ được chứa chữ cái, số, dấu gạch dưới và dấu chấm" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_add_user_password_too_short(self, admin_page):
        """TC-USER-09: Password quá ngắn (<6 ký tự)"""
        random_suffix = random.randint(1000, 9999)
        
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#username', f"testuser{random_suffix}")
        admin_page.fill('#password', "123")
        admin_page.fill('#fullname', f"Test User {random_suffix}")
        
        def handle_dialog(dialog):
            assert "ít nhất 6 ký tự" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_add_user_password_has_space(self, admin_page):
        """TC-USER-10: Password có khoảng trắng"""
        random_suffix = random.randint(1000, 9999)
        
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#username', f"testuser{random_suffix}")
        admin_page.fill('#password', "123 456")
        admin_page.fill('#fullname', f"Test User {random_suffix}")
        
        def handle_dialog(dialog):
            assert "không được chứa khoảng trắng" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_edit_user(self, admin_page):
        """TC-USER-11: Sửa user thành công"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        
        edit_btn = admin_page.locator('.btn-edit').first
        if edit_btn.count() > 0:
            edit_btn.click()
            admin_page.wait_for_timeout(500)
            
            new_name = f"Edited User {random.randint(1000, 9999)}"
            admin_page.fill('#fullname', new_name)
            
            def handle_dialog(dialog):
                assert "Cập nhật thành công" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_dialog)
            admin_page.click('#saveUserBtn')
            admin_page.wait_for_timeout(1500)
    
    def test_delete_user(self, admin_page):
        """TC-USER-12: Xóa user thành công (user không có tài sản)"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        
        # Tìm user mới tạo để xóa
        delete_btns = admin_page.locator('.btn-delete')
        if delete_btns.count() > 1:
            def handle_confirm(dialog):
                dialog.accept()
            
            admin_page.on("dialog", handle_confirm)
            delete_btns.last.click()
            admin_page.wait_for_timeout(1000)
            
            def handle_alert(dialog):
                assert "Xóa thành công" in dialog.message or "thành công" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_alert)
            admin_page.wait_for_timeout(1000)

    def test_close_modal(self, admin_page):
        """TC-USER-13: Đóng modal thêm/sửa user"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        
        modal = admin_page.locator('#userModal')
        expect(modal).to_be_visible()
        
        admin_page.click('#closeModalBtn')
        admin_page.wait_for_timeout(500)
        
        expect(modal).not_to_be_visible()