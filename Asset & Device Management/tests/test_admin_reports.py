import pytest
import time
import random
from playwright.sync_api import expect

class TestAdminReports:
   
    # =================================================================
    # 1. PERFORMANCE TESTS (5 tests)
    # =================================================================
    
    def test_perf_01_reports_page_load_time(self, admin_page):
        """PERF: Thời gian tải trang báo cáo < 3s"""
        start = time.time()
        admin_page.goto("http://localhost:5000/admin/reports")
        admin_page.wait_for_timeout(1000)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tải trang báo cáo: {elapsed:.0f}ms")
        assert elapsed < 3000
    
    def test_perf_02_search_performance(self, admin_page):
        """PERF: Thời gian tìm kiếm báo cáo < 1s"""
        admin_page.goto("http://localhost:5000/admin/reports")
        start = time.time()
        admin_page.fill('#searchReport', "hỏng")
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Tìm kiếm báo cáo: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_03_filter_performance(self, admin_page):
        """PERF: Thời gian lọc báo cáo < 1s"""
        admin_page.goto("http://localhost:5000/admin/reports")
        start = time.time()
        admin_page.select_option('#statusFilter', "Chờ xử lý")
        admin_page.wait_for_timeout(500)
        elapsed = (time.time() - start) * 1000
        print(f"[PERF] Lọc báo cáo: {elapsed:.0f}ms")
        assert elapsed < 1000
    
    def test_perf_04_view_detail_performance(self, admin_page):
        """PERF: Thời gian xem chi tiết < 1s"""
        admin_page.goto("http://localhost:5000/admin/reports")
        admin_page.wait_for_timeout(500)
        view_btn = admin_page.locator('.btn-view').first
        if view_btn.count() > 0:
            start = time.time()
            view_btn.click()
            admin_page.wait_for_timeout(500)
            elapsed = (time.time() - start) * 1000
            print(f"[PERF] Xem chi tiết: {elapsed:.0f}ms")
            assert elapsed < 1000
            admin_page.click('#closeViewModal')
    
    def test_perf_05_process_report_performance(self, admin_page):
        """PERF: Thời gian xử lý báo cáo < 2s"""
        admin_page.goto("http://localhost:5000/admin/reports")
        admin_page.wait_for_timeout(500)
        process_btn = admin_page.locator('.btn-processing').first
        if process_btn.count() > 0:
            process_btn.click()
            admin_page.wait_for_timeout(500)
            start = time.time()
            admin_page.click('#confirmProcessBtn')
            admin_page.wait_for_timeout(1000)
            elapsed = (time.time() - start) * 1000
            print(f"[PERF] Xử lý báo cáo: {elapsed:.0f}ms")
            assert elapsed < 2000
    
    # =================================================================
    # 2. SECURITY TESTS (5 tests)
    # =================================================================
    
    def test_sec_01_unauthorized_access(self, page):
        """SEC: Nhân viên không thể truy cập trang xử lý báo cáo"""
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', "employee1")
        page.fill('input[name="password"]', "123456")
        page.uncheck('input[name="is_admin"]')
        page.click('button[type="submit"]')
        page.wait_for_url("http://localhost:5000/")
        
        page.goto("http://localhost:5000/admin/reports")
        assert "admin" not in page.url
        assert "login" in page.url or page.url == "http://localhost:5000/"
    
    def test_sec_02_xss_in_search(self, admin_page):
        """SEC: XSS trong ô tìm kiếm báo cáo"""
        admin_page.goto("http://localhost:5000/admin/reports")
        admin_page.fill('#searchReport', "<script>alert('XSS')</script>")
        admin_page.wait_for_timeout(500)
        assert "alert" not in admin_page.content()
    
    def test_sec_03_sql_injection_search(self, admin_page):
        """SEC: SQL Injection trong tìm kiếm báo cáo"""
        admin_page.goto("http://localhost:5000/admin/reports")
        admin_page.fill('#searchReport', "' OR '1'='1")
        admin_page.wait_for_timeout(500)
        assert "500" not in admin_page.content()
    
    def test_sec_04_html_injection(self, admin_page):
        """SEC: HTML Injection trong tìm kiếm"""
        admin_page.goto("http://localhost:5000/admin/reports")
        admin_page.fill('#searchReport', "<h1>Hacked</h1>")
        admin_page.wait_for_timeout(500)
        assert "<h1>" not in admin_page.content() or "&lt;h1&gt;" in admin_page.content()
    
    def test_sec_05_large_payload_search(self, admin_page):
        """SEC: Payload lớn trong tìm kiếm"""
        admin_page.goto("http://localhost:5000/admin/reports")
        admin_page.fill('#searchReport', "A" * 10000)
        admin_page.wait_for_timeout(500)
        assert "500" not in admin_page.content()

