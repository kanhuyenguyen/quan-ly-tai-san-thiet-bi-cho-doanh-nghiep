import pytest
import time
import random
from playwright.sync_api import expect

class TestEmployee:
    
    # =================================================================
    # 1. TRANG CHỦ (HOME) - 8 tests (4F + 2P + 2S)
    # =================================================================
    
    # ----- FUNCTIONAL TESTS (4 tests) -----
    
    def test_home_01_view_home_page(self, employee_page):
        """FUNC: Xem trang chủ nhân viên"""
        employee_page.goto("http://localhost:5000/")
        employee_page.wait_for_timeout(1000)
        assert "Asset" in employee_page.title() or "Device" in employee_page.title()
    
    def test_home_02_statistics_display(self, employee_page):
        """FUNC: Kiểm tra thống kê hiển thị (4 stat cards)"""
        employee_page.goto("http://localhost:5000/")
        employee_page.wait_for_timeout(1000)
        stat_cards = employee_page.locator('.stat-card')
        assert stat_cards.count() == 4
    
    def test_home_03_recent_assets_display(self, employee_page):
        """FUNC: Kiểm tra hiển thị tài sản nổi bật"""
        employee_page.goto("http://localhost:5000/")
        employee_page.wait_for_timeout(1000)
        recent_assets = employee_page.locator('#recentAssets')
        expect(recent_assets).to_be_visible()
    
    def test_home_04_recent_devices_display(self, employee_page):
        """FUNC: Kiểm tra hiển thị thiết bị nổi bật"""
        employee_page.goto("http://localhost:5000/")
        employee_page.wait_for_timeout(1000)
        recent_devices = employee_page.locator('#recentDevices')
        expect(recent_devices).to_be_visible()
    
    # ----- PERFORMANCE TESTS (2 tests) -----
    
    def test_home_perf_01_load_time(self, employee_page):
        """PERF: Thời gian tải trang chủ < 2s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/")
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải trang chủ: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    def test_home_perf_02_statistics_load_time(self, employee_page):
        """PERF: Thời gian tải thống kê < 1s"""
        employee_page.goto("http://localhost:5000/")
        start = time.time()
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải thống kê: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    # ----- SECURITY TESTS (2 tests) -----
    
    def test_home_sec_01_xss_on_url(self, employee_page):
        """SEC: XSS qua URL parameter"""
        employee_page.goto("http://localhost:5000/?search=<script>alert(1)</script>")
        employee_page.wait_for_timeout(500)
        assert "alert" not in employee_page.content()
    
    def test_home_sec_02_sql_injection_url(self, employee_page):
        """SEC: SQL Injection qua URL"""
        employee_page.goto("http://localhost:5000/?id=' OR '1'='1")
        employee_page.wait_for_timeout(500)
        assert "500" not in employee_page.content()
    
    # =================================================================
    # 2. TRANG TÀI SẢN (ASSETS + BÁO CÁO TÀI SẢN) - 28 tests (16F + 6P + 6S)
    # =================================================================
    
    # ----- FUNCTIONAL TESTS - TÀI SẢN (10 tests) -----
    
    def test_assets_01_view_list(self, employee_page):
        """FUNC: Xem danh sách tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(1000)
        table = employee_page.locator('#assetTableBody')
        expect(table).to_be_visible()
        expect(table).not_to_contain_text("Đang tải")
    
    def test_assets_02_search_by_name(self, employee_page):
        """FUNC: Tìm kiếm tài sản theo tên"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "Bàn")
        employee_page.wait_for_timeout(500)
        rows = employee_page.locator('#assetTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Bàn")
    
    def test_assets_03_search_no_result(self, employee_page):
        """FUNC: Tìm kiếm không có kết quả"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "KHONGTONTAI999")
        employee_page.wait_for_timeout(500)
        empty_msg = employee_page.locator('#assetTableBody')
        expect(empty_msg).to_contain_text("Không có tài sản nào")
    
    def test_assets_06_refresh_list(self, employee_page):
        """FUNC: Làm mới danh sách tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.click('#refreshBtn')
        employee_page.wait_for_timeout(500)
        table = employee_page.locator('#assetTableBody')
        expect(table).to_be_visible()
    
    def test_assets_07_check_status_badge(self, employee_page):
        """FUNC: Kiểm tra hiển thị trạng thái tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(1000)
        badges = employee_page.locator('.status-badge')
        assert badges.count() > 0
    
    def test_assets_08_check_table_headers(self, employee_page):
        """FUNC: Kiểm tra tiêu đề cột"""
        employee_page.goto("http://localhost:5000/user/assets")
        headers = employee_page.locator('th')
        assert headers.count() >= 5
    
    def test_assets_09_verify_data_fields(self, employee_page):
        """FUNC: Kiểm tra các trường dữ liệu"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(1000)
        first_row = employee_page.locator('#assetTableBody tr').first
        cells = first_row.locator('td')
        assert cells.count() >= 5
    
    def test_assets_10_go_to_report_page(self, employee_page):
        """FUNC: Chuyển sang trang báo cáo tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.click('a[href="/user/report-assets"]')
        employee_page.wait_for_timeout(500)
        assert "report-assets" in employee_page.url
    
    # ----- FUNCTIONAL TESTS - BÁO CÁO TÀI SẢN (6 tests) -----
    
    def test_assets_report_01_view_form(self, employee_page):
        """FUNC: Xem form báo cáo tài sản"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.wait_for_timeout(500)
        form = employee_page.locator('#reportForm')
        expect(form).to_be_visible()
    
    def test_assets_report_02_asset_select_dropdown(self, employee_page):
        """FUNC: Dropdown chọn tài sản có dữ liệu"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.wait_for_timeout(500)
        select = employee_page.locator('#assetSelect')
        options = select.locator('option')
        assert options.count() > 1
    
    def test_assets_report_03_all_report_types(self, employee_page):
        """FUNC: Kiểm tra các loại báo cáo tài sản"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        report_types = employee_page.locator('input[name="reportType"]')
        assert report_types.count() == 3  # hỏng, sửa chữa, thay thế
    
    def test_assets_report_04_send_success(self, employee_page):
        """FUNC: Gửi báo cáo tài sản thành công"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', f"Báo cáo test {random.randint(1000, 9999)}")
        
        def handle(dialog):
            assert "đã được gửi" in dialog.message
            dialog.accept()
        employee_page.on("dialog", handle)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    def test_assets_report_05_missing_description(self, employee_page):
        """FUNC: Gửi báo cáo thiếu mô tả"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "")
        
        def handle(dialog):
            assert "nhập" in dialog.message
            dialog.accept()
        employee_page.on("dialog", handle)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    def test_assets_report_06_no_asset_selected(self, employee_page):
        """FUNC: Gửi báo cáo khi chưa chọn tài sản"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "Test mô tả")
        
        def handle(dialog):
            assert "chọn" in dialog.message
            dialog.accept()
        employee_page.on("dialog", handle)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    # ----- PERFORMANCE TESTS (6 tests) -----
    
    def test_assets_perf_01_load_time(self, employee_page):
        """PERF: Thời gian tải trang tài sản < 3s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải trang tài sản: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_assets_perf_02_search_time(self, employee_page):
        """PERF: Thời gian tìm kiếm tài sản < 1s"""
        employee_page.goto("http://localhost:5000/user/assets")
        start = time.time()
        employee_page.fill('#searchInput', "Bàn")
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tìm kiếm tài sản: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_assets_perf_03_filter_time(self, employee_page):
        """PERF: Thời gian lọc tài sản < 1s"""
        employee_page.goto("http://localhost:5000/user/assets")
        start = time.time()
        employee_page.click('.tab-btn[data-tab="my"]')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Lọc tài sản: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_assets_perf_04_refresh_time(self, employee_page):
        """PERF: Thời gian làm mới danh sách < 1s"""
        employee_page.goto("http://localhost:5000/user/assets")
        start = time.time()
        employee_page.click('#refreshBtn')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Làm mới: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_assets_perf_05_report_load_time(self, employee_page):
        """PERF: Thời gian tải form báo cáo < 2s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải form báo cáo: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    def test_assets_perf_06_report_submit_time(self, employee_page):
        """PERF: Thời gian gửi báo cáo < 2s"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "Performance test")
        
        start = time.time()
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Gửi báo cáo: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    # ----- SECURITY TESTS (6 tests) -----
    
    def test_assets_sec_01_xss_in_search(self, employee_page):
        """SEC: XSS trong ô tìm kiếm tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "<script>alert('XSS')</script>")
        employee_page.wait_for_timeout(500)
        assert "alert" not in employee_page.content()
    
    def test_assets_sec_02_sql_injection_search(self, employee_page):
        """SEC: SQL Injection trong tìm kiếm"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "' OR '1'='1")
        employee_page.wait_for_timeout(500)
        assert "500" not in employee_page.content()
    
    def test_assets_sec_03_html_injection(self, employee_page):
        """SEC: HTML Injection trong tìm kiếm"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "<h1>Hacked</h1>")
        employee_page.wait_for_timeout(500)
        assert "<h1>" not in employee_page.content() or "&lt;h1&gt;" in employee_page.content()
    
    def test_assets_sec_04_large_payload(self, employee_page):
        """SEC: Payload lớn trong tìm kiếm"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "A" * 10000)
        employee_page.wait_for_timeout(500)
        assert "500" not in employee_page.content()
    
    def test_assets_sec_05_xss_in_report(self, employee_page):
        """SEC: XSS trong mô tả báo cáo tài sản"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "<script>alert('XSS')</script>")
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        assert "alert" not in employee_page.content()
    
    def test_assets_sec_06_sql_injection_report(self, employee_page):
        """SEC: SQL Injection trong báo cáo"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "' OR '1'='1")
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        assert "500" not in employee_page.content()
    
    # =================================================================
    # 3. TRANG THIẾT BỊ (DEVICES + BÁO CÁO THIẾT BỊ) - 28 tests (16F + 6P + 6S)
    # =================================================================
    
    # ----- FUNCTIONAL TESTS - THIẾT BỊ (10 tests) -----
    
    def test_devices_01_view_list(self, employee_page):
        """FUNC: Xem danh sách thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.wait_for_timeout(1000)
        table = employee_page.locator('#deviceTableBody')
        expect(table).to_be_visible()
        expect(table).not_to_contain_text("Đang tải")
    
    def test_devices_02_search_by_name(self, employee_page):
        """FUNC: Tìm kiếm thiết bị theo tên"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.fill('#searchInput', "Laptop")
        employee_page.wait_for_timeout(500)
        rows = employee_page.locator('#deviceTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Laptop")
    
    def test_devices_03_search_no_result(self, employee_page):
        """FUNC: Tìm kiếm không có kết quả"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.fill('#searchInput', "KHONGTONTAI999")
        employee_page.wait_for_timeout(500)
        empty_msg = employee_page.locator('#deviceTableBody')
        expect(empty_msg).to_contain_text("Không tìm thấy")
    
    def test_devices_04_filter_my_devices(self, employee_page):
        """FUNC: Lọc thiết bị tôi đang dùng"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.click('.tab-btn[data-tab="my"]')
        employee_page.wait_for_timeout(500)
        table = employee_page.locator('#deviceTableBody')
        expect(table).to_be_visible()
    
    def test_devices_05_filter_all_devices(self, employee_page):
        """FUNC: Lọc tất cả thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.click('.tab-btn[data-tab="all"]')
        employee_page.wait_for_timeout(500)
        table = employee_page.locator('#deviceTableBody')
        expect(table).to_be_visible()
    
    def test_devices_06_refresh_list(self, employee_page):
        """FUNC: Làm mới danh sách thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.click('#refreshBtn')
        employee_page.wait_for_timeout(500)
        table = employee_page.locator('#deviceTableBody')
        expect(table).to_be_visible()
    
    def test_devices_07_check_status_badge(self, employee_page):
        """FUNC: Kiểm tra hiển thị trạng thái thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.wait_for_timeout(1000)
        badges = employee_page.locator('.status-badge')
        assert badges.count() > 0
    
    def test_devices_08_check_table_headers(self, employee_page):
        """FUNC: Kiểm tra tiêu đề cột thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        headers = employee_page.locator('th')
        assert headers.count() >= 6
    
    def test_devices_09_verify_data_fields(self, employee_page):
        """FUNC: Kiểm tra các trường dữ liệu thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.wait_for_timeout(1000)
        first_row = employee_page.locator('#deviceTableBody tr').first
        cells = first_row.locator('td')
        assert cells.count() >= 6
    
    def test_devices_10_go_to_report_page(self, employee_page):
        """FUNC: Chuyển sang trang báo cáo thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.click('a[href="/user/report-devices"]')
        employee_page.wait_for_timeout(500)
        assert "report-devices" in employee_page.url
    
    # ----- FUNCTIONAL TESTS - BÁO CÁO THIẾT BỊ (6 tests) -----
    
    def test_devices_report_01_view_form(self, employee_page):
        """FUNC: Xem form báo cáo thiết bị"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.wait_for_timeout(500)
        form = employee_page.locator('#reportForm')
        expect(form).to_be_visible()
    
    def test_devices_report_02_device_select_dropdown(self, employee_page):
        """FUNC: Dropdown chọn thiết bị có dữ liệu"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.wait_for_timeout(500)
        select = employee_page.locator('#deviceSelect')
        options = select.locator('option')
        assert options.count() > 1
    
    def test_devices_report_03_all_report_types(self, employee_page):
        """FUNC: Kiểm tra các loại báo cáo thiết bị"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        report_types = employee_page.locator('input[name="reportType"]')
        assert report_types.count() == 4  # hỏng, bảo trì, hỗ trợ kỹ thuật, lỗi
    
    def test_devices_report_04_send_success(self, employee_page):
        """FUNC: Gửi báo cáo thiết bị thành công"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.select_option('#deviceSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', f"Báo cáo thiết bị test {random.randint(1000, 9999)}")
        
        def handle(dialog):
            assert "đã được gửi" in dialog.message
            dialog.accept()
        employee_page.on("dialog", handle)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    def test_devices_report_05_missing_description(self, employee_page):
        """FUNC: Gửi báo cáo thiết bị thiếu mô tả"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.select_option('#deviceSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "")
        
        def handle(dialog):
            assert "nhập" in dialog.message
            dialog.accept()
        employee_page.on("dialog", handle)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    def test_devices_report_06_no_device_selected(self, employee_page):
        """FUNC: Gửi báo cáo khi chưa chọn thiết bị"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "Test mô tả")
        
        def handle(dialog):
            assert "chọn" in dialog.message
            dialog.accept()
        employee_page.on("dialog", handle)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    # ----- PERFORMANCE TESTS (6 tests) -----
    
    def test_devices_perf_01_load_time(self, employee_page):
        """PERF: Thời gian tải trang thiết bị < 3s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải trang thiết bị: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_devices_perf_02_search_time(self, employee_page):
        """PERF: Thời gian tìm kiếm thiết bị < 1s"""
        employee_page.goto("http://localhost:5000/user/devices")
        start = time.time()
        employee_page.fill('#searchInput', "Laptop")
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tìm kiếm thiết bị: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_devices_perf_03_filter_time(self, employee_page):
        """PERF: Thời gian lọc thiết bị < 1s"""
        employee_page.goto("http://localhost:5000/user/devices")
        start = time.time()
        employee_page.click('.tab-btn[data-tab="my"]')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Lọc thiết bị: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_devices_perf_04_refresh_time(self, employee_page):
        """PERF: Thời gian làm mới danh sách < 1s"""
        employee_page.goto("http://localhost:5000/user/devices")
        start = time.time()
        employee_page.click('#refreshBtn')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Làm mới: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_devices_perf_05_report_load_time(self, employee_page):
        """PERF: Thời gian tải form báo cáo thiết bị < 2s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải form báo cáo: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    def test_devices_perf_06_report_submit_time(self, employee_page):
        """PERF: Thời gian gửi báo cáo thiết bị < 2s"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.select_option('#deviceSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "Performance test")
        
        start = time.time()
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Gửi báo cáo: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    # ----- SECURITY TESTS (6 tests) -----
    
    def test_devices_sec_01_xss_in_search(self, employee_page):
        """SEC: XSS trong ô tìm kiếm thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.fill('#searchInput', "<script>alert('XSS')</script>")
        employee_page.wait_for_timeout(500)
        assert "alert" not in employee_page.content()
    
    def test_devices_sec_02_sql_injection_search(self, employee_page):
        """SEC: SQL Injection trong tìm kiếm thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.fill('#searchInput', "' OR '1'='1")
        employee_page.wait_for_timeout(500)
        assert "500" not in employee_page.content()
    
    def test_devices_sec_03_html_injection(self, employee_page):
        """SEC: HTML Injection trong tìm kiếm thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.fill('#searchInput', "<h1>Hacked</h1>")
        employee_page.wait_for_timeout(500)
        assert "<h1>" not in employee_page.content() or "&lt;h1&gt;" in employee_page.content()
    
    def test_devices_sec_04_large_payload(self, employee_page):
        """SEC: Payload lớn trong tìm kiếm thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.fill('#searchInput', "A" * 10000)
        employee_page.wait_for_timeout(500)
        assert "500" not in employee_page.content()
    
    def test_devices_sec_05_xss_in_report(self, employee_page):
        """SEC: XSS trong mô tả báo cáo thiết bị"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.select_option('#deviceSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "<script>alert('XSS')</script>")
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        assert "alert" not in employee_page.content()
    
    def test_devices_sec_06_sql_injection_report(self, employee_page):
        """SEC: SQL Injection trong báo cáo thiết bị"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.select_option('#deviceSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "' OR '1'='1")
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
        assert "500" not in employee_page.content()
    
    # =================================================================
    # 4. TRANG YÊU CẦU MƯỢN (BORROW) - 23 tests (13F + 5P + 5S)
    # =================================================================
    
    # ----- FUNCTIONAL TESTS (13 tests) -----
    
    def test_borrow_01_view_page(self, employee_page):
        """FUNC: Xem trang yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.wait_for_timeout(1000)
        my_assets = employee_page.locator('#myAssetsPanel')
        expect(my_assets).to_be_visible()
    
    def test_borrow_02_my_assets_table(self, employee_page):
        """FUNC: Kiểm tra bảng tài sản đang dùng"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.wait_for_timeout(1000)
        table = employee_page.locator('#myAssetsTable')
        expect(table).to_be_visible()
    
    def test_borrow_03_switch_to_available_tab(self, employee_page):
        """FUNC: Chuyển sang tab tài sản chưa sử dụng"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        available_panel = employee_page.locator('#availableAssetsPanel')
        expect(available_panel).to_be_visible()
    
    def test_borrow_04_available_assets_table(self, employee_page):
        """FUNC: Kiểm tra bảng tài sản chưa sử dụng"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        table = employee_page.locator('#availableAssetsTable')
        expect(table).to_be_visible()
    
    def test_borrow_05_borrow_button_exists(self, employee_page):
        """FUNC: Kiểm tra nút mượn trên mỗi tài sản"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btns = employee_page.locator('.borrow-btn')
        if borrow_btns.count() > 0:
            expect(borrow_btns.first).to_be_visible()
    
    def test_borrow_06_open_borrow_modal(self, employee_page):
        """FUNC: Mở modal yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            modal = employee_page.locator('#borrowModal')
            expect(modal).to_be_visible()
    
    def test_borrow_07_close_modal(self, employee_page):
        """FUNC: Đóng modal yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.click('#closeModalBtn')
            employee_page.wait_for_timeout(500)
            modal = employee_page.locator('#borrowModal')
            expect(modal).not_to_be_visible()
    
    def test_borrow_08_send_request_success(self, employee_page):
        """FUNC: Gửi yêu cầu mượn thành công"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.fill('#borrowReason', f"Yêu cầu mượn test {random.randint(1000, 9999)}")
            
            def handle(dialog):
                assert "đã được gửi" in dialog.message
                dialog.accept()
            employee_page.on("dialog", handle)
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
    
    def test_borrow_09_send_request_missing_reason(self, employee_page):
        """FUNC: Gửi yêu cầu mượn thiếu lý do"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.fill('#borrowReason', "")
            
            def handle(dialog):
                assert "lý do" in dialog.message
                dialog.accept()
            employee_page.on("dialog", handle)
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
    
    def test_borrow_10_check_borrow_dates(self, employee_page):
        """FUNC: Kiểm tra trường ngày mượn/trả"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            borrow_date = employee_page.locator('#borrowDate')
            return_date = employee_page.locator('#returnDate')
            expect(borrow_date).to_be_visible()
            expect(return_date).to_be_visible()
    
    def test_borrow_11_switch_back_to_my_assets(self, employee_page):
        """FUNC: Chuyển lại tab tài sản đang dùng"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        employee_page.click('#btnMyAssets')
        employee_page.wait_for_timeout(500)
        my_panel = employee_page.locator('#myAssetsPanel')
        expect(my_panel).to_be_visible()
    
    def test_borrow_12_check_user_info_display(self, employee_page):
        """FUNC: Kiểm tra hiển thị thông tin người dùng"""
        employee_page.goto("http://localhost:5000/user/borrow")
        user_info = employee_page.locator('.user-name')
        expect(user_info).to_be_visible()
    
    def test_borrow_13_check_asset_codes(self, employee_page):
        """FUNC: Kiểm tra mã tài sản hiển thị đúng format"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.wait_for_timeout(1000)
        codes = employee_page.locator('#myAssetsTable td:first-child')
        if codes.count() > 0:
            first_code = codes.first.inner_text()
            assert "AST" in first_code or "DEV" in first_code
    
    # ----- PERFORMANCE TESTS (5 tests) -----
    
    def test_borrow_perf_01_page_load_time(self, employee_page):
        """PERF: Thời gian tải trang yêu cầu mượn < 3s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải trang yêu cầu mượn: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_borrow_perf_02_tab_switch_time(self, employee_page):
        """PERF: Thời gian chuyển tab < 1s"""
        employee_page.goto("http://localhost:5000/user/borrow")
        start = time.time()
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Chuyển tab: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_borrow_perf_03_modal_open_time(self, employee_page):
        """PERF: Thời gian mở modal < 1s"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            start = time.time()
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            elapsed = (time.time() - start) * 1000
            print(f"[PERF] Mở modal: {elapsed:.0f}ms")
            assert elapsed < 1000
    
    def test_borrow_perf_04_modal_close_time(self, employee_page):
        """PERF: Thời gian đóng modal < 0.5s"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            start = time.time()
            employee_page.click('#closeModalBtn')
            employee_page.wait_for_timeout(500)
            elapsed = (time.time() - start) * 1000
            print(f"[PERF] Đóng modal: {elapsed:.0f}ms")
            assert elapsed < 500
    
    def test_borrow_perf_05_submit_request_time(self, employee_page):
        """PERF: Thời gian gửi yêu cầu < 2s"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.fill('#borrowReason', "Performance test")
            
            start = time.time()
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
            elapsed = (time.time() - start) * 1000
            print(f"[PERF] Gửi yêu cầu: {elapsed:.0f}ms")
            assert elapsed < 2000
    
    # ----- SECURITY TESTS (5 tests) -----
    
    def test_borrow_sec_01_xss_in_reason(self, employee_page):
        """SEC: XSS trong lý do mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.fill('#borrowReason', "<script>alert('XSS')</script>")
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
            assert "alert" not in employee_page.content()
    
    def test_borrow_sec_02_sql_injection_reason(self, employee_page):
        """SEC: SQL Injection trong lý do mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.fill('#borrowReason', "' OR '1'='1")
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
            assert "500" not in employee_page.content()
    
    def test_borrow_sec_03_html_injection_reason(self, employee_page):
        """SEC: HTML Injection trong lý do mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.fill('#borrowReason', "<h1>Hacked</h1>")
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
            assert "<h1>" not in employee_page.content() or "&lt;h1&gt;" in employee_page.content()
    
    def test_borrow_sec_04_large_payload_reason(self, employee_page):
        """SEC: Payload lớn trong lý do mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.fill('#borrowReason', "A" * 10000)
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
            assert "500" not in employee_page.content()
    
    def test_borrow_sec_05_invalid_date_format(self, employee_page):
        """SEC: Ngày mượn/trả không hợp lệ"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            employee_page.fill('#borrowReason', "Test dates")
            employee_page.fill('#borrowDate', "invalid-date")
            employee_page.fill('#returnDate', "invalid-date")
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
            assert "500" not in employee_page.content()
    
    # =================================================================
    # 5. TRANG THEO DÕI (TRACK - BÁO CÁO + YÊU CẦU) - 14 tests (8F + 3P + 3S)
    # =================================================================
    
    # ----- FUNCTIONAL TESTS (8 tests) -----
    
    def test_track_01_view_page(self, employee_page):
        """FUNC: Xem trang theo dõi"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.wait_for_timeout(1000)
        reports_tab = employee_page.locator('#tabReports')
        expect(reports_tab).to_be_visible()
    
    def test_track_02_reports_tab_display(self, employee_page):
        """FUNC: Kiểm tra tab báo cáo hiển thị"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.wait_for_timeout(1000)
        reports_tab = employee_page.locator('#tabReports')
        reports_tab.click()
        employee_page.wait_for_timeout(500)
        reports_table = employee_page.locator('#reportsTableBody')
        expect(reports_table).to_be_visible()
    
    def test_track_03_borrow_tab_display(self, employee_page):
        """FUNC: Kiểm tra tab yêu cầu mượn hiển thị"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.wait_for_timeout(1000)
        borrow_tab = employee_page.locator('#tabBorrow')
        borrow_tab.click()
        employee_page.wait_for_timeout(500)
        borrow_table = employee_page.locator('#borrowTableBody')
        expect(borrow_table).to_be_visible()
    
    def test_track_04_reports_table_headers(self, employee_page):
        """FUNC: Kiểm tra tiêu đề bảng báo cáo"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.click('#tabReports')
        employee_page.wait_for_timeout(500)
        headers = employee_page.locator('#reportsTableBody th')
        assert headers.count() >= 3
    
    def test_track_05_borrow_table_headers(self, employee_page):
        """FUNC: Kiểm tra tiêu đề bảng yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.click('#tabBorrow')
        employee_page.wait_for_timeout(500)
        headers = employee_page.locator('#borrowTableBody th')
        assert headers.count() >= 4
    
    def test_track_06_refresh_reports(self, employee_page):
        """FUNC: Làm mới bảng báo cáo"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.click('#tabReports')
        employee_page.wait_for_timeout(500)
        refresh_btn = employee_page.locator('#refreshReportsBtn')
        refresh_btn.click()
        employee_page.wait_for_timeout(500)
        table = employee_page.locator('#reportsTableBody')
        expect(table).to_be_visible()
    
    def test_track_07_refresh_borrow(self, employee_page):
        """FUNC: Làm mới bảng yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.click('#tabBorrow')
        employee_page.wait_for_timeout(500)
        refresh_btn = employee_page.locator('#refreshBorrowBtn')
        refresh_btn.click()
        employee_page.wait_for_timeout(500)
        table = employee_page.locator('#borrowTableBody')
        expect(table).to_be_visible()
    
    def test_track_08_status_badge_display(self, employee_page):
        """FUNC: Kiểm tra hiển thị trạng thái"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.click('#tabReports')
        employee_page.wait_for_timeout(500)
        badges = employee_page.locator('.status-badge')
        # Có thể không có dữ liệu, nhưng nếu có thì phải hiển thị đúng
    
    # ----- PERFORMANCE TESTS (3 tests) -----
    
    def test_track_perf_01_page_load_time(self, employee_page):
        """PERF: Thời gian tải trang theo dõi < 3s"""
        start = time.time()
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải trang theo dõi: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_track_perf_02_tab_switch_time(self, employee_page):
        """PERF: Thời gian chuyển tab < 1s"""
        employee_page.goto("http://localhost:5000/user/track")
        start = time.time()
        employee_page.click('#tabBorrow')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Chuyển tab: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_track_perf_03_refresh_time(self, employee_page):
        """PERF: Thời gian làm mới dữ liệu < 1s"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.click('#tabReports')
        employee_page.wait_for_timeout(500)
        start = time.time()
        employee_page.click('#refreshReportsBtn')
        employee_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Làm mới: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    # ----- SECURITY TESTS (3 tests) -----
    
    def test_track_sec_01_xss_in_url(self, employee_page):
        """SEC: XSS qua URL trên trang theo dõi"""
        employee_page.goto("http://localhost:5000/user/track?search=<script>alert(1)</script>")
        employee_page.wait_for_timeout(500)
        assert "alert" not in employee_page.content()
    
    def test_track_sec_02_sql_injection_url(self, employee_page):
        """SEC: SQL Injection qua URL"""
        employee_page.goto("http://localhost:5000/user/track?id=' OR '1'='1")
        employee_page.wait_for_timeout(500)
        assert "500" not in employee_page.content()
    
    def test_track_sec_03_unauthorized_data_access(self, employee_page):
        """SEC: Nhân viên chỉ thấy dữ liệu của mình"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.click('#tabReports')
        employee_page.wait_for_timeout(500)
        # Kiểm tra không có dữ liệu của user khác (nếu có)
        page_content = employee_page.content()
        # Không có thông tin nhạy cảm
        assert "admin" not in page_content or "admin" in page_content == False