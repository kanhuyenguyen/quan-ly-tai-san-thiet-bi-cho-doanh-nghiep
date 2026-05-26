from flask import Flask, render_template, request, redirect, session, jsonify
import pyodbc
import re
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "asset_device_secret_key_2025"

# Hàm kết nối SQL SERVER 
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=DESKTOP-8FQ9IH6\\SQLEXPRESS;'
            'DATABASE=AssetManagement;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print(f"Lỗi kết nối database: {e}")
        return None

# Hàm decorator kiểm tra đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        if session.get('role') != 'Admin':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

# Trang đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'Admin':
            return redirect('/admin')
        else:
            return redirect('/')
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        is_admin_login = request.form.get('is_admin') == '1'
        
        if not username or not password:
            return render_template('login.html', error="Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu")
        
        conn = get_db_connection()
        if conn is None:
            return render_template('login.html', error="Lỗi kết nối database")
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT UserID, Username, FullName, Role, Department 
            FROM Users 
            WHERE Username = ? AND PasswordHash = ?
        """, (username, password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_id = user[0]
            user_name = user[1]
            full_name = user[2]
            role = user[3]
            department = user[4] if user[4] else ""
            
            if is_admin_login and role != 'Admin':
                return render_template('login.html', error="Tài khoản này không có quyền Quản trị viên. Vui lòng bỏ tick 'Đăng nhập với tư cách Admin' hoặc dùng tài khoản Admin.", username=username)
            
            if not is_admin_login and role == 'Admin':
                return render_template('login.html', error="Tài khoản Admin cần tick chọn 'Đăng nhập với tư cách Admin' để đăng nhập.", username=username)
            
            session['user_id'] = user_id
            session['username'] = user_name
            session['user_name'] = full_name
            session['role'] = role
            session['department'] = department
            
            if role == 'Admin':
                return redirect('/admin')
            else:
                return redirect('/')
        else:
            return render_template('login.html', error="Sai tên đăng nhập hoặc mật khẩu", username=username)
    
    return render_template('login.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Các trang phía nhân viên
@app.route('/')
@login_required
def index():
    if session.get('role') == 'Admin':
        return redirect('/admin')
    return render_template('User/index.html', 
                          user_name=session.get('user_name'), 
                          department=session.get('department'), 
                          user_id=session.get('user_id'))

@app.route('/user/assets')
@login_required
def assets():
    if session.get('role') == 'Admin':
        return redirect('/admin')
    return render_template('User/assets.html', 
                          user_name=session.get('user_name'), 
                          department=session.get('department'), 
                          user_id=session.get('user_id'))

@app.route('/user/devices')
@login_required
def devices():
    if session.get('role') == 'Admin':
        return redirect('/admin')
    return render_template('User/devices.html', 
                          user_name=session.get('user_name'), 
                          department=session.get('department'), 
                          user_id=session.get('user_id'))

@app.route('/user/report-assets')
@login_required
def report_assets():
    if session.get('role') == 'Admin':
        return redirect('/admin')
    return render_template('User/report_assets.html', 
                          user_name=session.get('user_name'), 
                          department=session.get('department'), 
                          user_id=session.get('user_id'))

@app.route('/user/report-devices')
@login_required
def report_devices():
    if session.get('role') == 'Admin':
        return redirect('/admin')
    return render_template('User/report_devices.html', 
                          user_name=session.get('user_name'), 
                          department=session.get('department'), 
                          user_id=session.get('user_id'))

@app.route('/user/borrow')
@login_required
def borrow():
    if session.get('role') == 'Admin':
        return redirect('/admin')
    return render_template('User/borrow.html', 
                          user_name=session.get('user_name'), 
                          department=session.get('department'), 
                          user_id=session.get('user_id'))

@app.route('/user/track')
@login_required
def track():
    if session.get('role') == 'Admin':
        return redirect('/admin')
    return render_template('User/track.html', 
                          user_name=session.get('user_name'), 
                          department=session.get('department'), 
                          user_id=session.get('user_id'))

# Các trang phía admin
@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('Admin/dashboard.html', 
                          user_name=session.get('user_name'), 
                          role=session.get('role'))

@app.route('/admin/assets-devices')
@admin_required
def admin_assets_devices():
    return render_template('Admin/assets_devices.html', 
                          user_name=session.get('user_name'), 
                          role=session.get('role'))

@app.route('/admin/assign')
@admin_required
def admin_assign():
    return render_template('Admin/assign.html', 
                          user_name=session.get('user_name'), 
                          role=session.get('role'))

@app.route('/admin/reports')
@admin_required
def admin_reports():
    return render_template('Admin/reports.html', 
                          user_name=session.get('user_name'), 
                          role=session.get('role'))

@app.route('/admin/borrow-requests')
@admin_required
def admin_borrow_requests():
    return render_template('Admin/borrow_requests.html', 
                          user_name=session.get('user_name'), 
                          role=session.get('role'))

@app.route('/admin/users')
@admin_required
def admin_users():
    return render_template('Admin/users.html', 
                          user_name=session.get('user_name'), 
                          role=session.get('role'))

# Sử lý dữ liệu
# API lấy tất cả tài sản
@app.route('/api/assets')
def get_assets():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Không thể kết nối database'}), 500
    
    cursor = conn.cursor()
    assets = []
    cursor.execute("""
        SELECT AssetID, AssetName, AssetType, Status, AssignedTo, 
               FORMAT(CreatedDate, 'dd/MM/yyyy') as CreatedDate 
        FROM Assets
    """)
    for row in cursor.fetchall():
        assets.append({
            'id': row[0],
            'code': f"AST{row[0]:03d}",
            'name': row[1],
            'type': row[2],
            'status': row[3],
            'assignedTo': row[4] if row[4] else "---",
            'createdDate': row[5] if row[5] else "---"
        })
    conn.close()
    return jsonify(assets)

# API lấy tài sản đang sử dụng
@app.route('/api/assets/in-use')
def get_assets_in_use():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Không thể kết nối database'}), 500
    
    cursor = conn.cursor()
    assets = []
    cursor.execute("""
        SELECT AssetID, AssetName, AssetType, Status, AssignedTo, 
               FORMAT(CreatedDate, 'dd/MM/yyyy') as CreatedDate 
        FROM Assets
        WHERE Status = N'Đang sử dụng'
    """)
    for row in cursor.fetchall():
        assets.append({
            'id': row[0],
            'code': f"AST{row[0]:03d}",
            'name': row[1],
            'type': row[2],
            'status': row[3],
            'assignedTo': row[4] if row[4] else "---",
            'createdDate': row[5] if row[5] else "---"
        })
    conn.close()
    return jsonify(assets)

# API lấy tất cả các thiết bị
@app.route('/api/devices')
def get_devices():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Không thể kết nối database'}), 500
    
    cursor = conn.cursor()
    devices = []
    cursor.execute("""
        SELECT DeviceID, DeviceName, DeviceType, Status, AssignedTo, 
               FORMAT(AssignedDate, 'dd/MM/yyyy') as AssignedDate,
               FORMAT(CreatedDate, 'dd/MM/yyyy') as CreatedDate
        FROM Devices
    """)
    for row in cursor.fetchall():
        devices.append({
            'id': row[0],
            'code': f"DEV{row[0]:03d}",
            'name': row[1],
            'type': row[2],
            'status': row[3],
            'assignedTo': row[4] if row[4] else "---",
            'assignedDate': row[5] if row[5] else "---",
            'createdDate': row[6] if row[6] else "---"
        })
    conn.close()
    return jsonify(devices)

# API lấy thiết bị đang sử dụng
@app.route('/api/devices/in-use')
def get_devices_in_use():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Không thể kết nối database'}), 500
    
    cursor = conn.cursor()
    devices = []
    cursor.execute("""
        SELECT DeviceID, DeviceName, DeviceType, Status, AssignedTo, 
               FORMAT(AssignedDate, 'dd/MM/yyyy') as AssignedDate,
               FORMAT(CreatedDate, 'dd/MM/yyyy') as CreatedDate
        FROM Devices
        WHERE Status = N'Đang sử dụng'
    """)
    for row in cursor.fetchall():
        devices.append({
            'id': row[0],
            'code': f"DEV{row[0]:03d}",
            'name': row[1],
            'type': row[2],
            'status': row[3],
            'assignedTo': row[4] if row[4] else "---",
            'assignedDate': row[5] if row[5] else "---",
            'createdDate': row[6] if row[6] else "---"
        })
    conn.close()
    return jsonify(devices)

# API lấy tài sản chưa sử dụng
@app.route('/api/assets/available')
def get_available_assets():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Không thể kết nối database'}), 500
    
    cursor = conn.cursor()
    assets = []
    cursor.execute("""
        SELECT AssetID, AssetName, AssetType, Status, AssignedTo, 
               FORMAT(CreatedDate, 'dd/MM/yyyy') as CreatedDate 
        FROM Assets
        WHERE Status = N'Chưa sử dụng' OR AssignedTo IS NULL
    """)
    for row in cursor.fetchall():
        assets.append({
            'id': row[0],
            'code': f"AST{row[0]:03d}",
            'name': row[1],
            'type': row[2],
            'status': row[3],
            'assignedTo': row[4] if row[4] else "---",
            'createdDate': row[5] if row[5] else "---"
        })
    conn.close()
    return jsonify(assets)

# API báo cáo tài sản
@app.route('/api/send-report-asset', methods=['POST'])
def send_report_asset():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    data = request.get_json()
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    asset_name = data.get('asset_name', '')
    report_type = data.get('report_type', '')
    description = data.get('description', '')
    
    if not description:
        return jsonify({'error': 'Vui lòng nhập mô tả'}), 400
    
    report_types = {
        'broken': 'Báo hỏng',
        'repair': 'Cần sửa chữa',
        'replace': 'Cần thay thế'
    }
    
    type_text = report_types.get(report_type, 'Báo cáo')
    full_content = f"[TÀI SẢN - {asset_name}] [{type_text}] {description}"
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Lỗi database'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Reports (UserID, ReportContent, Status, CreatedAt)
            VALUES (?, ?, N'Chờ xử lý', GETDATE())
        """, (user_id, full_content))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Báo cáo đã được gửi'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# API báo cáo thiết bị
