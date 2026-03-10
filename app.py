from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agentic_ai_system import run_agentic_ai
import uvicorn
import os

app = FastAPI(title="Agentic AI System", description="Multi-agent AI system with research capabilities")

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    task: str
    final_response: str
    research_data: dict
    messages: list

@app.post("/api/ask", response_model=TaskResponse)
async def ask_agent(request: TaskRequest):
    """Process a task through the agentic AI system"""
    try:
        result = run_agentic_ai(request.task)
        return TaskResponse(
            task=result["task"],
            final_response=result["final_response"],
            research_data=result["research_data"],
            messages=result["messages"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "agentic-ai-system"}

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main web interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agentic AI System</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            .input-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #555;
            }
            textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                resize: vertical;
                min-height: 100px;
            }
            button {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            button:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
            }
            .result {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 4px solid #667eea;
            }
            .loading {
                display: none;
                text-align: center;
                margin: 20px 0;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .agent-steps {
                background: #e8f4fd;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
            }
            .agent-steps h3 {
                margin-top: 0;
                color: #2c5282;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Agentic AI Research Assistant</h1>
            <p style="text-align: center; color: #666; margin-bottom: 30px;">
                Ask complex questions and watch multiple AI agents collaborate to provide comprehensive answers!
            </p>

            <div class="input-group">
                <label for="task">What would you like to research?</label>
                <textarea id="task" placeholder="e.g., What are the latest developments in quantum computing?"></textarea>
            </div>

            <div style="text-align: center;">
                <button id="submit-btn" onclick="askAgent()">🚀 Ask Agents</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Agents are researching your question...</p>
            </div>

            <div id="result" class="result" style="display: none;">
                <h2>📋 Final Answer</h2>
                <div id="final-answer"></div>

                <div id="agent-steps" class="agent-steps" style="display: none;">
                    <h3>🔄 Agent Activity</h3>
                    <div id="steps-content"></div>
                </div>
            </div>
        </div>

        <script>
            async function askAgent() {
                const task = document.getElementById('task').value.trim();
                if (!task) {
                    alert('Please enter a task!');
                    return;
                }

                const submitBtn = document.getElementById('submit-btn');
                const loading = document.getElementById('loading');
                const result = document.getElementById('result');

                submitBtn.disabled = true;
                submitBtn.textContent = 'Processing...';
                loading.style.display = 'block';
                result.style.display = 'none';

                try {
                    const response = await fetch('/api/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ task: task })
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();

                    document.getElementById('final-answer').innerHTML = data.final_response.replace(/\n/g, '<br>');

                    // Show agent steps
                    const stepsContent = data.messages.map(msg =>
                        `<div><strong>${msg.role}:</strong> ${msg.content}</div>`
                    ).join('');
                    document.getElementById('steps-content').innerHTML = stepsContent;
                    document.getElementById('agent-steps').style.display = 'block';

                    result.style.display = 'block';

                } catch (error) {
                    console.error('Error:', error);
                    alert('Error processing request: ' + error.message);
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = '🚀 Ask Agents';
                    loading.style.display = 'none';
                }
            }

            // Allow Enter key to submit
            document.getElementById('task').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    askAgent();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)