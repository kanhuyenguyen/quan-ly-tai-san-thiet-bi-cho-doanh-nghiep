CREATE DATABASE AssetManagement;
GO

USE AssetManagement;
GO

--Bảng users
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    FullName NVARCHAR(100),
    Role NVARCHAR(20) NOT NULL CHECK (Role IN ('Admin', 'Employee')),
    Department NVARCHAR(100),
    CreatedAt DATETIME DEFAULT GETDATE()
);

INSERT INTO Users (Username, PasswordHash, FullName, Role, Department)
VALUES 
('admin', 'admin123', N'Quản trị viên', 'Admin', N'IT'),
('employee1', '123456', N'Nguyễn Văn A', 'Employee', N'Kế toán'),
('employee2', '123456', N'Trần Thị B', 'Employee', N'Nhân sự');

INSERT INTO Users (Username, PasswordHash, FullName, Role, Department)
VALUES
('employee3', '123456', N'Lê Văn C', 'Employee', N'IT'),
('employee4', '123456', N'Phạm Thị D', 'Employee', N'Marketing'),
('employee5', '123456', N'Hoàng Văn E', 'Employee', N'Kinh doanh'),
('employee6', '123456', N'Đỗ Thị F', 'Employee', N'Hành chính'),
('employee7', '123456', N'Bùi Văn G', 'Employee', N'Kho vận'),
('employee8', '123456', N'Vũ Thị H', 'Employee', N'IT'),
('employee9', '123456', N'Ngô Văn I', 'Employee', N'Nhân sự');

SELECT * FROM Users;

