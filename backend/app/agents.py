from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import TypedDict, Annotated
import operator
from app.config import settings

class AgentState(TypedDict):
    customer_id: int
    messages: Annotated[list, operator.add]
    goal: str
    context: dict
    recommendations: list
    actions: list

llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)

# Goal Understanding Agent
def goal_understanding_agent(state: AgentState):
    """Analyzes customer intent and identifies renewal needs"""
    prompt = ChatPromptTemplate.from_template(
        """Analyze the following customer message and identify their goal and intent.
        Return a clear understanding of what they need.
        
        Customer Message: {message}
        Customer ID: {customer_id}
        
        Provide:
        1. Primary Goal
        2. Sub-goals
        3. Urgency Level
        4. Required Actions"""
    )
    
    chain = prompt | llm
    message = state["messages"][-1] if state["messages"] else ""
    response = chain.invoke({
        "message": message,
        "customer_id": state["customer_id"]
    })
    
    return {
        "messages": [response.content],
        "goal": response.content,
        "context": {"agent": "goal_understanding"}
    }

# Customer Memory Agent
def customer_memory_agent(state: AgentState):
    """Maintains and retrieves customer profile and history"""
    prompt = ChatPromptTemplate.from_template(
        """Based on the customer ID and current context, provide relevant customer information.
        
        Customer ID: {customer_id}
        Current Goal: {goal}
        
        Retrieve:
        1. Customer Profile Summary
        2. Previous Interactions
        3. Policy History
        4. Preferences
        5. Important Notes"""
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "customer_id": state["customer_id"],
        "goal": state.get("goal", "")
    })
    
    return {
        "messages": [response.content],
        "context": {**state.get("context", {}), "customer_memory": response.content}
    }

# Policy Knowledge Agent
def policy_knowledge_agent(state: AgentState):
    """Retrieves and explains policy information"""
    prompt = ChatPromptTemplate.from_template(
        """Provide detailed policy information based on the customer's goal.
        
        Customer ID: {customer_id}
        Goal: {goal}
        Context: {context}
        
        Provide:
        1. Relevant Policy Details
        2. Coverage Information
        3. Terms and Conditions
        4. Renewal Options
        5. Alternative Coverage"""
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "customer_id": state["customer_id"],
        "goal": state.get("goal", ""),
        "context": str(state.get("context", {}))
    })
    
    return {
        "messages": [response.content],
        "context": {**state.get("context", {}), "policy_knowledge": response.content}
    }

# Recommendation Agent
def recommendation_agent(state: AgentState):
    """Generates renewal and coverage recommendations"""
    prompt = ChatPromptTemplate.from_template(
        """Based on the customer information and policy details, generate personalized recommendations.
        
        Customer ID: {customer_id}
        Goal: {goal}
        Policy Knowledge: {policy_knowledge}
        Customer Memory: {customer_memory}
        
        Generate:
        1. Renewal Recommendations (with rationale)
        2. Coverage Gap Analysis
        3. Cost Optimization Suggestions
        4. Alternative Options
        5. Priority Actions"""
    )
    
    chain = prompt | llm
    policy_knowledge = state.get("context", {}).get("policy_knowledge", "")
    customer_memory = state.get("context", {}).get("customer_memory", "")
    
    response = chain.invoke({
        "customer_id": state["customer_id"],
        "goal": state.get("goal", ""),
        "policy_knowledge": policy_knowledge,
        "customer_memory": customer_memory
    })
    
    return {
        "messages": [response.content],
        "recommendations": [response.content],
        "context": {**state.get("context", {}), "recommendations": response.content}
    }

# Notification Agent
def notification_agent(state: AgentState):
    """Creates notifications for actions and recommendations"""
    prompt = ChatPromptTemplate.from_template(
        """Based on the customer interactions and recommendations, create appropriate notifications.
        
        Customer ID: {customer_id}
        Recommendations: {recommendations}
        Recent Actions: {actions}
        
        Generate:
        1. Notification Title
        2. Notification Message
        3. Priority Level
        4. Delivery Method
        5. Follow-up Actions"""
    )
    
    chain = prompt | llm
    recommendations = state.get("recommendations", [])
    actions = state.get("actions", [])
    
    response = chain.invoke({
        "customer_id": state["customer_id"],
        "recommendations": str(recommendations),
        "actions": str(actions)
    })
    
    return {
        "messages": [response.content],
        "actions": [response.content]
    }

# Supervisor Agent
def supervisor_agent(state: AgentState):
    """Routes to appropriate agents and manages workflow"""
    prompt = ChatPromptTemplate.from_template(
        """You are a supervisor agent managing the policy renewal workflow.
        Based on the current state, determine the next best action.
        
        Customer ID: {customer_id}
        Messages: {messages}
        Goal: {goal}
        
        Determine:
        1. Next Agent to Call
        2. Information to Pass
        3. Priority Level
        4. Success Criteria"""
    )
    
    chain = prompt | llm
    messages_str = "\n".join(state.get("messages", []))
    
    response = chain.invoke({
        "customer_id": state["customer_id"],
        "messages": messages_str,
        "goal": state.get("goal", "")
    })
    
    return {
        "messages": [response.content],
        "context": {**state.get("context", {}), "supervisor": response.content}
    }

def create_workflow():
    """Creates the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("goal_understanding", goal_understanding_agent)
    workflow.add_node("customer_memory", customer_memory_agent)
    workflow.add_node("policy_knowledge", policy_knowledge_agent)
    workflow.add_node("recommendation", recommendation_agent)
    workflow.add_node("notification", notification_agent)
    workflow.add_node("supervisor", supervisor_agent)
    
    # Add edges
    workflow.add_edge(START, "supervisor")
    workflow.add_edge("goal_understanding", "customer_memory")
    workflow.add_edge("customer_memory", "policy_knowledge")
    workflow.add_edge("policy_knowledge", "recommendation")
    workflow.add_edge("recommendation", "notification")
    workflow.add_edge("supervisor", "goal_understanding")
    workflow.add_edge("notification", END)
    
    return workflow.compile()

agent_graph = create_workflow()
