import pytest
import time
import random
from playwright.sync_api import expect

class TestEmployee:
    
    # ========== FUNCTIONAL TESTS (12 tests) ==========
    
    def test_func_01_employee_view_home(self, employee_page):
        """Xem trang chủ nhân viên"""
        employee_page.goto("http://localhost:5000/")
        employee_page.wait_for_timeout(1000)
        assert "Asset" in employee_page.title() or "Device" in employee_page.title()
    
    def test_func_02_view_assets_list(self, employee_page):
        """Xem danh sách tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(1000)
        table = employee_page.locator('#assetTableBody')
        expect(table).to_be_visible()
        expect(table).not_to_contain_text("Đang tải")
    
    def test_func_03_view_devices_list(self, employee_page):
        """Xem danh sách thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.wait_for_timeout(1000)
        table = employee_page.locator('#deviceTableBody')
        expect(table).to_be_visible()
    
    def test_func_04_search_assets(self, employee_page):
        """Tìm kiếm tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "Bàn")
        employee_page.wait_for_timeout(500)
        rows = employee_page.locator('#assetTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Bàn")
    
    def test_func_05_search_devices(self, employee_page):
        """Tìm kiếm thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.fill('#searchInput', "Laptop")
        employee_page.wait_for_timeout(500)
        rows = employee_page.locator('#deviceTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Laptop")
    
    def test_func_06_send_asset_report(self, employee_page):
        """Gửi báo cáo tài sản"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.wait_for_timeout(500)
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', f"Test report {random.randint(1000, 9999)}")
        
        def handle(dialog):
            assert "đã được gửi" in dialog.message
            dialog.accept()
        employee_page.on("dialog", handle)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    def test_func_07_send_device_report(self, employee_page):
        """Gửi báo cáo thiết bị"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.wait_for_timeout(500)
        employee_page.select_option('#deviceSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', f"Test device report {random.randint(1000, 9999)}")
        
        def handle(dialog):
            assert "đã được gửi" in dialog.message
            dialog.accept()
        employee_page.on("dialog", handle)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    def test_func_08_view_borrow_page(self, employee_page):
        """Xem trang yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.wait_for_timeout(1000)
        my_assets = employee_page.locator('#myAssetsPanel')
        expect(my_assets).to_be_visible()
    
    def test_func_09_switch_to_available_assets(self, employee_page):
        """Chuyển sang tab tài sản chưa sử dụng"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        available = employee_page.locator('#availableAssetsPanel')
        expect(available).to_be_visible()
    
    def test_func_10_send_borrow_request(self, employee_page):
        """Gửi yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.fill('#borrowReason', f"Test borrow {random.randint(1000, 9999)}")
            
            def handle(dialog):
                assert "đã được gửi" in dialog.message
                dialog.accept()
            employee_page.on("dialog", handle)
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
    
    def test_func_11_view_track_reports(self, employee_page):
        """Theo dõi báo cáo"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.wait_for_timeout(1000)
        reports_tab = employee_page.locator('#tabReports')
        reports_tab.click()
        reports_table = employee_page.locator('#reportsTableBody')
        expect(reports_table).to_be_visible()
    
    def test_func_12_view_track_borrow(self, employee_page):
        """Theo dõi yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.wait_for_timeout(1000)
        borrow_tab = employee_page.locator('#tabBorrow')
        borrow_tab.click()
        borrow_table = employee_page.locator('#borrowTableBody')
        expect(borrow_table).to_be_visible()
    
    # ========== PERFORMANCE TESTS (9 tests) ==========
    
    def test_perf_01_assets_load_time(self, employee_page):
        """Tải danh sách tài sản < 3s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải tài sản: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_02_devices_load_time(self, employee_page):
        """Tải danh sách thiết bị < 3s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải thiết bị: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_03_search_performance(self, employee_page):
        """Tìm kiếm tài sản < 1s"""
        employee_page.goto("http://localhost:5000/user/assets")
        start = time.time()
        employee_page.fill('#searchInput', "Bàn")
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Tìm kiếm: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_04_report_submit_performance(self, employee_page):
        """Gửi báo cáo < 2s"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.wait_for_timeout(500)
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "Performance test")
        start = time.time()
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Gửi báo cáo: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    def test_perf_05_borrow_request_performance(self, employee_page):
        """Gửi yêu cầu mượn < 2s"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.fill('#borrowReason', "Performance test")
            start = time.time()
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
            elapsed = (time.time() - start) * 1000
            print(f"Gửi yêu cầu: {elapsed:.0f}ms")
            assert elapsed < 2000
    
    def test_perf_06_tab_switch_performance(self, employee_page):
        """Chuyển tab < 1s"""
        employee_page.goto("http://localhost:5000/user/track")
        start = time.time()
        employee_page.click('#tabBorrow')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Chuyển tab: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_07_refresh_performance(self, employee_page):
        """Làm mới danh sách < 1s"""
        employee_page.goto("http://localhost:5000/user/assets")
        start = time.time()
        employee_page.click('#refreshBtn')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Làm mới: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_08_my_assets_filter(self, employee_page):
        """Lọc tài sản của tôi < 1s"""
        employee_page.goto("http://localhost:5000/user/assets")
        start = time.time()
        employee_page.click('.tab-btn[data-tab="my"]')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Lọc tài sản của tôi: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_09_concurrent_employee_actions(self):
        """Nhiều nhân viên cùng thao tác"""
        import concurrent.futures
        def view_assets():
            s = requests.Session()
            s.post("http://localhost:5000/login", data={'username': 'employee1', 'password': '123456'})
            start = time.time()
            s.get("http://localhost:5000/user/assets")
            return (time.time() - start) * 1000
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            results = list(ex.map(lambda _: view_assets(), range(10)))
        avg = sum(results) / len(results)
        print(f"Concurrent: {avg:.0f}ms")
        assert avg < 3000
    
    # ========== SECURITY TESTS (9 tests) ==========
    
    def test_sec_01_xss_in_search(self, employee_page):
        """XSS trong tìm kiếm tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "<script>alert('XSS')</script>")
        employee_page.wait_for_timeout(500)
        assert "alert" not in employee_page.content()
    
    def test_sec_02_sql_injection_search(self, employee_page):
        """SQL Injection trong tìm kiếm"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "' OR '1'='1")
        employee_page.wait_for_timeout(500)
        assert "500" not in employee_page.content()
    
    def test_sec_03_xss_in_report_description(self, employee_page):
        """XSS trong báo cáo"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "<script>alert('XSS')</script>")
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        assert "alert" not in employee_page.content()
    
    def test_sec_04_html_injection_search(self, employee_page):
        """HTML Injection trong tìm kiếm"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "<h1>Hacked</h1>")
        employee_page.wait_for_timeout(500)
        assert "<h1>" not in employee_page.content() or "&lt;h1&gt;" in employee_page.content()
    
    def test_sec_05_unauthorized_admin_access(self, employee_page):
        """Nhân viên không thể truy cập admin"""
        employee_page.goto("http://localhost:5000/admin")
        assert "login" in employee_page.url or employee_page.url == "http://localhost:5000/"
    
    def test_sec_06_unauthorized_api_access(self, employee_page):
        """Nhân viên không thể gọi API admin"""
        employee_page.goto("http://localhost:5000/api/admin/users")
        # API trả về lỗi hoặc redirect
        assert "error" in employee_page.content() or "login" in employee_page.url
    
    def test_sec_07_large_payload_in_report(self, employee_page):
        """Payload lớn trong báo cáo"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "A" * 10000)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        assert "500" not in employee_page.content()
    
    def test_sec_08_special_chars_in_borrow_reason(self, employee_page):
        """Ký tự đặc biệt trong lý do mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.fill('#borrowReason', "!@#$%^&*()_+{}|:<>?~`")
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
            assert "500" not in employee_page.content()
    
    def test_sec_09_brute_force_report_submit(self, employee_page):
        """Gửi nhiều báo cáo liên tiếp"""
        start = time.time()
        for i in range(5):
            employee_page.goto("http://localhost:5000/user/report-assets")
            employee_page.select_option('#assetSelect', index=1)
            employee_page.check('input[value="broken"]')
            employee_page.fill('#description', f"Report {i}")
            employee_page.click('#reportForm button[type="submit"]')
            employee_page.wait_for_timeout(500)
        elapsed = time.time() - start
        print(f"5 reports: {elapsed:.1f}s")