cd project -> pip install requirements.txt

Route của web hoạt động như sau:
→ Chọn vai trò
   ├── học sinh → chọn lớp + tên → thông tin học sinh + map + menu các lớp
   └── giáo viên → đăng nhập → map + menu các lớp + quét QR

Chưa thêm CSS, chỉ đang thuần HTMl, các hàm trong app.py được tổng hợp và chưa tách thành các file riêng

Test trên điện thoại:
- Đối với android: python app.py trong terminal, dựa vào ip của máy, vd: 192.167.1.36:5000 -> http://192.167.1.36:5000
- Đối với ios: cài và giải nén ngrok, để file exe vào project, run app.py xong mở thêm 1 terminal gõ ./ngrok http 5000(dựa vào đuôi ip của máy)

Trường hợp run app hay ngrok không được hãy nghĩ đến khả năng chưa cd vào project, chưa cài các tài nguyên cần thiết
