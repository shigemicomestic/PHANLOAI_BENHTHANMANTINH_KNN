import pyodbc
from flask import Flask, jsonify, render_template, request
from joblib import load
import pandas as pd
from datetime import datetime
import numpy as np

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=PHAMNHUTTHANG;DATABASE=KQ_BenhThanManTinh;UID=sa;PWD=123')
cursor = conn.cursor()

app = Flask(__name__)
model = load('D:\\PhamNhutThang_2001200549\\NAM 3 HK2\\TH HOC MAY\\DOAN_TH_HOCMAY\\templates\\KNN_real.joblib')

@app.route('/')
def home():
    cursor.execute('SELECT * FROM KetQua')
    rows = cursor.fetchall()
    return render_template('web.html', data=rows)

@app.route('/process_data', methods=['POST'])
def process_data():
    data = []
    thongtin = []
    tenBN = request.form['TenBN']
    thongtin.append(tenBN)
    gioiTinh = request.form['GioiTinh']
    thongtin.append(gioiTinh)

    age = float(request.form['age'])
    data.append(age)

    # Collect bp
    bp = float(request.form['bp'])
    data.append(bp)

    # Collect sg
    sg = float(request.form['sg'])
    data.append(sg)

    # Collect al
    al = float(request.form['al'])
    data.append(al)

    # Collect rbc
    rbc = float(request.form['rbc'])
    data.append(rbc)

    # Collect pc
    pc = int(request.form['pc'])
    data.append(pc)

    # Collect pcc
    pcc = int(request.form['pcc'])
    data.append(pcc)

    # Collect ba
    ba = int(request.form['ba'])
    data.append(ba)

    # Collect bgr
    bgr = float(request.form['bgr'])
    data.append(bgr)

    # Collect bu
    bu = float(request.form['bu'])
    data.append(bu)

    # Collect sc
    sc = float(request.form['sc'])
    data.append(sc)

    # Collect sod
    sod = float(request.form['sod'])
    data.append(sod)

    # Collect pot
    pot = float(request.form['pot'])
    data.append(pot)

    # Collect hemo
    hemo = float(request.form['hemo'])
    data.append(hemo)

    # Collect pcv
    pcv = float(request.form['pcv'])
    data.append(pcv)

    # Collect wc
    wc = float(request.form['wc'])
    data.append(wc)

    # Collect rc
    rc = float(request.form['rc'])
    data.append(rc)

    # Collect htn
    htn = int(request.form['htn'])
    data.append(htn)

    # Collect dm
    dm = int(request.form['dm'])
    data.append(dm)

    # Collect cad
    cad = int(request.form['cad'])
    data.append(cad)

    # Collect appet
    appet = int(request.form['appet'])
    data.append(appet)

    # Collect pe
    pe = int(request.form['pe'])
    data.append(pe)

    # Collect ane
    ane = int(request.form['ane'])
    data.append(ane)
    data = np.array(data).reshape(1, -1)  # Reshape the data

    prediction = model.predict(data)[0]

    if prediction == 'ckd':
        chuandoan = 'ckd'
    else:
        chuandoan = 'notckd'
        
    return render_template('ketqua.html', chuandoan=chuandoan, tenBN=tenBN, gioiTinh=gioiTinh)

@app.route('/save_result', methods=['POST'])
def save_result():
    data = []
    tenBN = request.form['TenBN']
    data.append(tenBN)
    gioiTinh = request.form['GioiTinh']
    data.append(gioiTinh)
    ngayKham = request.form['NgayKham']
    date = datetime.strptime(ngayKham, "%d/%m/%Y").date()
    data.append(date)
    chuanDoan = request.form['ChuanDoan']
    data.append(chuanDoan)
    ghiChu = request.form['GhiChu']
    data.append(ghiChu)

    cursor.execute("UPDATE KetQua SET NgayKham=?, ChuanDoan=?, GhiChu=?, GioiTinh=? WHERE TenBN=?", (date, chuanDoan, ghiChu, gioiTinh, tenBN))
    conn.commit()

    response = {"message": "Kết quả đã được lưu thành công!"}
    return jsonify(response)


if __name__ == '__main__':
    app.run()