@app.route('/api/send-report-device', methods=['POST'])
def send_report_device():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    data = request.get_json()
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    device_name = data.get('device_name', '')
    report_type = data.get('report_type', '')
    description = data.get('description', '')
    
    if not description:
        return jsonify({'error': 'Vui lòng nhập mô tả'}), 400
    
    report_types = {
        'broken': 'Báo hỏng cần sửa',
        'maintenance': 'Cần bảo trì',
        'tech_support': 'Yêu cầu hỗ trợ kỹ thuật',
        'error': 'Báo lỗi thiết bị'
    }
    
    type_text = report_types.get(report_type, 'Báo cáo')
    full_content = f"[THIẾT BỊ - {device_name}] [{type_text}] {description}"
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Lỗi database'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Reports (UserID, ReportContent, Status, CreatedAt)
            VALUES (?, ?, N'Chờ xử lý', GETDATE())
        """, (user_id, full_content))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Báo cáo đã được gửi'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# API yêu cầu mượn
@app.route('/api/send-borrow-request', methods=['POST'])
def send_borrow_request():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    data = request.get_json()
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    department = session.get('department')
    asset_name = data.get('asset_name', '')
    reason = data.get('reason', '')
    borrow_date = data.get('borrow_date', '')
    return_date = data.get('return_date', '')
    
    if not reason:
        return jsonify({'error': 'Vui lòng nhập lý do mượn'}), 400
    
    full_content = f"[YÊU CẦU MƯỢN - {asset_name}] Người mượn: {user_name} - {department} | Lý do: {reason} | Dự kiến mượn: {borrow_date} | Dự kiến trả: {return_date}"
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Lỗi database'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Reports (UserID, ReportContent, Status, CreatedAt)
            VALUES (?, ?, N'Chờ xét duyệt', GETDATE())
        """, (user_id, full_content))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Yêu cầu mượn đã được gửi'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# API lấy báo cáo của nhân viên
