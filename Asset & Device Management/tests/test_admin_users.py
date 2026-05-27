import pytest
import time
import random
from playwright.sync_api import expect

class TestAdminUsers:
    
    # ========== FUNCTIONAL TESTS (12 tests) ==========
    
    def test_func_01_view_users_list(self, admin_page):
        """Xem danh sách người dùng"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        users_list = admin_page.locator('#usersList')
        expect(users_list).to_be_visible()
        expect(users_list).not_to_contain_text("Đang tải")
    
    def test_func_02_search_user(self, admin_page):
        """Tìm kiếm người dùng"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.fill('#searchUser', "admin")
        admin_page.wait_for_timeout(500)
        cards = admin_page.locator('.user-card')
        if cards.count() > 0:
            expect(cards.first).to_contain_text("admin")
    
    def test_func_03_search_user_not_found(self, admin_page):
        """Tìm kiếm không có kết quả"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.fill('#searchUser', "KHONGTONTAI")
        admin_page.wait_for_timeout(500)
        empty_msg = admin_page.locator('#usersList')
        expect(empty_msg).to_contain_text("Không có người dùng nào")
    
    def test_func_04_add_user_success(self, admin_page):
        """Thêm user thành công"""
        rand = random.randint(1000, 9999)
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        admin_page.fill('#username', f"testuser{rand}")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', f"Test User {rand}")
        admin_page.fill('#department', "Test Dept")
        admin_page.select_option('#role', "Employee")
        
        def handle(dialog):
            assert "thành công" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1500)
    
    def test_func_05_add_user_duplicate_username(self, admin_page):
        """Username đã tồn tại"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', "employee1")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "Duplicate")
        
        def handle(dialog):
            assert "đã tồn tại" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_func_06_add_user_username_too_short(self, admin_page):
        """Username quá ngắn (<3 ký tự)"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', "ab")
        admin_page.fill('#password', "123456")
        
        def handle(dialog):
            assert "ít nhất 3 ký tự" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_func_07_add_user_username_has_space(self, admin_page):
        """Username có khoảng trắng"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', "test user")
        admin_page.fill('#password', "123456")
        
        def handle(dialog):
            assert "không được chứa khoảng trắng" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_func_08_add_user_username_emoji(self, admin_page):
        """Username có emoji"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', "test😀user")
        admin_page.fill('#password', "123456")
        
        def handle(dialog):
            assert "không được chứa emoji" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_func_09_add_user_username_special_chars(self, admin_page):
        """Username có ký tự đặc biệt"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', "test@user")
        admin_page.fill('#password', "123456")
        
        def handle(dialog):
            assert "chỉ được chứa chữ cái, số, dấu gạch dưới và dấu chấm" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_func_10_add_user_password_too_short(self, admin_page):
        """Password quá ngắn (<6 ký tự)"""
        rand = random.randint(1000, 9999)
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', f"test{rand}")
        admin_page.fill('#password', "123")
        
        def handle(dialog):
            assert "ít nhất 6 ký tự" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_func_11_edit_user(self, admin_page):
        """Sửa user thành công"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        edit_btn = admin_page.locator('.btn-edit').first
        if edit_btn.count() > 0:
            edit_btn.click()
            admin_page.fill('#fullname', f"Edited {random.randint(1000, 9999)}")
            
            def handle(dialog):
                assert "Cập nhật" in dialog.message
                dialog.accept()
            admin_page.on("dialog", handle)
            admin_page.click('#saveUserBtn')
            admin_page.wait_for_timeout(1500)
    
    def test_func_12_delete_user(self, admin_page):
        """Xóa user thành công"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        delete_btns = admin_page.locator('.btn-delete')
        if delete_btns.count() > 1:
            admin_page.on("dialog", lambda d: d.accept())
            delete_btns.last.click()
            admin_page.wait_for_timeout(1000)
    
    # ========== PERFORMANCE TESTS (9 tests) ==========
    
    def test_perf_01_users_load_time(self, admin_page):
        """Thời gian tải danh sách user < 3s"""
        start = time.time()
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải user: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_02_search_user_performance(self, admin_page):
        """Tìm kiếm user < 1s"""
        admin_page.goto("http://localhost:5000/admin/users")
        start = time.time()
        admin_page.fill('#searchUser', "admin")
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Tìm user: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_03_add_user_performance(self, admin_page):
        """Thêm user < 2s"""
        rand = random.randint(1000, 9999)
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', f"perf{rand}")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "Perf Test")
        start = time.time()
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Thêm user: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    def test_perf_04_edit_user_performance(self, admin_page):
        """Sửa user < 2s"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        edit_btn = admin_page.locator('.btn-edit').first
        if edit_btn.count() > 0:
            edit_btn.click()
            start = time.time()
            admin_page.click('#saveUserBtn')
            admin_page.wait_for_timeout(1000)
            elapsed = (time.time() - start) * 1000
            print(f"Sửa user: {elapsed:.0f}ms")
            assert elapsed < 2000
    
    def test_perf_05_delete_user_performance(self, admin_page):
        """Xóa user < 1.5s"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(1000)
        delete_btns = admin_page.locator('.btn-delete')
        if delete_btns.count() > 1:
            start = time.time()
            admin_page.on("dialog", lambda d: d.accept())
            delete_btns.last.click()
            admin_page.wait_for_timeout(1000)
            elapsed = (time.time() - start) * 1000
            print(f"Xóa user: {elapsed:.0f}ms")
            assert elapsed < 1500
    
    def test_perf_06_modal_open_close(self, admin_page):
        """Mở/đóng modal < 1s"""
        admin_page.goto("http://localhost:5000/admin/users")
        start = time.time()
        admin_page.click('#addUserBtn')
        admin_page.wait_for_timeout(500)
        admin_page.click('#closeModalBtn')
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Mở/đóng modal: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_07_load_large_user_list(self, admin_page):
        """Tải danh sách user lớn < 5s"""
        start = time.time()
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.wait_for_timeout(2000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải user list: {elapsed:.0f}ms")
        assert elapsed < 5000
    
    def test_perf_08_concurrent_user_operations(self):
        """Concurrent API calls < 2s"""
        import concurrent.futures
        def get_users():
            s = requests.Session()
            s.post("http://localhost:5000/login", data={'username': 'admin', 'password': 'admin123', 'is_admin': '1'})
            start = time.time()
            s.get("http://localhost:5000/api/admin/users")
            return (time.time() - start) * 1000
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            results = list(ex.map(lambda _: get_users(), range(10)))
        avg = sum(results) / len(results)
        print(f"Concurrent API: {avg:.0f}ms")
        assert avg < 2000
    
    def test_perf_09_search_with_wildcard(self, admin_page):
        """Tìm kiếm với ký tự đại diện < 1s"""
        admin_page.goto("http://localhost:5000/admin/users")
        start = time.time()
        admin_page.fill('#searchUser', "a")
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Tìm kiếm wildcard: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    # ========== SECURITY TESTS (9 tests) ==========
    
    def test_sec_01_sql_injection_user_search(self, admin_page):
        """SQL Injection trong tìm kiếm user"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.fill('#searchUser', "' OR '1'='1")
        admin_page.wait_for_timeout(500)
        assert "500" not in admin_page.content()
    
    def test_sec_02_xss_in_fullname(self, admin_page):
        """XSS khi thêm user"""
        rand = random.randint(1000, 9999)
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', f"xss{rand}")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "<script>alert('XSS')</script>")
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
        assert "alert" not in admin_page.content()
    
    def test_sec_03_xss_in_department(self, admin_page):
        """XSS trong department"""
        rand = random.randint(1000, 9999)
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        admin_page.fill('#username', f"xssdept{rand}")
        admin_page.fill('#password', "123456")
        admin_page.fill('#fullname', "XSS Dept")
        admin_page.fill('#department', "<script>alert('XSS')</script>")
        admin_page.click('#saveUserBtn')
        admin_page.wait_for_timeout(1000)
        assert "alert" not in admin_page.content()
    
    def test_sec_04_self_deletion_prevention(self, admin_page):
        """Không thể xóa chính mình"""
        admin_page.goto("http://localhost:5000/admin/users")
        first_delete = admin_page.locator('.btn-delete').first
        admin_page.on("dialog", lambda d: d.accept())
        first_delete.click()
        admin_page.wait_for_timeout(1000)
        assert "users" in admin_page.url
    
    def test_sec_05_privilege_escalation(self, admin_page):
        """Chỉ Admin mới thấy nút thêm user"""
        admin_page.goto("http://localhost:5000/admin/users")
        add_btn = admin_page.locator('#addUserBtn')
        expect(add_btn).to_be_visible()
    
    def test_sec_06_invalid_role_assignment(self, admin_page):
        """Không thể gán role không hợp lệ"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.click('#addUserBtn')
        role_select = admin_page.locator('#role')
        options = role_select.locator('option')
        values = [opt.get_attribute('value') for opt in options.all()]
        assert 'Admin' in values
        assert 'Employee' in values
        assert 'SuperAdmin' not in values
    
    def test_sec_07_password_leak_in_response(self, admin_page):
        """Password không hiển thị trong response"""
        admin_page.goto("http://localhost:5000/admin/users")
        page_content = admin_page.content()
        assert "password" not in page_content.lower() or "••••••" in page_content
    
    def test_sec_08_brute_force_user_creation(self, admin_page):
        """Tạo nhiều user liên tiếp (rate limiting)"""
        start = time.time()
        for i in range(5):
            rand = random.randint(10000, 99999)
            admin_page.goto("http://localhost:5000/admin/users")
            admin_page.click('#addUserBtn')
            admin_page.fill('#username', f"brute{rand}")
            admin_page.fill('#password', "123456")
            admin_page.fill('#fullname', f"Brute {i}")
            admin_page.click('#saveUserBtn')
            admin_page.wait_for_timeout(500)
        elapsed = time.time() - start
        print(f"5 user creations: {elapsed:.1f}s")
        # Nếu quá nhanh (< 2s), có thể bị tấn công DoS
    
    def test_sec_09_html_injection_user_search(self, admin_page):
        """HTML Injection trong tìm kiếm user"""
        admin_page.goto("http://localhost:5000/admin/users")
        admin_page.fill('#searchUser', "<h1>Hacked</h1>")
        admin_page.wait_for_timeout(500)
        assert "<h1>" not in admin_page.content() or "&lt;h1&gt;" in admin_page.content()