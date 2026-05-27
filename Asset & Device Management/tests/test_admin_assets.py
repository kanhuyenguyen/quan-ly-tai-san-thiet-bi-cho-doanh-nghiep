import pytest
from playwright.sync_api import expect
import random

class TestAdminAssets:
    
    # ========== KIỂM TRA HIỂN THỊ ==========
    
    def test_view_assets_list(self, admin_page):
        """TC-ASSET-01: Xem danh sách tài sản"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(1000)
        
        # Kiểm tra bảng tài sản hiển thị
        table = admin_page.locator('#assetsTableBody')
        expect(table).to_be_visible()
        
        # Kiểm tra không còn thông báo "Đang tải"
        expect(table).not_to_contain_text("Đang tải")
    
    def test_view_devices_list(self, admin_page):
        """TC-DEVICE-01: Xem danh sách thiết bị"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(1000)
        
        table = admin_page.locator('#devicesTableBody')
        expect(table).to_be_visible()
        expect(table).not_to_contain_text("Đang tải")
    
    def test_view_return_list(self, admin_page):
        """TC-RETURN-01: Xem danh sách hoàn trả"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabReturn')
        admin_page.wait_for_timeout(1000)
        
        table = admin_page.locator('#returnTableBody')
        expect(table).to_be_visible()
        expect(table).not_to_contain_text("Đang tải")
    
    # ========== TÌM KIẾM VÀ LỌC ==========
    
    def test_search_asset_by_name(self, admin_page):
        """TC-ASSET-02: Tìm kiếm tài sản theo tên"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(500)
        
        # Nhập từ khóa tìm kiếm
        admin_page.fill('#searchAssets', "Bàn")
        admin_page.wait_for_timeout(1000)
        
        # Kiểm tra kết quả hiển thị
        rows = admin_page.locator('#assetsTableBody tr')
        expect(rows.first).to_contain_text("Bàn")
    
    def test_search_asset_empty(self, admin_page):
        """TC-ASSET-02b: Tìm kiếm tài sản không có kết quả"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#searchAssets', "KHONGCOKETQUA")
        admin_page.wait_for_timeout(1000)
        
        empty_msg = admin_page.locator('#assetsTableBody')
        expect(empty_msg).to_contain_text("Không có dữ liệu")
    
    def test_filter_asset_by_status(self, admin_page):
        """TC-ASSET-03: Lọc tài sản theo trạng thái"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(500)
        
        # Chọn lọc theo trạng thái "Đang sử dụng"
        admin_page.select_option('#filterAssetStatus', "Đang sử dụng")
        admin_page.wait_for_timeout(1000)
        
        # Kiểm tra các dòng hiển thị có trạng thái đúng
        status_badges = admin_page.locator('#assetsTableBody .status-badge')
        if status_badges.count() > 0:
            expect(status_badges.first).to_contain_text("Đang sử dụng")
    
    def test_filter_device_by_status(self, admin_page):
        """TC-DEVICE-02: Lọc thiết bị theo trạng thái"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(500)
        
        admin_page.select_option('#filterDeviceStatus', "Chưa sử dụng")
        admin_page.wait_for_timeout(1000)
        
        status_badges = admin_page.locator('#devicesTableBody .status-badge')
        if status_badges.count() > 0:
            expect(status_badges.first).to_contain_text("Chưa sử dụng")
    
    def test_search_device_by_name(self, admin_page):
        """TC-DEVICE-03: Tìm kiếm thiết bị theo tên"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#searchDevices', "Laptop")
        admin_page.wait_for_timeout(1000)
        
        rows = admin_page.locator('#devicesTableBody tr')
        expect(rows.first).to_contain_text("Laptop")
    
    # ========== THÊM TÀI SẢN ==========
    
    def test_add_asset_success(self, admin_page):
        """TC-ASSET-04: Thêm tài sản mới thành công"""
        random_suffix = random.randint(1000, 9999)
        
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.click('#addAssetBtn')
        admin_page.wait_for_timeout(500)
        
        # Điền thông tin
        admin_page.fill('#assetName', f"Test Asset {random_suffix}")
        admin_page.select_option('#assetGroup', "Nội thất")
        admin_page.select_option('#assetType', "Hữu hình")
        admin_page.select_option('#assetStatus', "Chưa sử dụng")
        admin_page.fill('#assetAssignedTo', "Phòng Test")
        
        # Xử lý dialog
        def handle_dialog(dialog):
            assert "Thêm thành công" in dialog.message or "thành công" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveAssetBtn')
        admin_page.wait_for_timeout(1500)
    
    def test_add_asset_missing_name(self, admin_page):
        """TC-ASSET-05: Thêm tài sản thiếu tên - Hiển thị lỗi"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.click('#addAssetBtn')
        admin_page.wait_for_timeout(500)
        
        # Để trống tên
        admin_page.fill('#assetName', "")
        admin_page.fill('#assetAssignedTo', "Phòng Test")
        
        def handle_dialog(dialog):
            assert "Vui lòng nhập" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveAssetBtn')
        admin_page.wait_for_timeout(1000)
    
    # ========== SỬA TÀI SẢN ==========
    
    def test_edit_asset(self, admin_page):
        """TC-ASSET-06: Sửa tài sản thành công"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(1000)
        
        # Click nút sửa đầu tiên
        edit_btn = admin_page.locator('#assetsTableBody .btn-edit').first
        if edit_btn.count() > 0:
            edit_btn.click()
            admin_page.wait_for_timeout(500)
            
            # Sửa tên
            new_name = f"Edited Asset {random.randint(1000, 9999)}"
            admin_page.fill('#assetName', new_name)
            
            def handle_dialog(dialog):
                assert "Cập nhật thành công" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_dialog)
            admin_page.click('#saveAssetBtn')
            admin_page.wait_for_timeout(1500)
    
    # ========== XÓA TÀI SẢN ==========
    
    def test_delete_asset(self, admin_page):
        """TC-ASSET-07: Xóa tài sản thành công"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(1000)
        
        # Click nút xóa đầu tiên
        delete_btn = admin_page.locator('#assetsTableBody .btn-delete').first
        if delete_btn.count() > 0:
            def handle_confirm(dialog):
                dialog.accept()
            
            admin_page.on("dialog", handle_confirm)
            delete_btn.click()
            admin_page.wait_for_timeout(1000)
            
            # Kiểm tra dialog xác nhận xóa
            def handle_alert(dialog):
                assert "Xóa thành công" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_alert)
            admin_page.wait_for_timeout(1000)
    
    # ========== THÊM THIẾT BỊ ==========
    
    def test_add_device_success(self, admin_page):
        """TC-DEVICE-04: Thêm thiết bị mới thành công"""
        random_suffix = random.randint(1000, 9999)
        
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.click('#addDeviceBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#deviceName', f"Test Device {random_suffix}")
        admin_page.select_option('#deviceGroup', "Laptop")
        admin_page.select_option('#deviceType', "Phần cứng")
        admin_page.select_option('#deviceStatus', "Chưa sử dụng")
        admin_page.fill('#deviceAssignedTo', "Test User")
        
        def handle_dialog(dialog):
            assert "Thêm thành công" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveDeviceBtn')
        admin_page.wait_for_timeout(1500)
    
    def test_add_device_missing_name(self, admin_page):
        """TC-DEVICE-05: Thêm thiết bị thiếu tên"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.click('#addDeviceBtn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#deviceName', "")
        
        def handle_dialog(dialog):
            assert "Vui lòng nhập" in dialog.message
            dialog.accept()
        
        admin_page.on("dialog", handle_dialog)
        admin_page.click('#saveDeviceBtn')
        admin_page.wait_for_timeout(1000)
    
    # ========== SỬA THIẾT BỊ ==========
    
    def test_edit_device(self, admin_page):
        """TC-DEVICE-06: Sửa thiết bị thành công"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(1000)
        
        edit_btn = admin_page.locator('#devicesTableBody .btn-edit').first
        if edit_btn.count() > 0:
            edit_btn.click()
            admin_page.wait_for_timeout(500)
            
            new_name = f"Edited Device {random.randint(1000, 9999)}"
            admin_page.fill('#deviceName', new_name)
            
            def handle_dialog(dialog):
                assert "Cập nhật thành công" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_dialog)
            admin_page.click('#saveDeviceBtn')
            admin_page.wait_for_timeout(1500)
    
    # ========== XÓA THIẾT BỊ ==========
    
    def test_delete_device(self, admin_page):
        """TC-DEVICE-07: Xóa thiết bị thành công"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(1000)
        
        delete_btn = admin_page.locator('#devicesTableBody .btn-delete').first
        if delete_btn.count() > 0:
            def handle_confirm(dialog):
                dialog.accept()
            
            admin_page.on("dialog", handle_confirm)
            delete_btn.click()
            admin_page.wait_for_timeout(1000)
            
            def handle_alert(dialog):
                assert "Xóa thành công" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_alert)
            admin_page.wait_for_timeout(1000)
    
    # ========== CHUYỂN TAB ==========
    
    def test_switch_tab_assets_to_devices(self, admin_page):
        """TC-TAB-01: Chuyển từ tab Tài sản sang tab Thiết bị"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabAssets')
        admin_page.wait_for_timeout(500)
        
        # Kiểm tra panel tài sản hiển thị
        assets_panel = admin_page.locator('#assetsPanel')
        expect(assets_panel).to_be_visible()
        
        # Chuyển sang tab thiết bị
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(500)
        
        devices_panel = admin_page.locator('#devicesPanel')
        expect(devices_panel).to_be_visible()
        expect(assets_panel).not_to_be_visible()
    
    def test_switch_tab_devices_to_return(self, admin_page):
        """TC-TAB-02: Chuyển từ tab Thiết bị sang tab Hoàn trả"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabDevices')
        admin_page.wait_for_timeout(500)
        
        devices_panel = admin_page.locator('#devicesPanel')
        expect(devices_panel).to_be_visible()
        
        admin_page.click('#tabReturn')
        admin_page.wait_for_timeout(500)
        
        return_panel = admin_page.locator('#returnPanel')
        expect(return_panel).to_be_visible()
        expect(devices_panel).not_to_be_visible()
    
    # ========== LÀM MỚI DỮ LIỆU ==========
    
    def test_refresh_return_list(self, admin_page):
        """TC-RETURN-02: Làm mới danh sách hoàn trả"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabReturn')
        admin_page.wait_for_timeout(500)
        
        refresh_btn = admin_page.locator('#refreshReturnBtn')
        refresh_btn.click()
        admin_page.wait_for_timeout(1000)
        
        table = admin_page.locator('#returnTableBody')
        expect(table).to_be_visible()
    
    # ========== LỌC DANH SÁCH HOÀN TRẢ ==========
    
    def test_filter_return_by_status_overdue(self, admin_page):
        """TC-RETURN-03: Lọc danh sách hoàn trả theo trạng thái Quá hạn"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabReturn')
        admin_page.wait_for_timeout(500)
        
        admin_page.select_option('#filterReturnStatus', "quahan")
        admin_page.wait_for_timeout(1000)
        
        table = admin_page.locator('#returnTableBody')
        expect(table).to_be_visible()
    
    def test_filter_return_by_status_nearing(self, admin_page):
        """TC-RETURN-04: Lọc danh sách hoàn trả theo trạng thái Sắp đến hạn"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabReturn')
        admin_page.wait_for_timeout(500)
        
        admin_page.select_option('#filterReturnStatus', "sapdenhan")
        admin_page.wait_for_timeout(1000)
        
        table = admin_page.locator('#returnTableBody')
        expect(table).to_be_visible()
    
    # ========== TÌM KIẾM DANH SÁCH HOÀN TRẢ ==========
    
    def test_search_return_by_name(self, admin_page):
        """TC-RETURN-05: Tìm kiếm trong danh sách hoàn trả"""
        admin_page.goto("http://localhost:5000/admin/assets-devices")
        admin_page.click('#tabReturn')
        admin_page.wait_for_timeout(500)
        
        admin_page.fill('#searchReturn', "Laptop")
        admin_page.wait_for_timeout(1000)
        
        rows = admin_page.locator('#returnTableBody tr')
        if rows.count() > 0:
            expect(rows.first).to_contain_text("Laptop")