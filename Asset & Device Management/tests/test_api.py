import pytest
import requests

BASE_URL = "http://localhost:5000"

class TestAPI:
    
    def setup_method(self):
        """Đăng nhập để lấy session"""
        self.session = requests.Session()
        # Đăng nhập trước khi test API
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'is_admin': '1'
        }
        response = self.session.post(f"{BASE_URL}/login", data=login_data)
        print(f"Login status: {response.status_code}")
        print(f"Login url: {response.url}")
    
    def test_get_assets_api(self):
        """API lấy danh sách tài sản"""
        response = self.session.get(f"{BASE_URL}/api/admin/assets")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_devices_api(self):
        """API lấy danh sách thiết bị"""
        response = self.session.get(f"{BASE_URL}/api/admin/devices")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_users_api(self):
        """API lấy danh sách người dùng"""
        response = self.session.get(f"{BASE_URL}/api/admin/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)