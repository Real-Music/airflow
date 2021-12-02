from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class CompanyDTO(BaseModel):
    id: Optional[int]
    name: Optional[str]
    catchPhrase: Optional[str]
    bs: Optional[str]

    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]

    class Config:
        orm_mode = True


class CompanyDTOs(BaseModel):
    __root__: Optional[List[CompanyDTO]]

    class Config:
        orm_mode = True
