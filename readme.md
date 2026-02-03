cd project -> pip install requirements.txt

Route của web hoạt động như sau:
→ Chọn vai trò
   - học sinh → chọn lớp + tên → thông tin học sinh + map + menu các lớp + menu lớp mình
   - giáo viên → đăng nhập → map + menu các lớp + quét QR

* Đang thuần HTML, chưa des web, các hàm được gọi chung trong app.py, chưa được tách riêng

Test trên điện thoại:
- Đối với android: python app.py trong terminal, dựa vào ip của máy, vd: 192.167.1.36:5000 -> http://192.167.1.36:5000
- Đối với ios: cài và giải nén ngrok (nếu trong project chưa có), đặt file exe vào project, run app.py xong mở thêm 1 terminal gõ ./ngrok http 5000 (giống vd của android) -> mở link forwarding trên điện thoại
