import pytest
import time
import random
import concurrent.futures
import requests
from playwright.sync_api import expect

class TestAdminAssets:
    
    # ========== FUNCTIONAL TESTS (12 tests) ==========
    
    def test_func_01_view_assets_list(self, admin_page):
        """Xem danh sách tài sản"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(1000)
        table = admin_page.locator('#assetsTableBody')
        expect(table).to_be_visible()
        expect(table).not_to_contain_text("Đang tải")
    
    def test_func_02_view_devices_list(self, admin_page):
        """Xem danh sách thiết bị"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(1000)
        table = admin_page.locator('#devicesTableBody')
        expect(table).to_be_visible()
    
    def test_func_03_view_return_list(self, admin_page):
        """Xem danh sách hoàn trả"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabReturn')
        admin_page.wait_for_timeout(1000)
        table = admin_page.locator('#returnTableBody')
        expect(table).to_be_visible()
    
    def test_func_04_search_asset_by_name(self, admin_page):
        """Tìm kiếm tài sản theo tên"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.fill('#searchAssets', "Bàn")
        admin_page.wait_for_timeout(500)
        rows = admin_page.locator('#assetsTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Bàn")
    
    def test_func_05_search_asset_empty(self, admin_page):
        """Tìm kiếm tài sản không có kết quả"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.fill('#searchAssets', "KHONGCOKETQUA")
        admin_page.wait_for_timeout(500)
        empty_msg = admin_page.locator('#assetsTableBody')
        expect(empty_msg).to_contain_text("Không có dữ liệu")
    
    def test_func_06_search_device_by_name(self, admin_page):
        """Tìm kiếm thiết bị theo tên"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.fill('#searchDevices', "Laptop")
        admin_page.wait_for_timeout(500)
        rows = admin_page.locator('#devicesTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Laptop")
    
    def test_func_07_filter_asset_by_status(self, admin_page):
        """Lọc tài sản theo trạng thái"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.select_option('#filterAssetStatus', "Đang sử dụng")
        admin_page.wait_for_timeout(1000)
        badges = admin_page.locator('#assetsTableBody .status-badge')
        if badges.count() > 0:
            expect(badges.first).to_contain_text("Đang sử dụng")
    
    def test_func_08_filter_asset_by_unused(self, admin_page):
        """Lọc tài sản chưa sử dụng"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.select_option('#filterAssetStatus', "Chưa sử dụng")
        admin_page.wait_for_timeout(1000)
        badges = admin_page.locator('#assetsTableBody .status-badge')
        if badges.count() > 0:
            expect(badges.first).to_contain_text("Chưa sử dụng")
    
    def test_func_09_filter_device_by_status(self, admin_page):
        """Lọc thiết bị theo trạng thái"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.select_option('#filterDeviceStatus', "Đang sử dụng")
        admin_page.wait_for_timeout(1000)
        badges = admin_page.locator('#devicesTableBody .status-badge')
        if badges.count() > 0:
            expect(badges.first).to_contain_text("Đang sử dụng")
    
    def test_func_10_add_asset_success(self, admin_page):
        """Thêm tài sản thành công"""
        rand = random.randint(1000, 9999)
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.click('#addAssetBtn')
        admin_page.wait_for_timeout(500)
        admin_page.fill('#assetName', f"Test Asset {rand}")
        admin_page.select_option('#assetGroup', "Nội thất")
        admin_page.select_option('#assetStatus', "Chưa sử dụng")
        
        def handle(dialog):
            assert "thành công" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveAssetBtn')
        admin_page.wait_for_timeout(1500)
    
    def test_func_11_add_asset_missing_name(self, admin_page):
        """Thêm tài sản thiếu tên"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.click('#addAssetBtn')
        admin_page.wait_for_timeout(500)
        admin_page.fill('#assetName', "")
        
        def handle(dialog):
            assert "Vui lòng nhập" in dialog.message
            dialog.accept()
        admin_page.on("dialog", handle)
        admin_page.click('#saveAssetBtn')
        admin_page.wait_for_timeout(1000)
    
    def test_func_12_edit_asset(self, admin_page):
        """Sửa tài sản"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(1000)
        edit_btn = admin_page.locator('#assetsTableBody .btn-edit').first
        if edit_btn.count() > 0:
            edit_btn.click()
            admin_page.wait_for_timeout(500)
            admin_page.fill('#assetName', f"Edited {random.randint(1000, 9999)}")
            
            def handle(dialog):
                assert "Cập nhật" in dialog.message
                dialog.accept()
            admin_page.on("dialog", handle)
            admin_page.click('#saveAssetBtn')
            admin_page.wait_for_timeout(1500)
    
    # ========== PERFORMANCE TESTS (9 tests) ==========
    
    def test_perf_01_assets_load_time(self, admin_page):
        """Tải danh sách tài sản < 3s"""
        start = time.time()
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải tài sản: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_02_devices_load_time(self, admin_page):
        """Tải danh sách thiết bị < 3s"""
        start = time.time()
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải thiết bị: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_03_return_list_load_time(self, admin_page):
        """Tải danh sách hoàn trả < 3s"""
        start = time.time()
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabReturn')
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải hoàn trả: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_04_search_asset_performance(self, admin_page):
        """Tìm kiếm tài sản < 1s"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        start = time.time()
        admin_page.fill('#searchAssets', "Bàn")
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Tìm kiếm: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_05_search_device_performance(self, admin_page):
        """Tìm kiếm thiết bị < 1s"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        start = time.time()
        admin_page.fill('#searchDevices', "Laptop")
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Tìm kiếm thiết bị: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_06_filter_performance(self, admin_page):
        """Lọc tài sản < 1.5s"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        start = time.time()
        admin_page.select_option('#filterAssetStatus', "Đang sử dụng")
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Lọc: {elapsed:.0f}ms")
        assert elapsed < 1500
    
    def test_perf_07_add_asset_performance(self, admin_page):
        """Thêm tài sản < 2s"""
        rand = random.randint(1000, 9999)
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.click('#addAssetBtn')
        admin_page.wait_for_timeout(500)
        admin_page.fill('#assetName', f"Perf {rand}")
        start = time.time()
        admin_page.click('#saveAssetBtn')
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Thêm tài sản: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    def test_perf_08_concurrent_api_assets(self):
        """10 concurrent API calls < 2s"""
        def get_assets():
            s = requests.Session()
            s.post("http://localhost:5000/login", data={'username': 'admin', 'password': 'admin123', 'is_admin': '1'})
            start = time.time()
            s.get("http://localhost:5000/api/admin/assets")
            return (time.time() - start) * 1000
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            results = list(ex.map(lambda _: get_assets(), range(10)))
        avg = sum(results) / len(results)
        print(f"Concurrent API: {avg:.0f}ms")
        assert avg < 2000
    
    def test_perf_09_tab_switch_performance(self, admin_page):
        """Chuyển tab < 1s"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        start = time.time()
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Chuyển tab: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    # ========== SECURITY TESTS (9 tests) ==========
    
    def test_sec_01_xss_in_asset_name(self, admin_page):
        """XSS khi thêm tài sản"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.click('#addAssetBtn')
        admin_page.fill('#assetName', "<script>alert('XSS')</script>")
        admin_page.click('#saveAssetBtn')
        admin_page.wait_for_timeout(1000)
        assert "alert" not in admin_page.content()
    
    def test_sec_02_xss_in_device_name(self, admin_page):
        """XSS khi thêm thiết bị"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.click('#addDeviceBtn')
        admin_page.fill('#deviceName', "<script>alert('XSS')</script>")
        admin_page.click('#saveDeviceBtn')
        admin_page.wait_for_timeout(1000)
        assert "alert" not in admin_page.content()
    
    def test_sec_03_sql_injection_search_asset(self, admin_page):
        """SQL Injection trong tìm kiếm tài sản"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.fill('#searchAssets', "' OR '1'='1")
        admin_page.wait_for_timeout(500)
        assert "500" not in admin_page.content()
    
    def test_sec_04_sql_injection_search_device(self, admin_page):
        """SQL Injection trong tìm kiếm thiết bị"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.fill('#searchDevices', "' OR '1'='1")
        admin_page.wait_for_timeout(500)
        assert "500" not in admin_page.content()
    
    def test_sec_05_large_payload_asset(self, admin_page):
        """Payload lớn trong tên tài sản"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.click('#addAssetBtn')
        admin_page.fill('#assetName', "A" * 10000)
        admin_page.click('#saveAssetBtn')
        admin_page.wait_for_timeout(1000)
        assert "500" not in admin_page.content()
    
    def test_sec_06_html_injection_search(self, admin_page):
        """HTML Injection trong tìm kiếm"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.fill('#searchAssets', "<h1>Hacked</h1>")
        admin_page.wait_for_timeout(500)
        assert "<h1>" not in admin_page.content() or "&lt;h1&gt;" in admin_page.content()
    
    def test_sec_07_special_chars_in_asset(self, admin_page):
        """Ký tự đặc biệt trong tên tài sản"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.click('#addAssetBtn')
        admin_page.fill('#assetName', "!@#$%^&*()_+{}|:<>?~`")
        admin_page.click('#saveAssetBtn')
        admin_page.wait_for_timeout(1000)
        assert "500" not in admin_page.content()
    
    def test_sec_08_unauthorized_return_action(self, page):
        """Người dùng thường không thấy nút hoàn trả"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.uncheck('input[name="is_admin"]')
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        page.goto("http://localhost:5000/admin/assets-devices")
        # Nhân viên không thể vào trang admin
        assert "login" in page.url or page.url == "http://localhost:5000/"
    
    def test_sec_09_path_traversal(self, admin_page):
        """Path Traversal attack"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.fill('#searchAssets', "../../../etc/passwd")
        admin_page.wait_for_timeout(500)
        assert "500" not in admin_page.content()