@app.route('/api/my-reports')
def get_my_reports():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    user_id = session.get('user_id')
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Không thể kết nối database'}), 500
    
    cursor = conn.cursor()
    reports = []
    cursor.execute("""
        SELECT ReportID, ReportContent, Status, FORMAT(CreatedAt, 'dd/MM/yyyy HH:mm') as CreatedAt
        FROM Reports
        WHERE UserID = ?
        ORDER BY CreatedAt DESC
    """, (user_id,))
    
    for row in cursor.fetchall():
        content = row[1]
        report_type = "Khác"
        if "[TÀI SẢN]" in content:
            report_type = "Báo cáo tài sản"
        elif "[THIẾT BỊ]" in content:
            report_type = "Báo cáo thiết bị"
        elif "[YÊU CẦU MƯỢN" in content:
            report_type = "Yêu cầu mượn"
        
        reports.append({
            'id': row[0],
            'content': content,
            'type': report_type,
            'status': row[2],
            'createdAt': row[3]
        })
    
    conn.close()
    return jsonify(reports)

# API lấy yêu cầu mượn của nhân viên
@app.route('/api/my-borrow-requests')
def get_my_borrow_requests():
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    user_id = session.get('user_id')
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Không thể kết nối database'}), 500
    
    cursor = conn.cursor()
    requests = []
    cursor.execute("""
        SELECT ReportID, ReportContent, Status, FORMAT(CreatedAt, 'dd/MM/yyyy HH:mm') as CreatedAt
        FROM Reports
        WHERE UserID = ? AND ReportContent LIKE N'%YÊU CẦU MƯỢN%'
        ORDER BY CreatedAt DESC
    """, (user_id,))
    
    for row in cursor.fetchall():
        content = row[1]
        asset_name = "Tài sản"
        match = re.search(r'YÊU CẦU MƯỢN - (.*?)\]', content)
        if match:
            asset_name = match.group(1)
        
        expected_handover = "---"
        if row[2] == "Đã duyệt":
            try:
                created_date = datetime.strptime(row[3], '%d/%m/%Y %H:%M')
                handover_date = created_date + timedelta(days=3)
                expected_handover = handover_date.strftime('%d/%m/%Y')
            except:
                expected_handover = "---"
        
        requests.append({
            'id': row[0],
            'asset_name': asset_name,
            'content': content,
            'status': row[2],
            'createdAt': row[3],
            'expected_handover': expected_handover
        })
    
    conn.close()
    return jsonify(requests)

