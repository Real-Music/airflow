from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import Session

from app import Base_Model
from app.models.dto.address_dto import AddressDTO
from app.utils.session import session_hook


class Address(Base_Model):
    __tablename__: str = "address"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    street = Column(String(100), nullable=True)
    suite = Column(String(100), nullable=True)
    city = Column(String(150), nullable=True)
    zipcode = Column(String(150), nullable=True)

    created_on = Column(DateTime, default=datetime.utcnow())
    updated_on = Column(DateTime, onupdate=datetime.utcnow())
    deleted_on = Column(DateTime, nullable=True)

    @staticmethod
    @session_hook
    def create(db: Session, address: dict) -> AddressDTO:
        new_address = Address(**address)
        db.add(new_address)
        db.flush()

        return AddressDTO.from_orm(new_address)
