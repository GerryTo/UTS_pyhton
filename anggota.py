from sqlalchemy import Column, String, Integer
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

# Declarative base yang akan di-inherit oleh setiap model
Base = declarative_base()


class AnggotaModel(Base):
    """
    Model Class untuk tabel Anggota.
    """
    __tablename__ = 'tAnggota'
    nim = Column(Integer, primary_key=True)
    nama = Column(String(60))
    jurusan = Column(String(30))

    def __init__(self, nim: int, nama: str, jurusan: str):
        self.nim = nim
        self.nama = nama
        self.jurusan = jurusan

    def __repr__(self):
        return 'Anggota: {nim: %d, nama: %s, jurusan: %s}' % (self.nim, self.nama, self.jurusan)


class AnggotaHelper:
    """
    Class helper untuk tabel Anggota.
    Berisi operasi dasar untuk tabel (CRUD).
    """
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, anggota: AnggotaModel):
        """Membuat model Anggota baru dan masuk ke dalam database."""
        with Session(self.engine) as session:
            session.add(anggota)
            session.commit()

    def update(self, nim, newAnggota: AnggotaModel):
        """Mengubah data angota berdasarkan nim."""
        with Session(self.engine) as session:
            theAnggota: AnggotaModel = self.read_one(nim)
            theAnggota.nama = newAnggota.nama
            theAnggota.jurusan = newAnggota.jurusan
            session.add(theAnggota)
            session.commit()

    def delete(self, nim):
        """
        Menghapus salah satu anggota dari database.

        Akan gagal bila masih ada nim yang terdapat dalam
        tabel tKembali dan tPinjaman.
        """
        with Session(self.engine) as session:
            theAnggota = self.read_one(nim)
            session.delete(theAnggota)
            session.commit()

    def read(self):
        """Query semua isi dari tabel tAnggota."""
        with Session(self.engine) as session:
            return session.query(AnggotaModel)

    def read_one(self, nim):
        """Query salah satu dari isi tabel tAnggota berdasarkan nim."""
        with Session(self.engine) as session:
            stmt = select(AnggotaModel).where(AnggotaModel.nim == nim)
            return session.scalars(stmt).one()