# Xử lý chức năng phía admin
# Hàm kiểm tra admin
def is_admin():
    if 'user_id' not in session:
        return False
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    cursor.execute("SELECT Role FROM Users WHERE UserID = ?", (session['user_id'],))
    row = cursor.fetchone()
    conn.close()
    return row and row[0] == 'Admin'
# API admin
@app.route('/api/admin/assets')
def admin_get_assets():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    assets = []
    cursor.execute("SELECT AssetID, AssetName, AssetType, Status, AssignedTo, FORMAT(CreatedDate, 'dd/MM/yyyy') FROM Assets")
    for row in cursor.fetchall():
        assets.append({
            'id': row[0], 
            'code': f"AST{row[0]:03d}", 
            'name': row[1], 
            'type': row[2], 
            'status': row[3], 
            'assignedTo': row[4] or '---', 
            'createdDate': row[5]
        })
    conn.close()
    return jsonify(assets)

@app.route('/api/admin/devices')
def admin_get_devices():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    devices = []
    cursor.execute("SELECT DeviceID, DeviceName, DeviceType, Status, AssignedTo, FORMAT(AssignedDate, 'dd/MM/yyyy') FROM Devices")
    for row in cursor.fetchall():
        devices.append({
            'id': row[0], 
            'code': f"DEV{row[0]:03d}", 
            'name': row[1], 
            'type': row[2], 
            'status': row[3], 
            'assignedTo': row[4] or '---', 
            'assignedDate': row[5] or '---'
        })
    conn.close()
    return jsonify(devices)

