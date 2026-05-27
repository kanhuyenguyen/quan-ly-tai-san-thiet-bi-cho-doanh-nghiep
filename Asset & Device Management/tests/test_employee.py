import pytest
from playwright.sync_api import expect
import random

class TestEmployee:
    
    # ========== TRANG CHỦ ==========
    
    def test_employee_view_home(self, employee_page):
        """TC-EMP-01: Nhân viên xem trang chủ"""
        employee_page.goto("http://localhost:5000/")
        employee_page.wait_for_timeout(1000)
        
        # Kiểm tra tiêu đề trang
        assert "Asset & Device Management" in employee_page.title()
    
    # ========== XEM TÀI SẢN ==========
    
    def test_employee_view_assets(self, employee_page):
        """TC-EMP-02: Nhân viên xem danh sách tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(1000)
        
        table = employee_page.locator('#assetTableBody')
        expect(table).to_be_visible()
        expect(table).not_to_contain_text("Đang tải")
    
    def test_employee_search_assets(self, employee_page):
        """TC-EMP-03: Nhân viên tìm kiếm tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.fill('#searchInput', "Bàn")
        employee_page.wait_for_timeout(500)
        
        rows = employee_page.locator('#assetTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Bàn")
    
    # ========== XEM THIẾT BỊ ==========
    
    def test_employee_view_devices(self, employee_page):
        """TC-EMP-04: Nhân viên xem danh sách thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.wait_for_timeout(1000)
        
        table = employee_page.locator('#deviceTableBody')
        expect(table).to_be_visible()
        expect(table).not_to_contain_text("Đang tải")
    
    def test_employee_search_devices(self, employee_page):
        """TC-EMP-05: Nhân viên tìm kiếm thiết bị"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.fill('#searchInput', "Laptop")
        employee_page.wait_for_timeout(500)
        
        rows = employee_page.locator('#deviceTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Laptop")
    
    # ========== BÁO CÁO TÀI SẢN ==========
    
    def test_employee_send_asset_report(self, employee_page):
        """TC-EMP-06: Nhân viên gửi báo cáo tài sản"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.wait_for_timeout(500)
        
        # Chọn tài sản đầu tiên
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', f"Test báo cáo tài sản {random.randint(1000, 9999)}")
        
        def handle_dialog(dialog):
            assert "đã được gửi" in dialog.message
            dialog.accept()
        
        employee_page.on("dialog", handle_dialog)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    def test_employee_send_asset_report_missing_description(self, employee_page):
        """TC-EMP-07: Gửi báo cáo tài sản thiếu mô tả"""
        employee_page.goto("http://localhost:5000/user/report-assets")
        employee_page.wait_for_timeout(500)
        
        employee_page.select_option('#assetSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', "")
        
        def handle_dialog(dialog):
            assert "Vui lòng nhập" in dialog.message
            dialog.accept()
        
        employee_page.on("dialog", handle_dialog)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    # ========== BÁO CÁO THIẾT BỊ ==========
    
    def test_employee_send_device_report(self, employee_page):
        """TC-EMP-08: Nhân viên gửi báo cáo thiết bị"""
        employee_page.goto("http://localhost:5000/user/report-devices")
        employee_page.wait_for_timeout(500)
        
        employee_page.select_option('#deviceSelect', index=1)
        employee_page.check('input[value="broken"]')
        employee_page.fill('#description', f"Test báo cáo thiết bị {random.randint(1000, 9999)}")
        
        def handle_dialog(dialog):
            assert "đã được gửi" in dialog.message
            dialog.accept()
        
        employee_page.on("dialog", handle_dialog)
        employee_page.click('#reportForm button[type="submit"]')
        employee_page.wait_for_timeout(1000)
    
    # ========== YÊU CẦU MƯỢN ==========
    
    def test_employee_view_borrow_page(self, employee_page):
        """TC-EMP-09: Nhân viên xem trang yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.wait_for_timeout(1000)
        
        # Kiểm tra hiển thị 2 panel
        my_assets = employee_page.locator('#myAssetsPanel')
        available_assets = employee_page.locator('#availableAssetsPanel')
        expect(my_assets).to_be_visible()
        expect(available_assets).not_to_be_visible()
    
    def test_employee_switch_to_available_assets(self, employee_page):
        """TC-EMP-10: Chuyển sang tab tài sản chưa sử dụng"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        
        available_assets = employee_page.locator('#availableAssetsPanel')
        expect(available_assets).to_be_visible()
    
    def test_employee_send_borrow_request(self, employee_page):
        """TC-EMP-11: Gửi yêu cầu mượn tài sản"""
        employee_page.goto("http://localhost:5000/user/borrow")
        employee_page.click('#BtnAvailableAssets')
        employee_page.wait_for_timeout(500)
        
        # Click nút mượn đầu tiên
        borrow_btn = employee_page.locator('.borrow-btn').first
        if borrow_btn.count() > 0:
            borrow_btn.click()
            employee_page.wait_for_timeout(500)
            
            employee_page.fill('#borrowReason', f"Test mượn tài sản {random.randint(1000, 9999)}")
            
            def handle_dialog(dialog):
                assert "đã được gửi" in dialog.message
                dialog.accept()
            
            employee_page.on("dialog", handle_dialog)
            employee_page.click('#submitBorrowBtn')
            employee_page.wait_for_timeout(1000)
    
    # ========== THEO DÕI TRẠNG THÁI ==========
    
    def test_employee_view_track_reports(self, employee_page):
        """TC-EMP-12: Xem theo dõi báo cáo"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.wait_for_timeout(1000)
        
        # Kiểm tra tab báo cáo
        reports_tab = employee_page.locator('#tabReports')
        expect(reports_tab).to_be_visible()
        reports_tab.click()
        employee_page.wait_for_timeout(500)
        
        reports_table = employee_page.locator('#reportsTableBody')
        expect(reports_table).to_be_visible()
    
    def test_employee_view_track_borrow(self, employee_page):
        """TC-EMP-13: Xem theo dõi yêu cầu mượn"""
        employee_page.goto("http://localhost:5000/user/track")
        employee_page.wait_for_timeout(1000)
        
        borrow_tab = employee_page.locator('#tabBorrow')
        expect(borrow_tab).to_be_visible()
        borrow_tab.click()
        employee_page.wait_for_timeout(500)
        
        borrow_table = employee_page.locator('#borrowTableBody')
        expect(borrow_table).to_be_visible()
    
    # ========== TÀI SẢN ĐANG SỬ DỤNG ==========
    
    def test_employee_view_my_assets_tab(self, employee_page):
        """TC-EMP-14: Xem tài sản đang sử dụng (tab My Assets)"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(1000)
        
        # Kiểm tra bảng hiển thị tài sản
        table = employee_page.locator('#assetTableBody')
        expect(table).to_be_visible()
    
    # ========== THIẾT BỊ ĐANG SỬ DỤNG ==========
    
    def test_employee_view_my_devices_tab(self, employee_page):
        """TC-EMP-15: Xem thiết bị đang sử dụng"""
        employee_page.goto("http://localhost:5000/user/devices")
        employee_page.wait_for_timeout(1000)
        
        table = employee_page.locator('#deviceTableBody')
        expect(table).to_be_visible()
    
    # ========== LÀM MỚI DỮ LIỆU ==========
    
    def test_employee_refresh_assets(self, employee_page):
        """TC-EMP-16: Làm mới danh sách tài sản"""
        employee_page.goto("http://localhost:5000/user/assets")
        employee_page.wait_for_timeout(500)
        
        refresh_btn = employee_page.locator('#refreshBtn')
        refresh_btn.click()
        employee_page.wait_for_timeout(500)
        
        table = employee_page.locator('#assetTableBody')
        expect(table).to_be_visible()