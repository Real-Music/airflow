from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class AddressDTO(BaseModel):
    id: Optional[int]
    street: Optional[str]
    suite: Optional[str]
    city: Optional[str]
    zipcode: Optional[str]

    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]

    class Config:
        orm_mode = True


class AddressDTOs(BaseModel):
    __root__: Optional[List[AddressDTO]]

    class Config:
        orm_mode = True
