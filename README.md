# HỆ THỐNG QUẢN LÝ TÀI SẢN VÀ THIẾT BỊ

## Giới thiệu
- Hệ thống Quản lý Tài sản và Thiết bị được xây dựng nhằm hỗ trợ doanh nghiệp quản lý tài sản, thiết bị và quá trình sử dụng tài sản của nhân viên một cách hiệu quả.
- Hệ thống cho phép:
    * Quản lý thông tin tài sản và thiết bị.
    * Theo dõi tình trạng sử dụng tài sản và thiết bị.
    * Quản lý yêu cầu mượn tài sản từ nhân viên.
    * Quản lý báo cáo sự cố thiết bịtừ nhân viên.
    * Theo dõi xử lý báo cáo, yêu cầu.
    * Phân quyền người dùng theo vai trò Admin và Employee.

## Công nghệ sử dụng
### Backend
* Python
* Flask
* SQL Server (kết nối thông qua thư viện PyODBC)

### Frontend
* HTML
* CSS
* JavaScript

### Kiểm thử
* Playwright
* framework Pytest

---
## Thư viện cần cài đặt
### Thư viện chạy hệ thống

```bash
pip install flask
pip install pyodbc
```

Các thư viện được sử dụng trong hệ thống:
```python
from flask import Flask, render_template, request, redirect, session, jsonify
import pyodbc
import re
from functools import wraps
from datetime import datetime, timedelta
```

---
### Thư viện chạy kiểm thử tự động
```bash
pip install pytest
pip install playwright
```

Cài đặt trình duyệt cho Playwright:
```bash
playwright install
```

Các thư viện sử dụng trong test:
```python
import pytest
import time
import random
from playwright.sync_api import expect
```

---

## Hướng dẫn chạy hệ thống

### Chạy ứng dụng
```bash
python app.py
```
---
## Hướng dẫn chạy kiểm thử tự động
### Chạy toàn bộ test
```bash
python -m pytest tests/ -v --html=report.html --self-contained-html
```

### Chạy file test cụ thể
- Test đăng nhập
```bash
python -m pytest tests/test_login.py -v --html=report.html--self-contained-html
```

-Test Admin - Quản lý tài sản
```bash
python -m pytest tests/test_admin_assets.py -v --html=report.html--self-contained-html
```

-Test Admin - Quản lý người dùng
```bash
python -m pytest tests/test_admin_users.py -v --html=report.html--self-contained-html
```

-Test Admin - Phân bổ
```bash
python -m pytest tests/test_admin_assign.py -v --html=report.html--self-contained-html
```

-Test Admin - xử lý yêu cầu mượn
```bash
python -m pytest tests/test_admin_borrow_requests.py -v --html=report.html--self-contained-html
```

-Test Admin - xử lý yêu báo cáo
```bash
python -m pytest tests/test_admin_reports.py -v --html=report.html--self-contained-html
```

-Test employee
```bash
python -m pytest tests/test_employee.py -v --html=report.html--self-contained-html
```
- Test employee từng phần
  Tài sản:
    ```bash
    python -m pytest tests/test_employee.py -k "assets" -v --html=report.html--self-contained-html
    ```
  Thiết bị:
    ```bash
    python -m pytest tests/test_employee.py -k "devices" -v --html=report.html--self-contained-html
    ```
  Theo dõi:
    ```bash
    python -m pytest tests/test_employee.py -k "track" -v --html=report.html--self-contained-html
    ```
  Mượn:
    ```bash
    python -m pytest tests/test_employee.py -k "borrow" -v --html=report.html--self-contained-html
    ```
---
Đề tài: Xây dựng Hệ thống Quản lý Tài sản và Thiết bị
