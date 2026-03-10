#!/bin/bash

# Agentic AI System - Local Deployment Script

echo "🤖 Agentic AI System - Local Deployment"
echo "======================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Please copy .env.example to .env and add your OpenAI API key"
    echo "   cp .env.example .env"
    echo "   # Then edit .env and add: OPENAI_API_KEY=your_key_here"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "⚠️  Warning: OPENAI_API_KEY not found in .env file"
    echo "   Please add your OpenAI API key to continue"
    echo "   The system will still start but agents requiring API calls will fail"
fi

echo "✅ Environment check passed"

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source .venv/bin/activate

# Test the system
echo "🧪 Testing agentic AI system..."
python -c "
try:
    from agentic_ai_system import run_agentic_ai
    print('✅ Imports successful')
    print('🚀 Agentic AI system ready!')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Start the server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📱 Open your browser and visit: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python app.py