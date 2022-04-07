from sqlalchemy import Column, String, Integer
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

# Declarative base yang akan di-inherit oleh setiap model
Base = declarative_base()


class BukuModel(Base):
    """
    Model class untuk tabel buku
    """
    __tablename__ = 'tbuku'
    kodeBuku = Column(Integer, primary_key=True)
    judulBuku = Column(String(30), nullable=True)
    stok = Column(Integer, nullable=False)

    def __init__(self, kodeBuku, judulBuku, stok):
        self.kodeBuku = kodeBuku
        self.judulBuku = judulBuku
        self.stok = stok

    def __repr__(self):
        return 'Buku: {kodeBuku: %d, judulBuku: %s, stok: %d}' % \
               (self.kodeBuku, self.judulBuku, self.stok)


class BukuHelper:
    """
    Class helper untukk tabel Buku
    Berisi operadsi dasar untuk tabel (CRUD).
    """
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, buku: BukuModel):
        """
        Membuat model buku baru dan masuk ke dalam database.
        :param buku: Buku baru
        :return:
        """
        with Session(self.engine) as session:
            session.add(buku)
            session.commit()

    def update(self, kodeBuku, newBuku: BukuModel):
        """
        Mengubah salah satu data buku berdasarrkan kodeBuku
        :param kodeBuku: kode yang dicari untuk diubah
        :param newBuku: buku untuk diganti
        :return:
        """
        with Session(self.engine) as session:
            the_buku: BukuModel = self.read_one(kodeBuku)
            the_buku.judulBuku = newBuku.judulBuku
            the_buku.stok = newBuku.stok
            session.add(the_buku)
            session.commit()

    def delete(self, kodeBuku):
        """
        Menghapus salah satu buku darii tabel
        :param kodeBuku: buku yang ingin dihapus
        :return:
        """
        with Session(self.engine) as session:
            the_buku = self.read_one(kodeBuku)
            session.delete(the_buku)
            session.commit()

    def read(self):
        """
        Query semua isi dari tabel buku
        :return: Buku yang ada di dalam tabel
        """
        with Session(self.engine) as session:
            return session.query(BukuModel)

    def read_one(self, kode_buku):
        """
        Query salah satu dari isi tabel tBuku berdasarkan kode_buku
        :param kode_buku: yang ingin dicari
        :return: BukuModel yang dicari
        """
        with Session(self.engine) as session:
            stmt = select(BukuModel).where(BukuModel.kodeBuku == kode_buku)
            return session.scalars(stmt).one()
