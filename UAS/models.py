from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class kamera(Base):
    __tablename__ = 'kamera'
    nama_kamera: Mapped[str] = mapped_column(primary_key=True)
    penyimpanan_memori: Mapped[int] = mapped_column()
    kapasitas_baterai: Mapped[int] = mapped_column()
    harga: Mapped[int] = mapped_column()
    berat: Mapped[int] = mapped_column()
    kualitas_hasil: Mapped[int] = mapped_column()
    
    def __repr__(self) -> str:
        return f"kamera(nama_kamera={self.nama_kamera!r}, penyimpanan_memori={self.penyimpanan_memori!r})"