# Policy Renewal Agent

## Overview

A fully functional agentic AI platform for insurance policy renewal using LangGraph, FastAPI, React, and ChromaDB.

## Features

- **Intelligent Agents**: LangGraph-based agents for goal understanding, customer memory, policy knowledge, recommendations, and notifications
- **RAG System**: PDF document ingestion with ChromaDB embeddings
- **Customer Portal**: Beautiful React frontend with policy management
- **Admin Dashboard**: System monitoring and customer management
- **Chat Interface**: Real-time AI-powered customer conversations
- **Automated Renewals**: Intelligent policy renewal recommendations
- **Notification System**: Automated email and in-app notifications

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- LangGraph & LangChain
- SQLAlchemy with SQLite
- ChromaDB
- Pydantic
- OpenAI GPT-4 Turbo

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Axios

### Deployment
- Docker & Docker Compose
- SQLite Database
- ChromaDB Vector Store

## Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key (or Azure OpenAI)

### Installation & Running

```bash
# Clone repository
git clone https://github.com/genahts3-cpu/Gen-ai-use-case-.git
cd Gen-ai-use-case-

# Create .env file
cp .env.example .env
# Edit .env with your OpenAI API key

# Start application
docker compose up --build
```

Application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
policy-renewal-agent/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── agents/      # LangGraph agents
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   ├── database.py  # Database setup
│   │   └── main.py      # FastAPI app
│   ├── tests/           # Unit & integration tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├��─ pages/       # Page components
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # API client
│   │   └── App.tsx
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## API Documentation

### Authentication
- `POST /api/auth/login` - Customer login
- `POST /api/auth/register` - Customer registration
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Current user

### Customer
- `GET /api/customers/{id}` - Get customer profile
- `PUT /api/customers/{id}` - Update customer
- `GET /api/customers/{id}/policies` - List customer policies

### Policies
- `GET /api/policies` - List all policies
- `GET /api/policies/{id}` - Get policy details
- `POST /api/policies` - Create policy
- `PUT /api/policies/{id}` - Update policy

### Renewals
- `GET /api/renewals` - List renewals
- `GET /api/renewals/{id}` - Get renewal details
- `POST /api/renewals/{id}/process` - Process renewal
- `POST /api/renewals/{id}/approve` - Approve renewal

### Recommendations
- `GET /api/recommendations/{customer_id}` - Get recommendations
- `POST /api/recommendations/generate` - Generate new recommendation

### Chat
- `POST /api/chat/message` - Send chat message
- `GET /api/conversations/{id}` - Get conversation history
- `POST /api/conversations` - Create conversation

### Knowledge
- `POST /api/knowledge/upload` - Upload PDF document
- `GET /api/knowledge/search` - Search documents

### Notifications
- `GET /api/notifications` - List notifications
- `PUT /api/notifications/{id}/read` - Mark as read
- `DELETE /api/notifications/{id}` - Delete notification

### Admin
- `GET /api/admin/health` - System health check
- `GET /api/admin/stats` - System statistics
- `GET /api/admin/audit-logs` - Audit logs

## Database Schema

### Tables
- **User**: System users and admins
- **Customer**: Insurance customers
- **Policy**: Insurance policies
- **Renewal**: Policy renewal records
- **Claim**: Insurance claims
- **Conversation**: Chat conversations
- **Message**: Chat messages
- **Recommendation**: AI recommendations
- **Notification**: System notifications
- **AuditLog**: System activity logs
- **Document**: Uploaded policy documents

## Agent Architecture

### Supervisor Agent
- Routes customer requests to appropriate agents
- Manages workflow orchestration
- Handles error recovery

### Goal Understanding Agent
- Analyzes customer intent
- Identifies renewal needs
- Determines action priority

### Customer Memory Agent
- Maintains customer profile
- Tracks interaction history
- Manages preferences

### Policy Knowledge Agent
- Retrieves policy documents
- Answers policy questions
- Provides coverage details

### Recommendation Agent
- Generates renewal recommendations
- Analyzes coverage gaps
- Suggests improvements

### Notification Agent
- Creates notifications
- Schedules messages
- Tracks delivery status

## Testing

```bash
# Run all tests
docker compose run backend pytest

# Run specific test file
docker compose run backend pytest tests/test_api.py

# Run with coverage
docker compose run backend pytest --cov=app tests/
```

## Development

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install

# Run backend locally
cd backend
uvicorn app.main:app --reload

# Run frontend locally
cd frontend
npm run dev
```

## Docker Compose

The application uses Docker Compose with the following services:

- **frontend**: React application
- **backend**: FastAPI server
- **chroma**: ChromaDB vector database
- **db**: SQLite (handled by backend)

## Environment Variables

See `.env.example` for all available configuration options.

## Contributing

Contributions welcome! Please ensure:
- All tests pass
- No linting errors
- TypeScript types are correct
- Python code follows PEP 8

## License

MIT