@app.route('/api/admin/reports/pending')
def admin_get_pending_reports():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    reports = []
    cursor.execute("""
        SELECT ReportID, ReportContent, Status, FORMAT(CreatedAt, 'dd/MM/yyyy HH:mm') 
        FROM Reports 
        WHERE Status IN (N'Chờ xử lý', N'Chưa xử lý', N'Chờ xét duyệt')
        ORDER BY CreatedAt DESC
    """)
    for row in cursor.fetchall():
        reports.append({
            'id': row[0], 
            'content': row[1], 
            'status': row[2], 
            'createdAt': row[3]
        })
    conn.close()
    return jsonify(reports)

@app.route('/api/admin/borrow-requests/pending')
def admin_get_pending_borrow():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    requests = []
    cursor.execute("""
        SELECT ReportID, ReportContent, Status, FORMAT(CreatedAt, 'dd/MM/yyyy HH:mm') 
        FROM Reports 
        WHERE ReportContent LIKE '%YÊU CẦU MƯỢN%' AND Status = N'Chờ xét duyệt' 
        ORDER BY CreatedAt DESC
    """)
    for row in cursor.fetchall():
        requests.append({
            'id': row[0], 
            'content': row[1], 
            'status': row[2], 
            'createdAt': row[3]
        })
    conn.close()
    return jsonify(requests)

