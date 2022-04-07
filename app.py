from flask import Flask, render_template, request,\
        flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from anggota import *
from buku import *
from kembali import *
from pinjaman import *

from datetime import date

engine = create_engine("sqlite:///dbPerpusOn.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PUGIOIFFG WEIFVOEIFG IEUFG FBEYOFIHOEWF HBEOYWEHBCORT RUGFBOIDJV'

anggota_helper = AnggotaHelper(engine)
anggota_helper.read()
buku_helper = BukuHelper(engine)
kembali_helper = KembaliHelper(engine)
pinjaman_helper = PinajmanHelper(engine)


def can_pinjam_buku(kode_buku) -> bool:
    the_buku: BukuModel = buku_helper.read_one(kode_buku)
    return the_buku.stok > 0


def do_pinjam_buku(nim, kode_buku):
    if not can_pinjam_buku(kode_buku):
        raise "Buku sudah habis"
    current_date_str = date.today().strftime("%Y/%m/%d")


def do_kembali_buku(nim, kode_buku):
    pass


@app.route('/anggota', methods=['GET'])
def view_anggota():
    return render_template('html/anggota.html', list=anggota_helper.read())


@app.route('/anggota/create', methods=['GET', 'POST'])
def create_anggota():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        jurusan = request.form['jurusan']
        new_anggota = AnggotaModel(nim, nama, jurusan)
        anggota_helper.create(new_anggota)
        return redirect(url_for('view_anggota'))
    else:
        return render_template('create/anggota_create.html')


@app.route('/angota/edit/<nim>', methods=['GET', 'POST'])
def edit_anggota(nim):
    if request.method == 'POST':
        pass
    else:
        pass


@app.route('/anggota/delete/<nim>', methods=['GET'])
def delete_anggota(nim):
    anggota_helper.delete(nim)
    return redirect(url_for('view_anggota'))


@app.route('/pinjaman', methods=['GET'])
def view_pinjaman():
    return render_template('html/pinjam.html', list=pinjaman_helper.read())


@app.route('/pinjaman/create', methods=['GET', 'POST'])
def create_pinjaman():
    if request.method == 'POST':
        kodePinjam = request.form['kodePinjam']
        kodeBuku = request.form['kodeBuku']
        nim = request.form['nim']
        tanggalPinjam = request.form['tanggalPinjam']
        new_pinjaman = PinjamanModel(kodePinjam, kodeBuku, nim, tanggalPinjam)
        pinjaman_helper.create(new_pinjaman)
        return redirect(url_for('view_pinjaman'))
    else:
        return render_template('create/pinjaman_create.html',
                               buku_list=buku_helper.read(),
                               anggota_list=anggota_helper.read())


if __name__ == '__main__':
    app.run(debug=True)

