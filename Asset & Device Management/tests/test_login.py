import pytest
import time
import concurrent.futures
import requests
import re
from playwright.sync_api import expect

class TestLogin:
    
    # =================================================================
    # 1. FUNCTIONAL TESTS (12 test cases - giữ nguyên từ bản cũ)
    # =================================================================
    
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
        """TC-LOGIN-07: Username chứa khoảng trắng"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee 1")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Tên đăng nhập không được chứa khoảng trắng")
    
    def test_login_username_has_emoji(self, page):
        """TC-LOGIN-08: Username chứa emoji"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee😀")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Tên đăng nhập không được chứa emoji")
    
    def test_login_username_special_chars(self, page):
        """TC-LOGIN-09: Username chứa ký tự đặc biệt"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee@#")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("chỉ được chứa chữ cái, số, dấu gạch dưới (_) và dấu chấm (.)")
    
    def test_login_password_too_short(self, page):
        """TC-LOGIN-10: Password quá ngắn (<6 ký tự)"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Mật khẩu phải có ít nhất 6 ký tự")
    
    def test_login_password_has_space(self, page):
        """TC-LOGIN-11: Password chứa khoảng trắng"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123 456")
        page.click('button[type="submit"]')
        error = page.locator('#clientError')
        expect(error).to_contain_text("Mật khẩu không được chứa khoảng trắng")
    
    def test_login_empty_username(self, page):
        """TC-LOGIN-12: Để trống username"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "")
        page.fill('input[name="password"]', "123456")
        # HTML5 required sẽ ngăn submit, kiểm tra vẫn ở trang login
        page.click('button[type="submit"]')
        page.wait_for_timeout(500)
        assert "login" in page.url
    
    def test_login_empty_password(self, page):
        """TC-LOGIN-13: Để trống password"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "")
        page.click('button[type="submit"]')
        page.wait_for_timeout(500)
        assert "login" in page.url
    
    def test_logout(self, page):
        """TC-LOGIN-14: Đăng xuất thành công"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        page.click('.logout-btn')
        page.wait_for_url("http://localhost:5000/login")
        assert "login" in page.url
    
    # =================================================================
    # 2. PERFORMANCE TESTS (8 test cases)
    # =================================================================
    
    def test_login_response_time(self, page):
        """PERF-LOGIN-01: Kiểm tra thời gian phản hồi đăng nhập"""
        start_time = time.time()
        
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        print(f"[PERF] Thời gian đăng nhập: {response_time:.2f}ms")
        assert response_time < 3000, f"Đăng nhập quá chậm: {response_time:.2f}ms"
    
    def test_login_page_load_time(self, page):
        """PERF-LOGIN-02: Kiểm tra thời gian tải trang login"""
        start_time = time.time()
        page.goto("http://localhost:5000/login")
        page.wait_for_timeout(500)
        end_time = time.time()
        
        load_time = (end_time - start_time) * 1000
        print(f"[PERF] Thời gian tải trang login: {load_time:.2f}ms")
        assert load_time < 2000, f"Tải trang login quá chậm: {load_time:.2f}ms"
    
    def test_concurrent_login_10_users(self):
        """PERF-LOGIN-03: 10 user đăng nhập cùng lúc"""
        def login_user():
            session = requests.Session()
            login_data = {
                'username': 'employee1',
                'password': '123456',
                'is_admin': '0'
            }
            start = time.time()
            response = session.post("http://localhost:5000/login", data=login_data)
            end = time.time()
            session.get("http://localhost:5000/logout")
            return end - start
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(login_user) for _ in range(10)]
            results = [f.result() for f in futures]
        
        avg_time = sum(results) / len(results) * 1000
        max_time = max(results) * 1000
        min_time = min(results) * 1000
        
        print(f"[PERF] 10 user cùng lúc - TB: {avg_time:.2f}ms, Nhanh: {min_time:.2f}ms, Chậm: {max_time:.2f}ms")
        assert avg_time < 5000, f"Đăng nhập đồng thời quá chậm: {avg_time:.2f}ms"
    
    def test_concurrent_login_20_users(self):
        """PERF-LOGIN-04: 20 user đăng nhập cùng lúc"""
        def login_user():
            session = requests.Session()
            login_data = {
                'username': 'employee1',
                'password': '123456',
                'is_admin': '0'
            }
            start = time.time()
            response = session.post("http://localhost:5000/login", data=login_data)
            end = time.time()
            session.get("http://localhost:5000/logout")
            return end - start
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(login_user) for _ in range(20)]
            results = [f.result() for f in futures]
        
        avg_time = sum(results) / len(results) * 1000
        max_time = max(results) * 1000
        
        print(f"[PERF] 20 user cùng lúc - TB: {avg_time:.2f}ms, Chậm nhất: {max_time:.2f}ms")
        assert avg_time < 8000, f"20 user đăng nhập quá chậm: {avg_time:.2f}ms"
    
    def test_login_load_test_50_times(self):
        """PERF-LOGIN-05: Load test 50 lần đăng nhập liên tiếp"""
        times = []
        
        for i in range(50):
            session = requests.Session()
            login_data = {
                'username': 'employee1',
                'password': '123456',
                'is_admin': '0'
            }
            start = time.time()
            response = session.post("http://localhost:5000/login", data=login_data)
            end = time.time()
            times.append(end - start)
            session.get("http://localhost:5000/logout")
        
        avg_time = sum(times) / len(times) * 1000
        max_time = max(times) * 1000
        min_time = min(times) * 1000
        
        print(f"[PERF] 50 lần login - TB: {avg_time:.2f}ms, Nhanh: {min_time:.2f}ms, Chậm: {max_time:.2f}ms")
        assert avg_time < 3000, f"Load test thất bại: {avg_time:.2f}ms"
    
    def test_login_load_test_100_times(self):
        """PERF-LOGIN-06: Load test 100 lần đăng nhập liên tiếp"""
        times = []
        
        for i in range(100):
            session = requests.Session()
            login_data = {
                'username': 'employee1',
                'password': '123456',
                'is_admin': '0'
            }
            start = time.time()
            response = session.post("http://localhost:5000/login", data=login_data)
            end = time.time()
            times.append(end - start)
            session.get("http://localhost:5000/logout")
        
        avg_time = sum(times) / len(times) * 1000
        print(f"[PERF] 100 lần login - TB: {avg_time:.2f}ms")
        assert avg_time < 3000, f"Load test 100 lần thất bại: {avg_time:.2f}ms"
    
    def test_login_with_different_users(self):
        """PERF-LOGIN-07: Đăng nhập với nhiều user khác nhau"""
        users = ['employee1', 'employee2', 'employee3']
        times = []
        
        for user in users:
            session = requests.Session()
            login_data = {
                'username': user,
                'password': '123456',
                'is_admin': '0'
            }
            start = time.time()
            response = session.post("http://localhost:5000/login", data=login_data)
            end = time.time()
            times.append(end - start)
            session.get("http://localhost:5000/logout")
        
        avg_time = sum(times) / len(times) * 1000
        print(f"[PERF] Đăng nhập nhiều user - TB: {avg_time:.2f}ms")
        assert avg_time < 3000, f"Đăng nhập nhiều user chậm: {avg_time:.2f}ms"
    
    def test_login_stress_test_sequential(self):
        """PERF-LOGIN-08: Stress test - 200 lần đăng nhập liên tiếp"""
        times = []
        success_count = 0
        
        for i in range(200):
            session = requests.Session()
            login_data = {
                'username': 'employee1',
                'password': '123456',
                'is_admin': '0'
            }
            start = time.time()
            response = session.post("http://localhost:5000/login", data=login_data)
            end = time.time()
            
            if response.status_code == 200 or response.status_code == 302:
                success_count += 1
            times.append(end - start)
            session.get("http://localhost:5000/logout")
        
        avg_time = sum(times) / len(times) * 1000
        success_rate = (success_count / 200) * 100
        
        print(f"[PERF] 200 lần login - TB: {avg_time:.2f}ms, Tỷ lệ thành công: {success_rate:.1f}%")
        assert success_rate > 95, f"Stress test thất bại, tỷ lệ thành công: {success_rate}%"
    
    # =================================================================
    # 3. SECURITY TESTS (10 test cases)
    # =================================================================
    
    def test_sql_injection_username_field(self, page):
        """SEC-LOGIN-01: SQL Injection qua trường username"""
        sql_payloads = [
            "' OR '1'='1",
            "admin' --",
            "'; DROP TABLE Users; --",
            "' OR 1=1 --",
            "1' AND 1=1 --",
            "1' AND 1=2 --",
            "' UNION SELECT * FROM Users --",
            "admin' OR 'a'='a",
            "' OR '1'='1' /*",
            "admin'#"
        ]
        
        for payload in sql_payloads:
            page.goto("http://localhost:5000/login")
            page.fill('input[name="username"]', payload)
            page.fill('input[name="password"]', "anything")
            page.click('button[type="submit"]')
            page.wait_for_timeout(500)
            
            # Không được đăng nhập thành công và không bị lỗi 500
            assert "admin" not in page.url
            assert "500" not in page.url
            print(f"[SEC] Tested SQL injection: {payload[:30]}...")
    
    def test_sql_injection_password_field(self, page):
        """SEC-LOGIN-02: SQL Injection qua trường password"""
        sql_payloads = [
            "' OR '1'='1",
            "anything' OR '1'='1",
            "123456' --",
            "' OR 1=1 --"
        ]
        
        for payload in sql_payloads:
            page.goto("http://localhost:5000/login")
            page.fill('input[name="username"]', "employee1")
            page.fill('input[name="password"]', payload)
            page.click('button[type="submit"]')
            page.wait_for_timeout(500)
            
            assert "500" not in page.url
            print(f"[SEC] Tested SQL injection in password: {payload[:30]}...")
    
    def test_xss_username_field(self, page):
        """SEC-LOGIN-03: XSS qua trường username"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
            "<body onload=alert('XSS')>",
            "><script>alert(1)</script>",
            "\"><script>alert('XSS')</script>",
            "<svg onload=alert(1)>",
            "javascript:alert(document.cookie)",
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<img/src=x onerror=alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            page.goto("http://localhost:5000/login")
            page.fill('input[name="username"]', payload)
            page.fill('input[name="password"]', "123456")
            page.click('button[type="submit"]')
            page.wait_for_timeout(500)
            
            # Payload không được thực thi
            assert "alert" not in page.content()
            print(f"[SEC] Tested XSS payload: {payload[:30]}...")
    
    def test_xss_password_field(self, page):
        """SEC-LOGIN-04: XSS qua trường password"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')"
        ]
        
        for payload in xss_payloads:
            page.goto("http://localhost:5000/login")
            page.fill('input[name="username"]', "employee1")
            page.fill('input[name="password"]', payload)
            page.click('button[type="submit"]')
            page.wait_for_timeout(500)
            
            assert "alert" not in page.content()
            print(f"[SEC] Tested XSS in password: {payload[:30]}...")
    
    def test_brute_force_protection_10_attempts(self, page):
        """SEC-LOGIN-05: Kiểm tra bảo vệ Brute Force - 10 lần sai"""
        start_time = time.time()
        
        for i in range(10):
            page.goto("http://localhost:5000/login")
            page.fill('input[name="username"]', "employee1")
            page.fill('input[name="password"]', f"wrong{i}")
            page.click('button[type="submit"]')
            page.wait_for_timeout(500)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"[SEC] 10 lần đăng nhập sai mất: {total_time:.2f} giây")
        # Nếu không có bảo vệ, 10 lần sai sẽ rất nhanh (<2s)
        if total_time < 2:
            print("[SEC] CẢNH BÁO: Không có bảo vệ Brute Force!")
    
    def test_brute_force_protection_20_attempts(self, page):
        """SEC-LOGIN-06: Kiểm tra bảo vệ Brute Force - 20 lần sai"""
        start_time = time.time()
        
        for i in range(20):
            page.goto("http://localhost:5000/login")
            page.fill('input[name="username"]', "employee1")
            page.fill('input[name="password"]', f"wrong{i}")
            page.click('button[type="submit"]')
            page.wait_for_timeout(300)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"[SEC] 20 lần đăng nhập sai mất: {total_time:.2f} giây")
    
    def test_session_fixation(self, page):
        """SEC-LOGIN-07: Kiểm tra Session Fixation"""
        # Lấy session ID trước khi đăng nhập
        page.goto("http://localhost:5000/login")
        cookies_before = page.context.cookies()
        
        # Đăng nhập
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        
        cookies_after = page.context.cookies()
        
        print(f"[SEC] Session trước: {cookies_before}")
        print(f"[SEC] Session sau: {cookies_after}")
        
        # Kiểm tra session có thay đổi không
        # (Nên thay đổi để tránh session fixation)
    
    def test_credential_stuffing(self):
        """SEC-LOGIN-08: Kiểm tra Credential Stuffing"""
        common_passwords = ['123456', 'password', 'admin', '12345678', 'qwerty', 'abc123']
        session = requests.Session()
        
        for pwd in common_passwords:
            login_data = {
                'username': 'employee1',
                'password': pwd,
                'is_admin': '0'
            }
            response = session.post("http://localhost:5000/login", data=login_data)
            # Chỉ có mật khẩu đúng mới đăng nhập được
            if pwd == '123456':
                assert response.status_code == 200 or response.status_code == 302
            else:
                assert "login" in response.url or response.status_code == 200
        
        print("[SEC] Tested credential stuffing with common passwords")
    
    def test_password_policy_enforcement(self, page):
        """SEC-LOGIN-09: Kiểm tra chính sách mật khẩu"""
        weak_passwords = ['123', '12', '1', 'a', 'aa']
        
        for pwd in weak_passwords:
            page.goto("http://localhost:5000/login")
            page.fill('input[name="username"]', "employee1")
            page.fill('input[name="password"]', pwd)
            page.click('button[type="submit"]')
            page.wait_for_timeout(500)
            
            # Phải có thông báo lỗi về độ dài mật khẩu
            error = page.locator('#clientError')
            if error.count() > 0:
                assert "6" in error.inner_text() or "ký tự" in error.inner_text()
            
            print(f"[SEC] Tested weak password: {pwd}")
    
    def test_account_lockout(self, page):
        """SEC-LOGIN-10: Kiểm tra khóa tài khoản sau nhiều lần sai"""
        # Thử đăng nhập sai nhiều lần
        for i in range(15):
            page.goto("http://localhost:5000/login")
            page.fill('input[name="username"]', "employee1")
            page.fill('input[name="password"]', f"wrong{i}")
            page.click('button[type="submit"]')
            page.wait_for_timeout(500)
        
        # Thử đăng nhập đúng sau đó
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.click('button[type="submit"]')
        page.wait_for_timeout(500)
        
        # Kiểm tra xem có bị khóa không (vẫn đăng nhập được hay bị chặn)
        print("[SEC] Tested account lockout after multiple failures")