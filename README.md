# 🎓 FTU Student Data Fetcher

Dự án này giúp bạn lấy danh sách sinh viên từ hệ thống tra cứu thông tin của **Đại học Ngoại thương (FTU)** cho từng khóa học hoặc ngành cụ thể.
## Trong folder data đã có một số khóa (có thể liên hệ tôi để lấy dữ liệu nếu không muốn tự chạy)

## 🚀 Hướng dẫn sử dụng

### 1️⃣ Cài đặt Python
Trước khi chạy, hãy đảm bảo bạn đã cài đặt **Python 3.x**. Nếu chưa, bạn có thể tải tại:  
🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

### 2️⃣ Chạy script để lấy dữ liệu

#### 🔹 Lấy toàn bộ danh sách sinh viên của khóa K59
```sh
python fetch_data_ftu_k59_all.py
```
#### 🔹 Lấy danh sách sinh viên của K59 theo nhóm ngành
```sh
python fetch_data_ftu_k59_divided_majors.py
```
✅ Danh sách sẽ được lưu vào một thư mục chứa các file CSV theo từng nhóm ngành.

✅ File merge_file.py giúp ghép các file ngành học thành một file duy nhất.
#### 🔹 Lấy danh sách sinh viên theo ngành cụ thể
```sh
python fetch_ftu_data_k59_major.py
```
Bạn cần sửa giá trị MAJOR_IDS trong file fetch_ftu_data_k59_major.py để chỉ định ngành muốn lấy.

📌 Danh sách mã ngành học cụ thể

| Ngành học              | Mã ngành                        |
|------------------------|--------------------------------|
| Kế toán               | `["810", "820"]`               |
| Kinh doanh quốc tế    | `["510", "520", "530", "550"]` |
| Kinh tế               | `["110", "120", "140", "150"]` |
| Kinh tế quốc tế       | `["410", "450", "420"]`        |
| Luật                  | `["610"]`                      |
| Ngôn ngữ Anh         | `["710"]`                      |
| Ngôn ngữ Nhật        | `["740", "750"]`               |
| Ngôn ngữ Pháp        | `["730", "760"]`               |
| Ngôn ngữ Trung       | `["720", "770"]`               |
| Quản trị khách sạn    | `["920"]`                      |
| Quản trị kinh doanh   | `["210", "250", "280"]`        |
| Tài chính - Ngân hàng | `["310", "320", "330", "340", "380"]` |

📌 Cách thay đổi ngành học muốn lấy dữ liệu:
Mở file fetch_ftu_data_k59.py, tìm biến MAJOR_IDS và thay thế bằng mã ngành mong muốn.
Ví dụ: Nếu muốn lấy danh sách sinh viên ngành Kinh tế quốc tế, sửa như sau:

MAJOR_IDS = ["410", "450", "420"]

### Hướng dẫn các sửa đổi trong code để phù hợp với các khóa

🌐 Chọn khóa học để lấy dữ liệu
Nếu muốn lấy dữ liệu của các khóa khác, bạn cần chỉnh sửa biến URL trong các file Python:



K56, K57, K58	

"https://tracuuthongtin.ftu.edu.vn/08_select_tracuuemail_msv2020.php"

K59	

"https://tracuuthongtin.ftu.edu.vn/03_select_tracuuemail_k59.php"

📌 Cách thay đổi URL trong code:
Mở file cần chạy, tìm dòng:

URL = "https://tracuuthongtin.ftu.edu.vn/03_select_tracuuemail_k59.php"

Sau đó thay đổi URL theo khóa học bạn muốn lấy.

📌 Trong mỗi chương trình đều có dòng sau:

#Sua: K59 = 20, K58 = 19, K57 = 18, K56 = 17

Sửa 2 số sau f để lấy đúng khóa.

Ví dụ: f"20 là Khóa 59

📌 Thay đổi tên package RESULT_DIR để tương ứng với khóa bạn muốn lấy.

📌 Thay đổi tên file kết quả result_file và file result_file cho đúng với khóa để tránh trùng lặp (Đối với chương trình: python fetch_data_ftu_k59_divided_majors.py)-(Được đánh dấu #Sua tại mỗi chỗ cần sửa).

💡 Góp Ý & Liên Hệ
Nếu có bất kỳ câu hỏi hay cải tiến nào, hãy tạo một issue hoặc liên hệ với  tôi:

Facebook: 
https://www.facebook.com/nguyen.ngoc.thuong.559145/

Email: 
nntthuong.it@gmail.com

🚀 Chúc bạn sử dụng hiệu quả!