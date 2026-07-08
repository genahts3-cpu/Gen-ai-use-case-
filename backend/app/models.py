from pydantic import BaseModel, Field
from typing import List, Optional


class UseCase(BaseModel):
    id: str
    title: str
    description: str
    industry: str
    business_value: str
    tags: List[str] = Field(default_factory=list)
    status: str = "draft"


class UseCaseCreate(BaseModel):
    title: str
    description: str
    industry: str
    business_value: str
    tags: Optional[List[str]] = None
    status: Optional[str] = "draft"


class UseCaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    business_value: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
