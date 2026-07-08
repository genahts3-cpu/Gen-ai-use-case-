from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, Conversation, Message, Customer, User
from app.schemas import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse, ChatMessage, ChatResponse
from app.security import get_current_user
from app.agents import agent_graph
from app.services.rag import get_rag_context
from langchain_openai import ChatOpenAI
from app.config import settings

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)

@router.post("/", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new conversation"""
    customer = db.query(Customer).filter(
        Customer.id == conversation.customer_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer not found or access denied"
        )
    
    db_conversation = Conversation(
        customer_id=conversation.customer_id,
        title=conversation.title
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    
    return db_conversation

@router.get("/", response_model=List[ConversationResponse])
def list_conversations(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List conversations for current user"""
    conversations = db.query(Conversation).join(Customer).filter(
        Customer.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return conversations

@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get conversation by ID"""
    conversation = db.query(Conversation).join(Customer).filter(
        Conversation.id == conversation_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation

@router.post("/{conversation_id}/messages", response_model=ChatResponse)
async def send_message(
    conversation_id: int,
    chat_message: ChatMessage,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a message in a conversation"""
    conversation = db.query(Conversation).join(Customer).filter(
        Conversation.id == conversation_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Save user message
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=chat_message.message
    )
    db.add(user_msg)
    db.commit()
    
    # Get RAG context
    rag_context = get_rag_context(chat_message.message)
    context_text = rag_context.get("context", "")
    
    # Generate response using agent
    try:
        agent_state = {
            "customer_id": chat_message.user_id,
            "messages": [chat_message.message],
            "goal": chat_message.message,
            "context": {"rag_context": context_text},
            "recommendations": [],
            "actions": []
        }
        
        result = agent_graph.invoke(agent_state)
        response_text = result["messages"][-1] if result["messages"] else "I couldn't process your request."
    except Exception as e:
        response_text = f"I encountered an error processing your request: {str(e)}"
    
    # Save assistant message
    assistant_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=response_text
    )
    db.add(assistant_msg)
    db.commit()
    
    return ChatResponse(
        conversation_id=conversation_id,
        message=chat_message.message,
        response=response_text
    )

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get messages in a conversation"""
    conversation = db.query(Conversation).join(Customer).filter(
        Conversation.id == conversation_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).offset(skip).limit(limit).all()
    
    return messages

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a conversation"""
    conversation = db.query(Conversation).join(Customer).filter(
        Conversation.id == conversation_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    db.delete(conversation)
    db.commit()
    
    return {"message": "Conversation deleted successfully"}
