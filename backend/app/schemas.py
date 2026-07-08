from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

class CustomerCreate(CustomerBase):
    user_id: int

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Policy Schemas
class PolicyBase(BaseModel):
    policy_number: str
    policy_type: str
    coverage_amount: float
    premium: float
    start_date: str
    end_date: str
    terms: str

class PolicyCreate(PolicyBase):
    customer_id: int

class PolicyUpdate(BaseModel):
    coverage_amount: Optional[float] = None
    premium: Optional[float] = None
    terms: Optional[str] = None
    status: Optional[str] = None

class PolicyResponse(PolicyBase):
    id: int
    customer_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Renewal Schemas
class RenewalBase(BaseModel):
    renewal_date: str
    new_premium: float
    recommended_coverage: float
    reason: str

class RenewalCreate(RenewalBase):
    customer_id: int
    policy_id: int

class RenewalUpdate(BaseModel):
    status: Optional[str] = None
    new_premium: Optional[float] = None

class RenewalResponse(RenewalBase):
    id: int
    customer_id: int
    policy_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Claim Schemas
class ClaimBase(BaseModel):
    claim_amount: float
    claim_date: str
    description: str

class ClaimCreate(ClaimBase):
    policy_id: int

class ClaimResponse(ClaimBase):
    id: int
    policy_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Conversation Schemas
class MessageCreate(BaseModel):
    role: str
    content: str

class MessageResponse(MessageCreate):
    id: int
    conversation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    customer_id: int
    title: str

class ConversationResponse(BaseModel):
    id: int
    customer_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True

# Recommendation Schemas
class RecommendationBase(BaseModel):
    title: str
    description: str
    recommendation_type: str
    priority: str

class RecommendationCreate(RecommendationBase):
    customer_id: int

class RecommendationUpdate(BaseModel):
    status: Optional[str] = None

class RecommendationResponse(RecommendationBase):
    id: int
    customer_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Notification Schemas
class NotificationCreate(BaseModel):
    customer_id: int
    title: str
    message: str
    notification_type: str

class NotificationUpdate(BaseModel):
    is_read: bool

class NotificationResponse(BaseModel):
    id: int
    customer_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Document Schemas
class DocumentCreate(BaseModel):
    filename: str
    file_path: str
    document_type: str
    content: str

class DocumentResponse(DocumentCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Chat Message Schemas
class ChatMessage(BaseModel):
    user_id: int
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    message: str
    response: str
    
# Health Check
class HealthResponse(BaseModel):
    status: str
    message: str
