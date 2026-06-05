import pytest
import time
import random
from playwright.sync_api import expect

class TestAdminBorrowRequests:
    
    # ========== FUNCTIONAL TESTS (10 tests) ==========
    
    def test_func_01_view_borrow_requests_page(self, admin_page):
        """Xem trang xử lý yêu cầu mượn"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(1000)
        
        requests_list = admin_page.locator('#requestsList')
        expect(requests_list).to_be_visible()
        expect(requests_list).not_to_contain_text("Đang tải")
    
    def test_func_02_view_pending_requests(self, admin_page):
        """Xem danh sách yêu cầu đang chờ"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(1000)
        
        # Lọc theo trạng thái
        admin_page.select_option('#statusFilter', "Chờ xét duyệt")
        admin_page.wait_for_timeout(500)
        
        requests_list = admin_page.locator('#requestsList')
        expect(requests_list).to_be_visible()
    
    def test_func_03_search_borrow_request(self, admin_page):
        """Tìm kiếm yêu cầu mượn"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.fill('#searchRequest', "máy in")
        admin_page.wait_for_timeout(500)
        
        requests_list = admin_page.locator('#requestsList')
        expect(requests_list).to_be_visible()
    
    def test_func_04_view_request_detail(self, admin_page):
        """Xem chi tiết yêu cầu mượn"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(1000)
        
        view_btn = admin_page.locator('.btn-view').first
        if view_btn.count() > 0:
            view_btn.click()
            admin_page.wait_for_timeout(500)
            
            # Kiểm tra modal hiển thị
            modal = admin_page.locator('#viewRequestModal')
            expect(modal).to_be_visible()
            
            # Đóng modal
            admin_page.click('#closeViewModal')
            admin_page.wait_for_timeout(500)
            expect(modal).not_to_be_visible()
    
    def test_func_05_approve_borrow_request(self, admin_page):
        """Duyệt yêu cầu mượn"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(1000)
        
        # Lọc để chỉ thấy yêu cầu chờ duyệt
        admin_page.select_option('#statusFilter', "Chờ xét duyệt")
        admin_page.wait_for_timeout(500)
        
        approve_btn = admin_page.locator('.btn-approve').first
        if approve_btn.count() > 0:
            approve_btn.click()
            admin_page.wait_for_timeout(500)
            
            # Chọn ngày bàn giao
            admin_page.fill('#handoverDate', "2024-12-31")
            
            def handle_dialog(dialog):
                assert "duyệt" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_dialog)
            admin_page.click('#confirmApproveBtn')
            admin_page.wait_for_timeout(1500)
    
    def test_func_06_reject_borrow_request(self, admin_page):
        """Từ chối yêu cầu mượn"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(1000)
        
        admin_page.select_option('#statusFilter', "Chờ xét duyệt")
        admin_page.wait_for_timeout(500)
        
        reject_btn = admin_page.locator('.btn-reject').first
        if reject_btn.count() > 0:
            reject_btn.click()
            admin_page.wait_for_timeout(500)
            
            admin_page.fill('#rejectReason', "Tài sản đã được bàn giao cho người khác")
            
            def handle_dialog(dialog):
                assert "từ chối" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_dialog)
            admin_page.click('#confirmRejectBtn')
            admin_page.wait_for_timeout(1500)
    
    def test_func_07_filter_by_status_approved(self, admin_page):
        """Lọc yêu cầu đã duyệt"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.select_option('#statusFilter', "Đã duyệt")
        admin_page.wait_for_timeout(500)
        
        requests_list = admin_page.locator('#requestsList')
        expect(requests_list).to_be_visible()
    
    def test_func_08_filter_by_status_rejected(self, admin_page):
        """Lọc yêu cầu bị từ chối"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.select_option('#statusFilter', "Từ chối")
        admin_page.wait_for_timeout(500)
        
        requests_list = admin_page.locator('#requestsList')
        expect(requests_list).to_be_visible()
    
    def test_func_09_approve_without_handover_date(self, admin_page):
        """Duyệt yêu cầu nhưng không chọn ngày bàn giao"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(1000)
        
        admin_page.select_option('#statusFilter', "Chờ xét duyệt")
        admin_page.wait_for_timeout(500)
        
        approve_btn = admin_page.locator('.btn-approve').first
        if approve_btn.count() > 0:
            approve_btn.click()
            admin_page.wait_for_timeout(500)
            
            # Để trống ngày bàn giao
            admin_page.fill('#handoverDate', "")
            
            def handle_dialog(dialog):
                assert "ngày" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_dialog)
            admin_page.click('#confirmApproveBtn')
            admin_page.wait_for_timeout(1000)
    
    def test_func_10_reject_without_reason(self, admin_page):
        """Từ chối yêu cầu nhưng không nhập lý do"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(1000)
        
        admin_page.select_option('#statusFilter', "Chờ xét duyệt")
        admin_page.wait_for_timeout(500)
        
        reject_btn = admin_page.locator('.btn-reject').first
        if reject_btn.count() > 0:
            reject_btn.click()
            admin_page.wait_for_timeout(500)
            
            admin_page.fill('#rejectReason', "")
            
            def handle_dialog(dialog):
                assert "lý do" in dialog.message
                dialog.accept()
            
            admin_page.on("dialog", handle_dialog)
            admin_page.click('#confirmRejectBtn')
            admin_page.wait_for_timeout(1000)
    
    # ========== PERFORMANCE TESTS (5 tests) ==========
    
    def test_perf_01_borrow_requests_load_time(self, admin_page):
        """Thời gian tải trang yêu cầu mượn < 3s"""
        start = time.time()
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"Tải trang: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_02_search_borrow_performance(self, admin_page):
        """Tìm kiếm yêu cầu mượn < 1s"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        start = time.time()
        admin_page.fill('#searchRequest', "máy in")
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Tìm kiếm: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_03_filter_performance(self, admin_page):
        """Lọc yêu cầu mượn < 1s"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        start = time.time()
        admin_page.select_option('#statusFilter', "Đã duyệt")
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"Lọc: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_04_approve_performance(self, admin_page):
        """Thời gian duyệt yêu cầu < 2s"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(500)
        
        admin_page.select_option('#statusFilter', "Chờ xét duyệt")
        admin_page.wait_for_timeout(500)
        
        approve_btn = admin_page.locator('.btn-approve').first
        if approve_btn.count() > 0:
            approve_btn.click()
            admin_page.wait_for_timeout(500)
            admin_page.fill('#handoverDate', "2024-12-31")
            
            start = time.time()
            admin_page.click('#confirmApproveBtn')
            admin_page.wait_for_timeout(1000)
            elapsed = (time.time() - start) * 1000
            print(f"Duyệt: {elapsed:.0f}ms")
            assert elapsed < 2000
    
    def test_perf_05_reject_performance(self, admin_page):
        """Thời gian từ chối yêu cầu < 2s"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(500)
        
        admin_page.select_option('#statusFilter', "Chờ xét duyệt")
        admin_page.wait_for_timeout(500)
        
        reject_btn = admin_page.locator('.btn-reject').first
        if reject_btn.count() > 0:
            reject_btn.click()
            admin_page.wait_for_timeout(500)
            admin_page.fill('#rejectReason', "Test reason")
            
            start = time.time()
            admin_page.click('#confirmRejectBtn')
            admin_page.wait_for_timeout(1000)
            elapsed = (time.time() - start) * 1000
            print(f"Từ chối: {elapsed:.0f}ms")
            assert elapsed < 2000
    
    # ========== SECURITY TESTS (5 tests) ==========
    
    def test_sec_01_unauthorized_borrow_access(self, page):
        """Nhân viên không thể xử lý yêu cầu mượn"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.uncheck('input[name="is_admin"]')
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        
        page.goto("http://localhost:5000/admin/borrow-requests")
        assert "admin" not in page.url
        assert "login" in page.url or page.url == "http://localhost:5000/"
    
    def test_sec_02_xss_in_borrow_reason(self, admin_page):
        """XSS trong lý do yêu cầu mượn"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(500)
        
        # Tìm yêu cầu có nội dung XSS nếu có
        page_content = admin_page.content()
        assert "alert" not in page_content
    
    def test_sec_03_approve_already_processed_request(self, admin_page):
        """Duyệt yêu cầu đã được xử lý"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.select_option('#statusFilter', "Đã duyệt")
        admin_page.wait_for_timeout(500)
        
        # Không còn nút duyệt cho yêu cầu đã duyệt
        approve_btns = admin_page.locator('.btn-approve')
        assert approve_btns.count() == 0
    
    def test_sec_04_borrow_request_injection(self, admin_page):
        """SQL Injection trong tìm kiếm yêu cầu mượn"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.fill('#searchRequest', "' OR '1'='1")
        admin_page.wait_for_timeout(500)
        assert "500" not in admin_page.content()
    
    def test_sec_05_handover_date_in_past(self, admin_page):
        """Ngày bàn giao trong quá khứ"""
        admin_page.goto("http://localhost:5000/admin/borrow-requests")
        admin_page.wait_for_timeout(500)
        
        admin_page.select_option('#statusFilter', "Chờ xét duyệt")
        admin_page.wait_for_timeout(500)
        
        approve_btn = admin_page.locator('.btn-approve').first
        if approve_btn.count() > 0:
            approve_btn.click()
            admin_page.wait_for_timeout(500)
            
            # Nhập ngày trong quá khứ
            admin_page.fill('#handoverDate', "2020-01-01")
            admin_page.click('#confirmApproveBtn')
            admin_page.wait_for_timeout(1000)
            # Hệ thống có thể chấp nhận hoặc báo lỗi
            assert "500" not in admin_page.content()