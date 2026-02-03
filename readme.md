Route của web hoạt động như sau:
→ Chọn vai trò
   - học sinh → chọn lớp + tên → thông tin học sinh + map + menu các lớp + menu lớp mình
   - giáo viên → đăng nhập → map + menu các lớp + quét QR

Test trên điện thoại:
cd project -> pip install requirements.txt -> python app.py

- Đối với android: python app.py trong terminal, dựa vào ip của máy, vd: 192.167.1.36:5000 -> http://192.167.1.36:5000
- Đối với ios: cài và giải nén ngrok (nếu trong project chưa có), đặt file exe vào project, run app.py xong mở thêm 1 terminal gõ ./ngrok http 5000 (giống vd của android) -> mở link forwarding trên điện thoại

- Trong data gồm file tài khoảng gv và danh sách học sinh, mn có thể thêm bừa vào để test xem oki hong nhá. Mã QR thì cứ điền bừa vào ma_hs trong danhsachhocsinh.xlsx sau đó generate nó trên web QR nhé.
- File checkin.xlsx sẽ được auto tạo ra khi quét QR, đừng tạo trước để tránh lỗi nhé.
