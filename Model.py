from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///db/database.db", echo=False)

Base = declarative_base()


# Models
class Device(Base):
    __tablename__ = "device"
    # id:int, device_name:str, vacant:bool
    id = Column(Integer, primary_key=True)
    device_name = Column(String(20))
    vacant = Column(Boolean)

    def __repr__(self) -> str:
        return "<Device(id='%s', device_name='%s', vacant='%s')>" % (
            self.id,
            self.device_name,
            self.vacant,
        )


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    device_id = Column(Integer, ForeignKey("device.id"))


class Pulse(Base):
    __tablename__ = "pulse"
    id = Column(Integer, primary_key=True)
    from_device = Column(Integer, ForeignKey("device.id"))
    reading = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)


class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True)
    from_device = Column(Integer, ForeignKey("device.id"))
    reading = Column(Float)
    created_at = Column(DateTime, default=datetime.now)


class SPO2(Base):
    __tablename__ = "spo2"
    id = Column(Integer, primary_key=True)
    from_device = Column(Integer, ForeignKey("device.id"))
    reading = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)


# relationships
# Device.pulse = relationship("Pulse", order_by=Pulse.id, back_populates="pulse")
# Device.temperature = relationship(
#     "Temperature", order_by=Temperature.id, back_populates="temperature"
# )

# create_all() saves table in SQLite format
Base.metadata.create_all(engine)

# Creating session
# it communicate with db, SQL operations
Session = sessionmaker(bind=engine)
session = Session()
