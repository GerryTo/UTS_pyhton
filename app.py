from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from anggota import *
from buku import *
from kembali import *
from pinjaman import *

engine = create_engine("sqlite:///dbPerpusOn.db")
app = Flask(__name__)

anggota_helper = AnggotaHelper(engine)
buku_helper = BukuHelper(engine)
kembali_helper = KembaliHelper(engine)
pinjaman_helper = PinajmanHelper(engine)