--Bảng tài sản
CREATE TABLE Assets (
    AssetID INT PRIMARY KEY IDENTITY(1,1),
    AssetName NVARCHAR(100) NOT NULL,
    AssetType NVARCHAR(100),
    Status NVARCHAR(50) DEFAULT N'Chưa sử dụng',
    AssignedTo NVARCHAR(100),
    UserID INT NULL,
    CreatedDate DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Assets_Users FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

INSERT INTO Assets (AssetName, AssetType, Status, AssignedTo, UserID)
VALUES 
(N'Bàn làm việc', N'Nội thất', N'Đang sử dụng', N'Phòng Kế toán', 2),
(N'Ghế xoay', N'Nội thất', N'Đang sử dụng', N'Phòng Kế toán', 2),
(N'Máy in HP LaserJet', N'Thiết bị văn phòng', N'Chưa sử dụng', NULL, NULL),
(N'Tủ đựng hồ sơ', N'Nội thất', N'Đang sử dụng', N'Phòng Nhân sự', 3),
(N'Máy scan', N'Thiết bị văn phòng', N'Chưa sử dụng', NULL, NULL);

INSERT INTO Assets (AssetName, AssetType, Status, AssignedTo, UserID)
VALUES
(N'Bàn họp', N'Nội thất', N'Đang sử dụng', N'Phòng IT', 4),
(N'Tủ hồ sơ lớn', N'Nội thất', N'Đang sử dụng', N'Phòng Marketing', 5),
(N'Điều hòa Panasonic', N'Thiết bị văn phòng', N'Đang sử dụng', N'Phòng Kinh doanh', 6),
(N'Kệ sách', N'Nội thất', N'Chưa sử dụng', NULL, NULL),
(N'Bảng trắng', N'Thiết bị văn phòng', N'Đang sử dụng', N'Phòng Nhân sự', 7),
(N'Bàn tiếp khách', N'Nội thất', N'Đang sử dụng', N'Sảnh công ty', 8),
(N'Máy photocopy Canon', N'Thiết bị văn phòng', N'Đang sử dụng', N'Phòng Hành chính', 9),
(N'Tủ lạnh mini', N'Thiết bị văn phòng', N'Chưa sử dụng', NULL, NULL),
(N'Quạt hơi nước', N'Thiết bị văn phòng', N'Đang sử dụng', N'Kho vận', 10),
(N'Ghế sofa', N'Nội thất', N'Chưa sử dụng', NULL, NULL);


SELECT * FROM Assets;

--Bảng thiết bị
CREATE TABLE Devices (
    DeviceID INT PRIMARY KEY IDENTITY(1,1),
    DeviceName NVARCHAR(100) NOT NULL,
    DeviceType NVARCHAR(100),
    Status NVARCHAR(50) DEFAULT N'Chưa sử dụng',
    AssignedTo NVARCHAR(100),
    UserID INT NULL,
    AssignedDate DATETIME,
    CreatedDate DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Devices_Users FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Thêm cột ngày dự kiến hoàn trả
ALTER TABLE Devices ADD ReturnDate DATE NULL;

-- Thêm cột ngày hoàn trả thực tế
ALTER TABLE Devices ADD ActualReturnDate DATE NULL;

INSERT INTO Devices (DeviceName, DeviceType, Status, AssignedTo, UserID, AssignedDate)
VALUES 
(N'Laptop Dell XPS', N'Laptop', N'Đang sử dụng', N'Nguyễn Văn A', 2, GETDATE()),
(N'PC Dell Optiplex', N'Máy tính để bàn', N'Đang sử dụng', N'Trần Thị B', 3, GETDATE()),
(N'Máy chiếu Epson', N'Máy chiếu', N'Chưa sử dụng', NULL, NULL, NULL),
(N'Bàn phím cơ', N'Phụ kiện', N'Đang sử dụng', N'Nguyễn Văn A', 2, GETDATE()),
(N'Chuột không dây', N'Phụ kiện', N'Chưa sử dụng', NULL, NULL, NULL);

INSERT INTO Devices 
(DeviceName, DeviceType, Status, AssignedTo, UserID, AssignedDate, ReturnDate, ActualReturnDate)
VALUES
(N'Laptop HP Probook', N'Laptop', N'Đang sử dụng', N'Lê Văn C', 4, GETDATE(), '2026-06-10', NULL),
(N'Macbook Air M2', N'Laptop', N'Đang sử dụng', N'Phạm Thị D', 5, GETDATE(), '2026-06-15', NULL),
(N'PC Gaming MSI', N'Máy tính để bàn', N'Chưa sử dụng', NULL, NULL, NULL, NULL, NULL),
(N'Máy in Canon LBP2900', N'Máy in', N'Đang sử dụng', N'Hoàng Văn E', 6, GETDATE(), '2026-06-05', NULL),
(N'Tai nghe Logitech', N'Phụ kiện', N'Đang sử dụng', N'Đỗ Thị F', 7, GETDATE(), '2026-06-08', NULL),
(N'Màn hình Dell 24 inch', N'Màn hình', N'Chưa sử dụng', NULL, NULL, NULL, NULL, NULL),
(N'Ipad Gen 10', N'Máy tính bảng', N'Đang sử dụng', N'Bùi Văn G', 8, GETDATE(), '2026-06-12', NULL),
(N'Chuột Logitech MX', N'Phụ kiện', N'Chưa sử dụng', NULL, NULL, NULL, NULL, NULL),
(N'Máy chiếu Sony', N'Máy chiếu', N'Đang sử dụng', N'Vũ Thị H', 9, GETDATE(), '2026-06-20', NULL),
(N'Camera Logitech C920', N'Thiết bị họp', N'Chưa sử dụng', NULL, NULL, NULL, NULL, NULL);

SELECT * FROM Devices;

--Bảng báo cáo
CREATE TABLE Reports (
    ReportID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    ReportContent NVARCHAR(MAX),
    CreatedAt DATETIME DEFAULT GETDATE(),
    Status NVARCHAR(50) DEFAULT N'Chờ xử lý',
    
    CONSTRAINT FK_Reports_Users FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Thêm cột ghi chú xử lý
ALTER TABLE Reports ADD ProcessedNote NVARCHAR(500) NULL;

-- Thêm cột thời gian xử lý
ALTER TABLE Reports ADD ProcessedAt DATETIME NULL;

-- Thêm cột người xử lý
ALTER TABLE Reports ADD ProcessedBy INT NULL;

INSERT INTO Reports (UserID, ReportContent, Status)
VALUES 
(2, N'[THIẾT BỊ - Laptop Dell XPS] [Báo hỏng cần sửa] Bàn phím bị liệt một số phím', N'Chờ xử lý'),
(2, N'[TÀI SẢN - Bàn làm việc] [Cần sửa chữa] Chân bàn bị lung lay', N'Chờ xử lý'),
(3, N'[THIẾT BỊ - PC Dell Optiplex] [Cần bảo trì] Máy chạy chậm, cần vệ sinh', N'Đã xử lý');

INSERT INTO Reports (UserID, ReportContent, Status, ProcessedNote, ProcessedAt, ProcessedBy)
VALUES
(4, N'[THIẾT BỊ - Laptop HP Probook] [Báo lỗi] Máy nóng nhanh', N'Chờ xử lý', NULL, NULL, NULL),
(5, N'[THIẾT BỊ - Macbook Air M2] [Báo lỗi] Không kết nối được wifi', N'Chờ xử lý', NULL, NULL, NULL),
(6, N'[TÀI SẢN - Điều hòa Panasonic] [Bảo trì] Điều hòa chảy nước', N'Đã xử lý', N'Đã vệ sinh máy', GETDATE(), 1),
(7, N'[THIẾT BỊ - Tai nghe Logitech] [Hỏng] Không nghe được âm thanh', N'Chờ xử lý', NULL, NULL, NULL),
(8, N'[TÀI SẢN - Bảng trắng] [Hư hỏng] Bị nứt góc', N'Đã xử lý', N'Đã thay bảng mới', GETDATE(), 1),
(9, N'[THIẾT BỊ - Máy chiếu Sony] [Bảo trì] Hình ảnh mờ', N'Chờ xử lý', NULL, NULL, NULL),
(10, N'[TÀI SẢN - Ghế sofa] [Báo hỏng] Ghế bị rách', N'Chờ xử lý', NULL, NULL, NULL),
(4, N'[THIẾT BỊ - Camera Logitech C920] [Lỗi] Không nhận mic', N'Đã xử lý', N'Đã cập nhật driver', GETDATE(), 1),
(5, N'[THIẾT BỊ - Máy in Canon] [Lỗi] Kẹt giấy thường xuyên', N'Chờ xử lý', NULL, NULL, NULL),
(6, N'[TÀI SẢN - Tủ hồ sơ lớn] [Hư hỏng] Khóa bị kẹt', N'Đã xử lý', N'Đã thay khóa', GETDATE(), 1);


SELECT * FROM Reports;
SELECT ReportID, Status FROM Reports;

--Bảng yêu cầu mượn
CREATE TABLE BorrowRequests (
    RequestID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    AssetID INT NULL,
    DeviceID INT NULL,
    RequestReason NVARCHAR(500),
    RequestDate DATETIME DEFAULT GETDATE(),
    ExpectedBorrowDate DATE,
    ExpectedReturnDate DATE,
    Status NVARCHAR(50) DEFAULT N'Chờ xét duyệt',
    ApprovedBy INT NULL,
    HandoverDate DATE NULL,
    
    CONSTRAINT FK_BorrowRequests_Users FOREIGN KEY (UserID) REFERENCES Users(UserID),
    CONSTRAINT FK_BorrowRequests_Assets FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
    CONSTRAINT FK_BorrowRequests_Devices FOREIGN KEY (DeviceID) REFERENCES Devices(DeviceID),
    CONSTRAINT CHK_BorrowRequest_Type CHECK (AssetID IS NOT NULL OR DeviceID IS NOT NULL)
);

-- Thêm các cột cần thiết
ALTER TABLE BorrowRequests ADD ProcessedNote NVARCHAR(500) NULL;
ALTER TABLE BorrowRequests ADD ProcessedAt DATETIME NULL;
ALTER TABLE BorrowRequests ADD ProcessedBy INT NULL;

INSERT INTO BorrowRequests (UserID, AssetID, RequestReason, ExpectedBorrowDate, ExpectedReturnDate, Status)
VALUES 
(2, 3, N'Cần mượn máy in để in báo cáo cuối năm', '2026-5-20', '2026-5-22', N'Chờ xét duyệt'),
(3, 5, N'Máy scan cũ bị hỏng, cần mượn tạm', '2026-5-18', '2026-5-22', N'Đã duyệt');

INSERT INTO BorrowRequests
(UserID, AssetID, DeviceID, RequestReason, ExpectedBorrowDate, ExpectedReturnDate, Status, ApprovedBy, HandoverDate)
VALUES
(4, NULL, 8, N'Cần chuột để làm việc', '2026-05-26', '2026-06-02', N'Chờ xét duyệt', NULL, NULL),
(5, 8, NULL, N'Cần tủ lạnh cho phòng nghỉ', '2026-05-25', '2026-06-10', N'Đã duyệt', 1, '2026-05-25'),
(6, NULL, 10, N'Cần camera họp online', '2026-05-27', '2026-06-05', N'Chờ xét duyệt', NULL, NULL),
(7, 10, NULL, N'Cần ghế sofa tiếp khách', '2026-05-26', '2026-06-15', N'Từ chối', 1, NULL),
(8, NULL, 6, N'Cần màn hình làm việc', '2026-05-28', '2026-06-20', N'Đã duyệt', 1, '2026-05-28'),
(9, 4, NULL, N'Cần kệ sách lưu tài liệu', '2026-05-26', '2026-06-12', N'Chờ xét duyệt', NULL, NULL),
(10, NULL, 3, N'Cần PC để test phần mềm', '2026-05-29', '2026-06-30', N'Đã duyệt', 1, '2026-05-29'),
(4, 9, NULL, N'Cần quạt hơi nước cho kho', '2026-05-30', '2026-06-07', N'Chờ xét duyệt', NULL, NULL),
(5, NULL, 7, N'Cần iPad để thuyết trình', '2026-05-31', '2026-06-03', N'Đã duyệt', 1, '2026-05-31'),
(6, 6, NULL, N'Cần bàn tiếp khách cho sự kiện', '2026-06-01', '2026-06-05', N'Chờ xét duyệt', NULL, NULL);

SELECT * FROM BorrowRequests;
