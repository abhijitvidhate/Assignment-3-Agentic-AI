# 🤖 Agentic AI System - End-to-End Implementation

A complete multi-agent AI system built with LangGraph, featuring research capabilities, web search, and intelligent task coordination.

## 🚀 Features

- **Multi-Agent Architecture**: Planner, Search, Wikipedia, and Synthesizer agents
- **Intelligent Routing**: Dynamic task analysis and agent coordination
- **Web Research**: DuckDuckGo search and Wikipedia integration
- **Web Interface**: Modern UI for easy interaction
- **Containerized**: Docker deployment ready
- **Scalable**: Built with FastAPI for production use

## 🏗️ Architecture

```
User Query → Planner Agent → Research Agents → Synthesizer → Final Response
                      ↓
               Search Agent ←→ Wikipedia Agent
```

## 📋 Prerequisites

- Python 3.13+
- Docker & Docker Compose
- OpenAI API Key

## 🛠️ Local Development Setup

### 1. Clone and Setup Environment

```bash
cd "/home/abhijit/ML-Ops-Assignement/Assignment-3/Agentic AI/LangGraph-Course-freeCodeCamp"
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run Locally

```bash
python app.py
```

Visit: http://localhost:8000

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
# Build the image
docker-compose build

# Run the service
docker-compose up -d

# Check logs
docker-compose logs -f agentic-ai

# Stop the service
docker-compose down
```

### Manual Docker Commands

```bash
# Build image
docker build -t agentic-ai .

# Run container
docker run -p 8000:8000 --env-file .env agentic-ai
```

## 🧪 Testing the System

### Health Check
```bash
curl http://localhost:8000/health
```

### API Test
```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{"task": "What are the benefits of renewable energy?"}'
```

### Example Queries to Test

1. **Simple Question**: "What is machine learning?"
2. **Research Task**: "Latest developments in quantum computing"
3. **Complex Analysis**: "Compare renewable energy sources"
4. **Current Events**: "Recent advancements in AI"

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `PORT` | Server port | 8000 |
| `HOST` | Server host | 0.0.0.0 |

### Optional Monitoring

Add to `.env` for LangSmith tracing:
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=agentic-ai-demo
```

## 📊 Agent Workflow

1. **Planner Agent**: Analyzes the task and determines research needs
2. **Search Agent**: Performs web search using DuckDuckGo
3. **Wikipedia Agent**: Gathers detailed information from Wikipedia
4. **Synthesizer Agent**: Combines all information into a coherent response

## 🎯 Demo Scenarios

### For Assignment Presentation:

1. **Show the Web Interface**: Demonstrate the user-friendly UI
2. **Live Agent Coordination**: Ask a complex question and show agent activity
3. **Architecture Explanation**: Walk through the multi-agent workflow
4. **Scalability Discussion**: Explain how more agents can be added

### Technical Deep Dive:

1. **Graph Visualization**: Show the LangGraph structure
2. **State Management**: Explain how data flows between agents
3. **Error Handling**: Demonstrate robustness
4. **Performance**: Discuss response times and optimization

## 🚀 Production Deployment

### Using Docker Compose (Recommended)

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# Scale if needed
docker-compose up -d --scale agentic-ai=3
```

### Behind Reverse Proxy (nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔍 Monitoring & Troubleshooting

### Logs
```bash
# Application logs
docker-compose logs -f agentic-ai

# System resource usage
docker stats
```

### Common Issues

1. **API Key Missing**: Check `.env` file
2. **Port Already in Use**: Change port in docker-compose.yml
3. **Memory Issues**: Increase Docker memory limit
4. **Rate Limits**: OpenAI API rate limits reached

## 📈 Performance Optimization

- **Caching**: Add Redis for response caching
- **Async Processing**: Implement background task processing
- **Load Balancing**: Deploy multiple instances
- **Database**: Add persistent storage for conversation history

## 🎓 Learning Outcomes

This implementation demonstrates:
- Multi-agent system design
- Graph-based workflow orchestration
- API integration and tool usage
- Containerization and deployment
- Web application development
- Production-ready architecture
