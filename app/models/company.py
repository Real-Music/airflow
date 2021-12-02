from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import Session

from app import Base_Model
from app.models.dto.company_dto import CompanyDTO
from app.utils.session import session_hook


class Company(Base_Model):
    __tablename__: str = "company"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=True)
    catchPhrase = Column(String(150), nullable=True)
    bs = Column(String(200), nullable=True)

    created_on = Column(DateTime, default=datetime.utcnow())
    updated_on = Column(DateTime, onupdate=datetime.utcnow())
    deleted_on = Column(DateTime, nullable=True)

    @staticmethod
    @session_hook
    def create(db: Session, company: dict) -> CompanyDTO:
        new_company = Company(**company)
        db.add(new_company)
        db.flush()

        return CompanyDTO.from_orm(new_company)
