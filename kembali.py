from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

# Declarative base yang akan di-inherit oleh setiap model
Base = declarative_base()


class KembaliModel(Base):
    """
    Model class untuk tabel Kembali
    """
    __tablename__  = 'tKembali'
    kodeKembali = Column(Integer, primary_key=True)
    kodeBuku = Column(Integer, ForeignKey("tBuku.kodeBuku"), nullable=False)
    nim = Column(Integer, ForeignKey("tAnggota.nim"), nullable=False)
    tanggalKembali = Column(String(20), nullable=False)

    def __init__(self, kodeKembali, kodeBuku, nim, tanggalKembali):
        self.kodeKembali = kodeKembali
        self.kodeBuku = kodeBuku
        self.nim = nim
        self.tanggalKembali = tanggalKembali

    def __repr__(self):
        return 'Kembali: {kodePinjam: %d, kodeBuku: %d, nim: %d, tanggalKembali: %s}' % \
               (self.kodePinjam, self.kodeBuku, self.nim, self.tanggalKembali)


class KembaliHelper:
    """
    Class helepr untuk tabel Kembali.
    Berisi operas dasar untuk tabel (CRUD).
    """
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, kembali: KembaliModel):
        """Membuat model kembali baru dan masuk ke dalam database"""
        with Session(self.engine) as session:
            session.add(kembali)
            session.commit()

    def update(self, kode_kembali, newKembali: KembaliModel):
        """Mengubah data kembali berdasarkan kode kembali"""
        with Session(self.engine) as session:
            the_kembali: KembaliModel = self.read_one(kode_kembali)
            the_kembali.kodeBuku = newKembali.kodeBuku
            the_kembali.nim = newKembali.nim
            the_kembali.tanggalKembali = newKembali.tanggalKembali
            session.add(the_kembali)
            session.commit()

    def delete(self, kode_kembali):
        """
        Menghapus salah satu kembali dari database.
        :param kode_kembali: pencarian berdasarkan kode pinjam
        :return: None
        """
        with Session(self.engine) as session:
            the_kembali = self.read_one(kode_kembali)
            session.delete(the_kembali)
            session.commit()

    def read(self):
        """
        Query semua isi dari tabel tKembali
        :return: Semua isi tabel dari tKembali
        """

    def read_one(self, kode_kembali):
        """
        Query salah satu dari isi tabel tKembali berdasakan kode_kembali
        :param kode_kembali:
        :return:
        """
        with Session(self.engine) as session:
            stmt = select(KembaliModel).where(KembaliModel.kodeKembali == kode_kembali)
            return session.scalars(stmt).one()