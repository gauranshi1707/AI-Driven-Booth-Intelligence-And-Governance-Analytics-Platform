from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Booth(Base):
    __tablename__ = "booths"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ward = Column(String)

    streets = relationship("Street", back_populates="booth")


class Street(Base):
    __tablename__ = "streets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    booth_id = Column(Integer, ForeignKey("booths.id"))

    booth = relationship("Booth", back_populates="streets")
    citizens = relationship("Citizen", back_populates="street")


class Citizen(Base):
    __tablename__ = "citizens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    mobile = Column(String)
    occupation = Column(String)
    consent = Column(Boolean, default=True)
    segment = Column(String)

    street_id = Column(Integer, ForeignKey("streets.id"))
    street = relationship("Street", back_populates="citizens")
class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizens.id"))
    scheme_id = Column(Integer, ForeignKey("schemes.id"))
class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    category = Column(String)
    status = Column(String, default="Open")
    street_id = Column(Integer, ForeignKey("streets.id"))
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    street_id = Column(Integer, ForeignKey("streets.id"))
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    role = Column(String)  # admin / volunteer / analyst