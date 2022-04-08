from flask import Flask, render_template, request, \
    flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from anggota import *
from buku import *
from kembali import *
from pinjaman import *

from datetime import date
import time
from random import randint

engine = create_engine("sqlite:///dbPerpusOn.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PUGIOIFFG WEIFVOEIFG IEUFG FBEYOFIHOEWF HBEOYWEHBCORT RUGFBOIDJV'

anggota_helper = AnggotaHelper(engine)
anggota_helper.read()
buku_helper = BukuHelper(engine)
kembali_helper = KembaliHelper(engine)
pinjaman_helper = PinajmanHelper(engine)


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
    return render_template('pinjam.html', list=pinjaman_helper.read())


@app.route('/pinjaman/create', methods=['GET', 'POST'])
def create_pinjaman():
    if request.method == 'POST':
        nim = int(request.form['nim'])
        kodePinjam = randint(1111111, 9999999) ^ nim
        kodeBuku = int(request.form['kodeBuku'])
        tanggalPinjam = date.today().strftime("%Y/%m/%d")
        new_pinjaman = PinjamanModel(kodePinjam, kodeBuku, nim, tanggalPinjam)
        pinjaman_helper.create(new_pinjaman)
        buku_helper.decrease_one(kodeBuku)
        return redirect(url_for('view_pinjaman'))
    else:
        return render_template('create/pinjaman_create.html',
                               buku_list=buku_helper.read(),
                               anggota_list=anggota_helper.read())


@app.route('/pinjaman/edit/<kode_pinjaman>', methods=['GET', 'POST'])
def edit_pinjaman(kode_pinjaman):
    the_pinjaman: PinjamanModel = pinjaman_helper.read_one(kode_pinjaman)
    if request.method == 'POST':
        nim = request.form['nim']
        the_pinjaman.nim = nim
        pinjaman_helper.update(kode_pinjaman, the_pinjaman)
        return redirect(url_for('view_pinjaman'))
    else:
        return render_template('edit/pinjam_edit.html', pinjaman=the_pinjaman, anggota_list=anggota_helper.read())


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
    # TODO: CHECK BOOK CONSTRAINTS FROM PINJAMAN TABLE

    pass


if __name__ == '__main__':
    app.run(debug=True)
