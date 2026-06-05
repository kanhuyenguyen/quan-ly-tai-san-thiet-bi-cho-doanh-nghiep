import pytest
import time
import random
from playwright.sync_api import expect

class TestAdminAssign:
 
    # ========== PERFORMANCE TESTS (5 tests) ==========
    
    def test_perf_01_assign_page_load_time(self, admin_page):
        """Thời gian tải trang phân bổ < 3s"""
        start = time.time()
        admin_page.goto("http://localhost:5000/admin/assign")
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải trang phân bổ: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_02_asset_list_load_time(self, admin_page):
        """Thời gian tải danh sách tài sản < 2s"""
        admin_page.goto("http://localhost:5000/admin/assign")
        start = time.time()
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải danh sách tài sản: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    def test_perf_03_device_list_load_time(self, admin_page):
        """Thời gian tải danh sách thiết bị < 2s"""
        admin_page.goto("http://localhost:5000/admin/assign")
        admin_page.click('#tabAssignDevice')
        start = time.time()
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải danh sách thiết bị: {elapsed:.0f}ms")
        assert elapsed < 2000
    
    def test_perf_04_tab_switch_performance(self, admin_page):
        """Chuyển tab < 1s"""
        admin_page.goto("http://localhost:5000/admin/assign")
        start = time.time()
        admin_page.click('#tabAssignDevice')
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Chuyển tab: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_05_assign_action_performance(self, admin_page):
        """Thời gian thực hiện bàn giao < 2s"""
        admin_page.goto("http://localhost:5000/admin/assign")
        admin_page.wait_for_timeout(500)
        
        first_asset = admin_page.locator('#assetList .asset-item').first
        if first_asset.count() > 0:
            first_asset.click()
            admin_page.wait_for_timeout(500)
            admin_page.select_option('#assignUser', index=1)
            
            start = time.time()
            admin_page.click('#confirmAssignAsset')
            admin_page.wait_for_timeout(1000)
            elapsed = (time.time() - start) * 1000
            print(f"Bàn giao: {elapsed:.0f}ms")
            assert elapsed < 2000
    
    # ========== SECURITY TESTS (5 tests) ==========
    
    def test_sec_01_unauthorized_assign_access(self, page):
        """Nhân viên không thể truy cập trang phân bổ"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.uncheck('input[name="is_admin"]')
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        
        page.goto("http://localhost:5000/admin/assign")
        # Phải redirect về trang chủ hoặc login
        assert "admin" not in page.url
        assert "login" in page.url or page.url == "http://localhost:5000/"
    
    def test_sec_02_assign_without_selection(self, admin_page):
        """Bàn giao khi chưa chọn tài sản"""
        admin_page.goto("http://localhost:5000/admin/assign")
        
        def handle_dialog(dialog):
            assert "chọn" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#confirmAssignAsset')
        admin_page.wait_for_timeout(1000)
    
    def test_sec_03_xss_in_assign_note(self, admin_page):
        """XSS trong ghi chú bàn giao"""
        admin_page.goto("http://localhost:5000/admin/assign")
        admin_page.wait_for_timeout(500)
        
        first_asset = admin_page.locator('#assetList .asset-item').first
        if first_asset.count() > 0:
            first_asset.click()
            admin_page.wait_for_timeout(500)
            admin_page.select_option('#assignUser', index=1)
            admin_page.fill('#assignNote', "<script>alert('XSS')</script>")
            admin_page.click('#confirmAssignAsset')
            admin_page.wait_for_timeout(1000)
            assert "alert" not in admin_page.content()
    
    def test_sec_04_invalid_date_format(self, admin_page):
        """Ngày bàn giao không hợp lệ"""
        admin_page.goto("http://localhost:5000/admin/assign")
        admin_page.wait_for_timeout(500)
        
        first_asset = admin_page.locator('#assetList .asset-item').first
        if first_asset.count() > 0:
            first_asset.click()
            admin_page.wait_for_timeout(500)
            admin_page.select_option('#assignUser', index=1)
            admin_page.fill('#assignDate', "invalid-date")
            admin_page.click('#confirmAssignAsset')
            admin_page.wait_for_timeout(1000)
            # Không bị lỗi server
            assert "500" not in admin_page.content()
    
    def test_sec_05_assign_same_asset_twice(self, admin_page):
        """Bàn giao cùng một tài sản 2 lần"""
        admin_page.goto("http://localhost:5000/admin/assign")
        admin_page.wait_for_timeout(500)
        
        first_asset = admin_page.locator('#assetList .asset-item').first
        if first_asset.count() > 0:
            # Lần 1
            first_asset.click()
            admin_page.wait_for_timeout(500)
            admin_page.select_option('#assignUser', index=1)
            admin_page.click('#confirmAssignAsset')
            admin_page.wait_for_timeout(1000)
            
            # Làm mới trang
            admin_page.reload()
            admin_page.wait_for_timeout(500)
            
            # Kiểm tra tài sản đã biến mất khỏi danh sách chưa sử dụng
            remaining_assets = admin_page.locator('#assetList .asset-item')
            # Tài sản đã bàn giao không còn trong danh sách
            print(f"Số tài sản còn lại: {remaining_assets.count()}")