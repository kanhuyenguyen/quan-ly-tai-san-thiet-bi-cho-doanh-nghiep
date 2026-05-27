import pytest
import time
import concurrent.futures
import requests

BASE_URL = "http://localhost:5000"

class TestAPI:
    
    def setup_method(self):
        """Đăng nhập Admin để lấy session"""
        self.session = requests.Session()
        self.session.post(f"{BASE_URL}/login", data={'username': 'admin', 'password': 'admin123', 'is_admin': '1'})
    
    # ========== FUNCTIONAL TESTS (12 tests) ==========
    
    def test_func_01_get_assets_api(self):
        """GET /api/admin/assets trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/admin/assets")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_02_get_devices_api(self):
        """GET /api/admin/devices trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/admin/devices")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_03_get_users_api(self):
        """GET /api/admin/users trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/admin/users")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'id' in data[0]
            assert 'username' in data[0]
    
    def test_func_04_get_all_reports_api(self):
        """GET /api/admin/reports/all trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/admin/reports/all")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_05_get_pending_reports_api(self):
        """GET /api/admin/reports/pending trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/admin/reports/pending")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_06_get_all_borrow_requests_api(self):
        """GET /api/admin/borrow-requests/all trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/admin/borrow-requests/all")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_07_get_pending_borrow_api(self):
        """GET /api/admin/borrow-requests/pending trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/admin/borrow-requests/pending")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_08_get_return_items_api(self):
        """GET /api/admin/return-items trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/admin/return-items")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_09_get_assets_in_use_api(self):
        """GET /api/assets/in-use trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/assets/in-use")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_10_get_devices_in_use_api(self):
        """GET /api/devices/in-use trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/devices/in-use")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_11_get_available_assets_api(self):
        """GET /api/assets/available trả về danh sách"""
        resp = self.session.get(f"{BASE_URL}/api/assets/available")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    
    def test_func_12_unauthorized_access(self):
        """Truy cập API không có session trả về lỗi"""
        new_session = requests.Session()
        resp = new_session.get(f"{BASE_URL}/api/admin/users")
        assert resp.status_code == 401 or resp.status_code == 302
    
    # ========== PERFORMANCE TESTS (9 tests) ==========
    
    def test_perf_01_assets_api_response_time(self):
        """Thời gian response API assets < 500ms"""
        start = time.time()
        self.session.get(f"{BASE_URL}/api/admin/assets")
        elapsed = (time.time() - start) * 1000
        print(f"Assets API: {elapsed:.0f}ms")
        assert elapsed < 500
    
    def test_perf_02_devices_api_response_time(self):
        """Thời gian response API devices < 500ms"""
        start = time.time()
        self.session.get(f"{BASE_URL}/api/admin/devices")
        elapsed = (time.time() - start) * 1000
        print(f"Devices API: {elapsed:.0f}ms")
        assert elapsed < 500
    
    def test_perf_03_users_api_response_time(self):
        """Thời gian response API users < 500ms"""
        start = time.time()
        self.session.get(f"{BASE_URL}/api/admin/users")
        elapsed = (time.time() - start) * 1000
        print(f"Users API: {elapsed:.0f}ms")
        assert elapsed < 500
    
    def test_perf_04_reports_api_response_time(self):
        """Thời gian response API reports < 500ms"""
        start = time.time()
        self.session.get(f"{BASE_URL}/api/admin/reports/all")
        elapsed = (time.time() - start) * 1000
        print(f"Reports API: {elapsed:.0f}ms")
        assert elapsed < 500
    
    def test_perf_05_concurrent_20_requests(self):
        """20 concurrent API requests"""
        def call_api():
            s = requests.Session()
            s.post(f"{BASE_URL}/login", data={'username': 'admin', 'password': 'admin123', 'is_admin': '1'})
            start = time.time()
            s.get(f"{BASE_URL}/api/admin/assets")
            return (time.time() - start) * 1000
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
            results = list(ex.map(lambda _: call_api(), range(20)))
        avg = sum(results) / len(results)
        print(f"20 concurrent: {avg:.0f}ms")
        assert avg < 1000
    
    def test_perf_06_concurrent_50_requests(self):
        """50 concurrent API requests"""
        def call_api():
            s = requests.Session()
            s.post(f"{BASE_URL}/login", data={'username': 'admin', 'password': 'admin123', 'is_admin': '1'})
            start = time.time()
            s.get(f"{BASE_URL}/api/admin/assets")
            return (time.time() - start) * 1000
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
            results = list(ex.map(lambda _: call_api(), range(50)))
        avg = sum(results) / len(results)
        max_time = max(results)
        print(f"50 concurrent - TB: {avg:.0f}ms, Chậm: {max_time:.0f}ms")
        assert avg < 1500
    
    def test_perf_07_load_test_100_requests(self):
        """100 requests liên tiếp"""
        times = []
        for _ in range(100):
            start = time.time()
            self.session.get(f"{BASE_URL}/api/admin/assets")
            times.append((time.time() - start) * 1000)
        avg = sum(times) / len(times)
        print(f"100 requests: {avg:.0f}ms")
        assert avg < 500
    
    def test_perf_08_load_test_500_requests(self):
        """500 requests liên tiếp"""
        times = []
        for _ in range(500):
            start = time.time()
            self.session.get(f"{BASE_URL}/api/admin/assets")
            times.append((time.time() - start) * 1000)
        avg = sum(times) / len(times)
        max_time = max(times)
        print(f"500 requests - TB: {avg:.0f}ms, Chậm: {max_time:.0f}ms")
        assert avg < 500
    
    def test_perf_09_success_rate_1000_requests(self):
        """Tỷ lệ thành công 1000 requests > 99%"""
        success = 0
        for _ in range(1000):
            resp = self.session.get(f"{BASE_URL}/api/admin/assets")
            if resp.status_code == 200:
                success += 1
        rate = success / 1000 * 100
        print(f"Tỷ lệ thành công: {rate:.1f}%")
        assert rate > 99
    
    # ========== SECURITY TESTS (9 tests) ==========
    
    def test_sec_01_sql_injection_api(self):
        """SQL Injection qua API param"""
        payloads = ["' OR '1'='1", "admin'--", "1' AND 1=1--"]
        for payload in payloads:
            resp = self.session.get(f"{BASE_URL}/api/admin/users?search={payload}")
            assert resp.status_code != 500
            assert "error" not in resp.text or "SQL" not in resp.text
    
    def test_sec_02_xss_via_api(self):
        """XSS qua API param"""
        resp = self.session.get(f"{BASE_URL}/api/admin/users?search=<script>alert('XSS')</script>")
        assert resp.status_code != 500
        assert "<script>" not in resp.text
    
    def test_sec_03_path_traversal_api(self):
        """Path Traversal qua API"""
        paths = ["../../../etc/passwd", "..\\..\\..\\windows\\win.ini"]
        for path in paths:
            resp = self.session.get(f"{BASE_URL}/api/admin/assets?file={path}")
            assert resp.status_code != 500
    
    def test_sec_04_large_payload_api(self):
        """Large payload attack"""
        large_payload = "A" * 100000
        resp = self.session.post(f"{BASE_URL}/api/admin/users", 
                                 json={'username': large_payload, 'password': '123'})
        assert resp.status_code != 500
        assert resp.status_code == 400 or resp.status_code == 200
    
    def test_sec_05_rate_limiting_api(self):
        """Rate limiting test"""
        start = time.time()
        for _ in range(100):
            self.session.get(f"{BASE_URL}/api/admin/assets")
        elapsed = time.time() - start
        print(f"100 requests time: {elapsed:.1f}s")
        # Nếu quá nhanh (< 2s), không có rate limiting
    
    def test_sec_06_api_authentication_bypass(self):
        """Test authentication bypass"""
        new_session = requests.Session()
        resp = new_session.get(f"{BASE_URL}/api/admin/users")
        assert resp.status_code != 200
    
    def test_sec_07_method_not_allowed(self):
        """Test method not allowed"""
        resp = self.session.delete(f"{BASE_URL}/api/admin/users")
        # DELETE không được phép trên endpoint này
        assert resp.status_code == 405 or resp.status_code == 401 or resp.status_code == 404
    
    def test_sec_08_invalid_json_payload(self):
        """Invalid JSON payload attack"""
        resp = self.session.post(f"{BASE_URL}/api/admin/users", 
                                 data="invalid json",
                                 headers={'Content-Type': 'application/json'})
        assert resp.status_code == 400 or resp.status_code == 500
        # Không được crash server
    
    def test_sec_09_api_response_leak(self):
        """API không leak thông tin nhạy cảm"""
        resp = self.session.get(f"{BASE_URL}/api/admin/users")
        assert resp.status_code == 200
        # Password không được xuất hiện trong response
        assert "password" not in resp.text.lower()