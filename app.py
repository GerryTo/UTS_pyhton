from flask import Flask, render_template, \
                    request, redirect, url_for
from sqlalchemy import create_engine
from anggota import *
from buku import *
from kembali import *
from pinjaman import *

from datetime import date
import time

engine = create_engine("sqlite:///dbPerpusOn.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PUGIOIFFG WEIFVOEIFG IEUFG FBEYOFIHOEWF HBEOYWEHBCORT RUGFBOIDJV'

anggota_helper = AnggotaHelper(engine)
anggota_helper.read()
buku_helper = BukuHelper(engine)
kembali_helper = KembaliHelper(engine)
pinjaman_helper = PinajmanHelper(engine)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/anggota', methods=['GET'])
def view_anggota():
    return render_template('anggota.html', anggota_list=anggota_helper.read())


@app.route('/anggota/create', methods=['POST'])
def create_anggota():
    nim = request.form['nim']
    nama = request.form['nama']
    jurusan = request.form['jurusan']
    new_anggota = AnggotaModel(nim, nama, jurusan)
    anggota_helper.create(new_anggota)
    return redirect(url_for('view_anggota'))


@app.route('/anggota/edit/<nim>', methods=['POST'])
def edit_anggota(nim):
    the_anggota: AnggotaModel = anggota_helper.read_one(nim)
    the_anggota.nama = request.form['nama']
    the_anggota.jurusan = request.form['jurusan']
    anggota_helper.update(nim, the_anggota)
    return redirect(url_for('view_anggota'))


@app.route('/anggota/delete/<nim>', methods=['GET'])
def delete_anggota(nim):
    anggota_helper.delete(nim)
    return redirect(url_for('view_anggota'))


@app.route('/pinjaman', methods=['GET'])
def view_pinjaman():
    return render_template('pinjaman.html', pinjaman_list=pinjaman_helper.read(),
                                          buku_list=buku_helper.read(),
                                          anggota_list=anggota_helper.read())


@app.route('/pinjaman/create', methods=['POST'])
def create_pinjaman():
    nim = int(request.form['nim'])
    kodePinjam = int(time.time() * 100) ^ nim
    kodeBuku = int(request.form['kodeBuku'])
    tanggalPinjam = date.today().strftime("%Y/%m/%d")
    new_pinjaman = PinjamanModel(kodePinjam, kodeBuku, nim, tanggalPinjam)
    pinjaman_helper.create(new_pinjaman)
    buku_helper.decrease_one(kodeBuku)
    return redirect(url_for('view_pinjaman'))


@app.route('/pinjaman/edit/<kode_pinjaman>', methods=['POST'])
def edit_pinjaman(kode_pinjaman):
    the_pinjaman: PinjamanModel = pinjaman_helper.read_one(kode_pinjaman)
    nim = request.form['nim']
    the_pinjaman.nim = nim
    pinjaman_helper.update(kode_pinjaman, the_pinjaman)
    return redirect(url_for('view_pinjaman'))


@app.route('/pinjaman/delete/<kode_pinjaman>', methods=['GET'])
def delete_pinjaman(kode_pinjaman):
    the_pinjaman: PinjamanModel = pinjaman_helper.read_one(kode_pinjaman)
    kode_buku = the_pinjaman.kodeBuku
    pinjaman_helper.delete(kode_pinjaman)
    buku_helper.add_one(kode_buku)
    return redirect(url_for('view_pinjaman'))


@app.route('/buku', methods=['GET'])
def view_buku():
    return render_template('buku.html', buku_list=buku_helper.read())


@app.route('/buku/create', methods=['POST'])
def create_buku():
    nama_buku = request.form['nama']
    kode_buku = nama_buku.__hash__() ^ int(time.time() * 100)  # time diff until ms
    jumlah_buku = request.form['jumlah']
    the_buku = BukuModel(kode_buku, nama_buku, jumlah_buku)
    buku_helper.create(the_buku)

    return redirect(url_for('view_buku'))


@app.route('/buku/edit/<kode_buku>', methods=['POST'])
def edit_buku(kode_buku):
    the_buku: BukuModel = buku_helper.read_one(kode_buku)
    the_buku.judulBuku = request.form['nama']
    the_buku.stok = request.form['jumlah']
    buku_helper.update(kode_buku, the_buku)

    return redirect(url_for('view_buku'))


@app.route('/buku/delete/<kode_buku>', methods=['GET'])
def delete_buku(kode_buku):
    buku_helper.delete(kode_buku)
    return redirect(url_for('view_buku'))


@app.route('/kembali', methods=['GET'])
def view_kembali():
    return render_template('kembali.html',
                           kembali_list=kembali_helper.read(),
                           anggota_list=anggota_helper.read(),
                           buku_list=buku_helper.read())


@app.route('/kembali/create', methods=['POST'])
def create_kembali():
    nim = int(request.form['nim'])
    kode_kembali = int(time.time() * 100) ^ nim
    kode_buku = request.form['kodeBuku']
    tanggal_kembali = date.today().strftime("%Y/%m/%d")
    new_kembali = KembaliModel(kode_kembali, kode_buku, nim, tanggal_kembali)
    kembali_helper.create(new_kembali)
    buku_helper.add_one(kode_buku)

    return redirect(url_for('view_kembali'))


@app.route('/kembali/edit/<kode_kembali>', methods=['POST'])
def edit_kembali(kode_kembali):
    the_kembali: KembaliModel = kembali_helper.read_one(kode_kembali)
    the_kembali.nim = request.form['nim']
    kembali_helper.update(kode_kembali, the_kembali)
    return redirect(url_for('view_kembali'))


@app.route('/kembali/delete/<kode_kembali>', methods=['GET'])
def delete_kembali(kode_kembali):
    kembali_helper.delete(kode_kembali)
    return redirect(url_for('view_kembali'))


if __name__ == '__main__':
    app.run(debug=True)
