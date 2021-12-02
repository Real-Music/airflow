from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship, backref, Session

from app import Base_Model
from app.models.dto.user_dto import UserDTO
from app.utils.session import session_hook


class Users(Base_Model):
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50), nullable=False)
    username = Column(String(70), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    created_on = Column(DateTime, default=datetime.utcnow())
    updated_on = Column(DateTime, onupdate=datetime.utcnow())
    deleted_on = Column(DateTime, nullable=True)

    address = relationship(
        "Address",
        backref=backref(
            "user",
            lazy="joined",
            cascade="all, delete",
            single_parent=True,
            passive_deletes=True,
        ),
    )
    company = relationship(
        "Company",
        backref=backref(
            "user",
            lazy="joined",
            cascade="all, delete",
            single_parent=True,
            passive_deletes=True,
        ),
    )

    @staticmethod
    @session_hook
    def create(db: Session, user: dict) -> UserDTO:
        new_user = Users(**user)
        db.add(new_user)
        db.flush()

        return UserDTO.from_orm(new_user)
