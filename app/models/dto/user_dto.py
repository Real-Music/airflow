from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.dto.address_dto import AddressDTO
from app.models.dto.company_dto import CompanyDTO


class UserDTO(BaseModel):
    id: Optional[int]
    name: Optional[str]
    username: Optional[str]
    email: Optional[str]

    address: Optional[List[AddressDTO]]
    company: Optional[List[CompanyDTO]]

    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]

    class Config:
        orm_mode = True


class UserDTOs(BaseModel):
    __root__: Optional[List[UserDTO]]

    class config:
        orm_mode = True
