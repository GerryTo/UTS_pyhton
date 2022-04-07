from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from anggota import AnggotaModel
from buku import BukuModel

# Declarative base yang akan di-inherit oleh setiap model
Base = declarative_base()


class PinjamanModel(Base):
    """
    Model Class untuk tabel tPinjam
    """
    __tablename__ = 'tPinjaman'
    kodePinjam = Column(Integer, primary_key=True)
    kodeBuku = Column(Integer, ForeignKey(BukuModel.kodeBuku), nullable=False)
    nim = Column(Integer, ForeignKey(AnggotaModel.nim), nullable=False)
    tanggalPinjam = Column(String(20), nullable=False)

    def __init__(self, kodePinjam, kodeBuku, nim, tanggalPinjam):
        self.kodePinjam = kodePinjam
        self.kodeBuku = kodeBuku
        self.nim = nim
        self.tanggalPinjam = tanggalPinjam

    def __repr__(self):
        return 'Pinjaman: {kodePinjam: %d, kodeBuku: %d, nim: %d, tanggalPinjam: %s}' % \
               (self.kodePinjam, self.kodeBuku, self.nim, self.tanggalPinjam)


class PinajmanHelper:
    """
    Class helper untuk tabel Pinjaman.
    Berisi operasi dasar untuk tabel (CRUD).
    """
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, pinjaman: PinjamanModel):
        """Membuat model pinjaman baru dan masuk ke dalam database."""
        with Session(self.engine) as session:
            session.add(pinjaman)
            session.commit()

    def update(self, kode_pinjam, newPinjaman: PinjamanModel):
        """Mengubah data pnjaman berdasarkan kode pinjam."""
        with Session(self.engine) as session:
            the_pinjaman: PinjamanModel = self.read_one(kode_pinjam)
            the_pinjaman.kodeBuku = newPinjaman.kodeBuku
            the_pinjaman.nim = newPinjaman.nim
            the_pinjaman.tanggalPinjam = newPinjaman.tanggalPinjam
            session.add(the_pinjaman)
            session.commit()

    def delete(self, kode_pinjam):
        """
        Menghapus salah satu pinjaman dari database.
        """
        with Session(self.engine) as session:
            the_pinjaman = self.read_one(kode_pinjam)
            session.delete(the_pinjaman)
            session.commit()

    def read(self):
        """Query semua isi dari tabel tpinjaman."""
        with Session(self.engine) as session:
            return session.query(PinjamanModel)

    def read_one(self, kode_pinjam):
        """Query salah satu dari isi tabel tpinjaman berdasarkan kode_pinjam."""
        with Session(self.engine) as session:
            stmt = select(PinjamanModel).where(PinjamanModel.kodePinjam == kode_pinjam)
            return session.scalars(stmt).one()