# API BÀN GIAO TÀI SẢN 
@app.route('/api/admin/assets/<int:asset_id>/assign', methods=['PUT'])
def admin_assign_asset(asset_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Cập nhật tài sản: gán cho người dùng, cập nhật trạng thái
        cursor.execute("""
            UPDATE Assets 
            SET Status = N'Đang sử dụng', 
                AssignedTo = ?,
                UserID = ?
            WHERE AssetID = ?
        """, (data['userName'] + ' - ' + data['department'], data['userId'], asset_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# API BÀN GIAO THIẾT BỊ
@app.route('/api/admin/devices/<int:device_id>/assign', methods=['PUT'])
def admin_assign_device(device_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE Devices 
            SET Status = N'Đang sử dụng', 
                AssignedTo = ?,
                UserID = ?,
                AssignedDate = ?
            WHERE DeviceID = ?
        """, (data['userName'], data['userId'], data['assignDate'], device_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# API LẤY DANH SÁCH NGƯỜI DÙNG CHO ADMIN
# Lấy danh sách người dùng
@app.route('/api/admin/users')
def admin_get_users():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    users = []
    cursor.execute("SELECT UserID, Username, FullName, Role, Department FROM Users ORDER BY UserID")
    for row in cursor.fetchall():
        users.append({
            'id': row[0],
            'username': row[1],
            'fullname': row[2],
            'role': row[3],
            'department': row[4] or ''
        })
    conn.close()
    return jsonify(users)

# Thêm người dùng mới
@app.route('/api/admin/users', methods=['POST'])
def admin_create_user():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Kiểm tra username đã tồn tại chưa
        cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = ?", (data['username'],))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return jsonify({'error': 'Tên đăng nhập đã tồn tại'}), 400
        
        # Thêm mới
        cursor.execute("""
            INSERT INTO Users (Username, PasswordHash, FullName, Role, Department, CreatedAt)
            VALUES (?, ?, ?, ?, ?, GETDATE())
        """, (data['username'], data['password'], data['fullname'], data['role'], data.get('department', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Cập nhật người dùng
@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def admin_update_user(user_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Kiểm tra username đã tồn tại (trừ chính nó)
        cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = ? AND UserID != ?", (data['username'], user_id))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return jsonify({'error': 'Tên đăng nhập đã tồn tại'}), 400
        
        # Cập nhật (nếu có mật khẩu mới thì update, không thì giữ nguyên)
        if data.get('password'):
            cursor.execute("""
                UPDATE Users 
                SET Username=?, PasswordHash=?, FullName=?, Role=?, Department=?
                WHERE UserID=?
            """, (data['username'], data['password'], data['fullname'], data['role'], data.get('department', ''), user_id))
        else:
            cursor.execute("""
                UPDATE Users 
                SET Username=?, FullName=?, Role=?, Department=?
                WHERE UserID=?
            """, (data['username'], data['fullname'], data['role'], data.get('department', ''), user_id))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Xóa người dùng
@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Không cho xóa chính mình
    if user_id == session.get('user_id'):
        return jsonify({'error': 'Không thể xóa tài khoản đang đăng nhập'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Kiểm tra xem user có đang sử dụng tài sản không
        cursor.execute("SELECT COUNT(*) FROM Assets WHERE UserID = ?", (user_id,))
        asset_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Devices WHERE UserID = ?", (user_id,))
        device_count = cursor.fetchone()[0]
        
        if asset_count > 0 or device_count > 0:
            conn.close()
            return jsonify({'error': f'Người dùng đang quản lý {asset_count} tài sản và {device_count} thiết bị. Không thể xóa.'}), 400
        
        cursor.execute("DELETE FROM Users WHERE UserID=?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
    
# ========== API LẤY DANH SÁCH CẦN HOÀN TRẢ ==========
@app.route('/api/admin/return-items')
def admin_get_return_items():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    items = []
    
    # Lấy thiết bị đang sử dụng có ngày dự kiến hoàn trả
    cursor.execute("""
        SELECT DeviceID, DeviceName, DeviceType, Status, AssignedTo, 
               FORMAT(AssignedDate, 'dd/MM/yyyy') as AssignedDate,
               FORMAT(ReturnDate, 'dd/MM/yyyy') as ReturnDate
        FROM Devices
        WHERE Status = N'Đang sử dụng'
        ORDER BY ReturnDate ASC
    """)
    for row in cursor.fetchall():
        items.append({
            'id': row[0],
            'code': f"DEV{row[0]:03d}",
            'name': row[1],
            'type': 'device',
            'assignedTo': row[4] or '---',
            'assignDate': row[5],
            'returnDate': row[6]
        })
    
    conn.close()
    return jsonify(items)

# ========== API XÁC NHẬN HOÀN TRẢ THIẾT BỊ ==========
@app.route('/api/admin/devices/<int:device_id>/return', methods=['PUT'])
def admin_return_device(device_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Cập nhật thiết bị: chuyển về chưa sử dụng, xóa người dùng
        cursor.execute("""
            UPDATE Devices 
            SET Status = N'Chưa sử dụng', 
                AssignedTo = NULL,
                UserID = NULL,
                ActualReturnDate = ?
            WHERE DeviceID = ?
        """, (data.get('actualReturnDate'), device_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ========== API LẤY TẤT CẢ BÁO CÁO CHO ADMIN ==========
@app.route('/api/admin/reports/all')
def admin_get_all_reports():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    reports = []
    
    cursor.execute("""
        SELECT r.ReportID, r.ReportContent, r.Status, FORMAT(r.CreatedAt, 'dd/MM/yyyy HH:mm') as CreatedAt,
               u.FullName as UserName
        FROM Reports r
        LEFT JOIN Users u ON r.UserID = u.UserID
        ORDER BY r.CreatedAt DESC
    """)
    
    for row in cursor.fetchall():
        content = row[1]
        report_type = "Khác"
        if "[TÀI SẢN]" in content:
            report_type = "Báo cáo tài sản"
        elif "[THIẾT BỊ]" in content:
            report_type = "Báo cáo thiết bị"
        elif "[YÊU CẦU MƯỢN" in content:
            report_type = "Yêu cầu mượn"
        
        reports.append({
            'id': row[0],
            'content': content,
            'status': row[2],
            'createdAt': row[3],
            'userName': row[4] if row[4] else 'Nhân viên',
            'type': report_type
        })
    
    conn.close()
    return jsonify(reports)

# ========== API XỬ LÝ BÁO CÁO ==========
@app.route('/api/admin/reports/<int:report_id>/process', methods=['PUT'])
def admin_process_report(report_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    new_status = data.get('status')
    note = data.get('note', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Cập nhật trạng thái báo cáo
        cursor.execute("""
            UPDATE Reports 
            SET Status = ?, 
                ProcessedNote = ?,
                ProcessedAt = GETDATE(),
                ProcessedBy = ?
            WHERE ReportID = ?
        """, (new_status, note, session.get('user_id'), report_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ========== API LẤY TẤT CẢ YÊU CẦU MƯỢN CHO ADMIN ==========
@app.route('/api/admin/borrow-requests/all')
def admin_get_all_borrow_requests():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    requests = []
    
    try:
        # Lấy dữ liệu đơn giản trước, không format date
        cursor.execute("""
            SELECT br.RequestID, br.RequestReason, br.Status, 
                   br.RequestDate,
                   br.ExpectedBorrowDate, br.ExpectedReturnDate,
                   u.FullName, u.Department,
                   a.AssetName
            FROM BorrowRequests br
            LEFT JOIN Users u ON br.UserID = u.UserID
            LEFT JOIN Assets a ON br.AssetID = a.AssetID
            ORDER BY br.RequestDate DESC
        """)
        
        for row in cursor.fetchall():
            # Xử lý date an toàn
            borrow_date = '---'
            return_date = '---'
            request_date = '---'
            
            if row[3]:
                request_date = row[3].strftime('%d/%m/%Y %H:%M') if hasattr(row[3], 'strftime') else str(row[3])
            if row[4]:
                borrow_date = row[4].strftime('%d/%m/%Y') if hasattr(row[4], 'strftime') else str(row[4])
            if row[5]:
                return_date = row[5].strftime('%d/%m/%Y') if hasattr(row[5], 'strftime') else str(row[5])
            
            requests.append({
                'id': row[0],
                'assetName': row[8] if row[8] else 'Tai san',
                'userName': row[6] if row[6] else 'Nhan vien',
                'department': row[7] if row[7] else '',
                'reason': row[1] if row[1] else '',
                'borrowDate': borrow_date,
                'returnDate': return_date,
                'status': row[2] if row[2] else 'Chờ xét duyệt',
                'createdAt': request_date
            })
        conn.close()
        return jsonify(requests)
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e), 'details': 'Loi truy van du lieu'}), 500

# ========== API DUYỆT YÊU CẦU MƯỢN ==========
@app.route('/api/admin/borrow-requests/<int:request_id>/approve', methods=['PUT'])
def admin_approve_borrow_request(request_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE BorrowRequests 
            SET Status = N'Đã duyệt',
                ApprovedBy = ?,
                HandoverDate = ?,
                ProcessedAt = GETDATE(),
                ProcessedBy = ?,
                ProcessedNote = ?
            WHERE RequestID = ?
        """, (session.get('user_id'), data.get('handoverDate'), session.get('user_id'), data.get('note', ''), request_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ========== API TỪ CHỐI YÊU CẦU MƯỢN ==========
@app.route('/api/admin/borrow-requests/<int:request_id>/reject', methods=['PUT'])
def admin_reject_borrow_request(request_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE BorrowRequests 
            SET Status = N'Từ chối',
                ApprovedBy = ?,
                ProcessedAt = GETDATE(),
                ProcessedBy = ?,
                ProcessedNote = ?
            WHERE RequestID = ?
        """, (session.get('user_id'), session.get('user_id'), data.get('reason', ''), request_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)