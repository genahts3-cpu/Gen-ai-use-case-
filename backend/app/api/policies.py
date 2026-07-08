from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, Policy, Renewal, Customer, User
from app.schemas import PolicyCreate, PolicyResponse, PolicyUpdate, RenewalCreate, RenewalResponse, RenewalUpdate
from app.security import get_current_user

router = APIRouter(prefix="/api", tags=["policies", "renewals"])

# Policy Endpoints
@router.post("/policies", response_model=PolicyResponse)
def create_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new policy"""
    customer = db.query(Customer).filter(
        Customer.id == policy.customer_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer not found or access denied"
        )
    
    db_policy = Policy(**policy.dict())
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    
    return db_policy

@router.get("/policies", response_model=List[PolicyResponse])
def list_policies(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all policies for current user's customers"""
    policies = db.query(Policy).join(Customer).filter(
        Customer.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return policies

@router.get("/policies/{policy_id}", response_model=PolicyResponse)
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get policy by ID"""
    policy = db.query(Policy).join(Customer).filter(
        Policy.id == policy_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    return policy

@router.put("/policies/{policy_id}", response_model=PolicyResponse)
def update_policy(
    policy_id: int,
    policy_update: PolicyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update policy"""
    policy = db.query(Policy).join(Customer).filter(
        Policy.id == policy_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    update_data = policy_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(policy, field, value)
    
    db.commit()
    db.refresh(policy)
    
    return policy

@router.delete("/policies/{policy_id}")
def delete_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete policy"""
    policy = db.query(Policy).join(Customer).filter(
        Policy.id == policy_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    db.delete(policy)
    db.commit()
    
    return {"message": "Policy deleted successfully"}

# Renewal Endpoints
@router.post("/renewals", response_model=RenewalResponse)
def create_renewal(
    renewal: RenewalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new renewal"""
    policy = db.query(Policy).join(Customer).filter(
        Policy.id == renewal.policy_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Policy not found or access denied"
        )
    
    db_renewal = Renewal(**renewal.dict())
    db.add(db_renewal)
    db.commit()
    db.refresh(db_renewal)
    
    return db_renewal

@router.get("/renewals", response_model=List[RenewalResponse])
def list_renewals(
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List renewals for current user"""
    query = db.query(Renewal).join(Policy).join(Customer).filter(
        Customer.user_id == current_user.id
    )
    
    if status:
        query = query.filter(Renewal.status == status)
    
    renewals = query.offset(skip).limit(limit).all()
    
    return renewals

@router.get("/renewals/{renewal_id}", response_model=RenewalResponse)
def get_renewal(
    renewal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get renewal by ID"""
    renewal = db.query(Renewal).join(Policy).join(Customer).filter(
        Renewal.id == renewal_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not renewal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Renewal not found"
        )
    
    return renewal

@router.put("/renewals/{renewal_id}", response_model=RenewalResponse)
def update_renewal(
    renewal_id: int,
    renewal_update: RenewalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update renewal"""
    renewal = db.query(Renewal).join(Policy).join(Customer).filter(
        Renewal.id == renewal_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not renewal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Renewal not found"
        )
    
    update_data = renewal_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(renewal, field, value)
    
    db.commit()
    db.refresh(renewal)
    
    return renewal

@router.delete("/renewals/{renewal_id}")
def delete_renewal(
    renewal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete renewal"""
    renewal = db.query(Renewal).join(Policy).join(Customer).filter(
        Renewal.id == renewal_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not renewal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Renewal not found"
        )
    
    db.delete(renewal)
    db.commit()
    
    return {"message": "Renewal deleted successfully"}
