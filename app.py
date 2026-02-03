from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = "khitoi182026"

@app.route("/")
def choose_role():
    return render_template("chon_role.html")

@app.route("/hocsinh/thongtin", methods=["GET", "POST"])
def hocsinh_select():
    df = pd.read_excel("data/danhsachhocsinh.xlsx")

    lop = sorted(df["lop"].unique())
    hocsinh = df.to_dict(orient="records")

    if request.method == "POST":
        session.clear()
        session["role"] = "hocsinh"
        session["lop"] = request.form["lop"]
        session["ten"] = request.form["ten"]
        return redirect("/hocsinh/trang_chu")

    return render_template(
        "/hoc_sinh/hocsinh_thongtin.html",
        lop=lop,
        hocsinh=hocsinh
    )

@app.route("/hocsinh/trang_chu")
def hocsinh_trang_chu():
    if session.get("role") != "hocsinh":
        return redirect("/")

    return render_template(
        "/hoc_sinh/hocsinh.html",
        ten=session["ten"],
        lop=session["lop"],
        menu_img="menu/{}.jpg".format(session["lop"])
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        df = pd.read_excel("data/giaovien_taikhoan.xlsx")

        df["username"] = df["username"].astype(str).str.strip()
        df["password"] = df["password"].astype(str).str.strip()

        acc = df[(df.username == user) & (df.password == pwd)]

        if not acc.empty:
            session["role"] = "giaovien"
            session["username"] = user
            return redirect("/giaovien/trang_chu")

        return "Sai tài khoản hoặc mật khẩu"

    return render_template("giaovien_dangnhap.html")

@app.route("/giaovien/trang_chu")
def giaovien_trang_chu():
    if session.get("role") != "giaovien":
        return redirect("/login")

    return render_template(
        "giaovien.html",
        user=session["username"]
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

from datetime import datetime
import os

checkin_FILE = "data/checkin.xlsx"
hocsinh_FILE = "data/hocsinh.xlsx"

@app.route("/scan")
def scan():
    if session.get("role") != "giaovien":
        return redirect("/login")

    return render_template("qr_scan.html")

# có thể tách hàm quét qr ra file riêng, sau đó import vào là được ._.
@app.route("/qr-result", methods=["POST"])
def qr_result():
    if session.get("role") != "giaovien":
        return "Không đủ quyền hạn để truy cập"
    ma_hs = str(request.json.get("ma_hs")).strip()
    giam_thi = session.get("username")

    df_hocsinhs = pd.read_excel(hocsinh_FILE, dtype={"ma_hs": str})

    hs = df_hocsinhs[df_hocsinhs["ma_hs"] == ma_hs]
    if hs.empty:
        return "Không tìm thấy học sinh"

    ten = hs.iloc[0]["ten"]
    lop = hs.iloc[0]["lop"]

    if not os.path.exists(checkin_FILE):
        df_checkin = pd.DataFrame(
            columns=["ma_hs", "ten", "lop", "time", "giao_vien"]
        )
    else:
        df_checkin = pd.read_excel(checkin_FILE, dtype=str)
        df_checkin.columns = df_checkin.columns.str.strip()

    if "ma_hs" not in df_checkin.columns:
        return "File checkin.xlsx sai cấu trúc"

    if (df_checkin["ma_hs"] == ma_hs).any():
        old = df_checkin[df_checkin["ma_hs"] == ma_hs].iloc[0]
        return (
            f"ĐÃ KIỂM TRA TRƯỚC ĐÓ\n"
            f"{old['ten']} – {old['lop']}\n"
            f"Lúc {old['time']} bởi {old['giam_thi']}"
        )

    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    new_row = {
        "ma_hs": ma_hs,
        "ten": ten,
        "lop": lop,
        "time": now,
        "giam_thi": giam_thi
    }

    df_checkin = pd.concat(
        [df_checkin, pd.DataFrame([new_row])],
        ignore_index=True
    )

    df_checkin.to_excel(checkin_FILE, index=False)

    return f"KIỂM TRA THÀNH CÔNG\n {ten} – {lop}"

@app.route("/map")
def view_map():
    role = session.get("role")

    if role == "hocsinh":
        back_url = "/hocsinh/trang_chu"
    elif role == "giaovien":
        back_url = "/giaovien/trang_chu"
    else:
        return redirect("/")

    return render_template(
        "map.html",
        back_url=back_url
    )

@app.route("/menu", methods=["GET", "POST"])
def choose_menu_class():
    role = session.get("role")
    if role not in ["hocsinh", "giaovien"]:
        return redirect("/")
    
    classes = [
        "12.1", "12.2", "12.3",
        "12.4", "12.5", "12.6",
        "12A1", "12A2", "12A3",
        "12A4", "12A5", "12A6",
        "12B", "12H", 
        "12D1", "12D2", "12D3",
        "12L1", "12L2", "12L3", "12L4"
    ]

    if request.method == "POST":
        lop = request.form["lop"]
        return redirect(url_for("view_menu", lop=lop))

    return render_template(
        "chon_lop.html", 
        classes=classes,
        back_url="/hocsinh/trang_chu" if role == "hocsinh" else "/giaovien/trang_chu"
        )

@app.route("/menu/<lop>")
def view_menu(lop):

    role = session.get("role")
    if role not in ["hocsinh", "giaovien"]:
        return redirect("/")

    return render_template(
        "menu.html",
        lop=lop,
        menu_img=f"menu/{lop}.jpg",
        back_url="/hocsinh/trang_chu" if role == "hocsinh" else "/giaovien/trang_chu"
    )

# back dựa vào role, cơ mà để đấy nào rảnh sẽ sửa vào =))))
# def get_back_url():
#     return "/hocsinh/trang_chu" if session.get("role") == "hocsinh" else "/giaovien/trang_chu"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
