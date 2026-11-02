from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlmodel import Session, select

try:
    from .maindb import create_db_and_tables, User, Team, engine
    from .agent_flow import process_chat_query, stream_chat_query
    from .app import sequence_agent
except ImportError:
    # Running directly: python main.py (from src/ directory)
    from maindb import create_db_and_tables, User, Team, engine
    from agent_flow import process_chat_query, stream_chat_query
    from app import sequence_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    user_id: int = 1
    history: list[dict] = []



from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return StreamingResponse(
        stream_chat_query(request.query, request.user_id, request.history),
        media_type="application/x-ndjson"
    )

@app.get("/chat")
async def chat_get_endpoint(query: str, user_id: int = 1):
    response = process_chat_query(query, user_id, [])
    return {"response": response}

@app.get("/")
async def main(query: str = None):
    if query:
        response = process_chat_query(query, 1)
        return {"response": response}
    
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        teams = session.exec(select(Team)).all()
        
        users_data = []
        for user in users:
            user_dict = user.model_dump()
            
            # Replace team_id with team name if available
            team_id = user_dict.pop("team_id", None)
            if user.team:
                user_dict["team"] = user.team.name
            
            users_data.append(user_dict)
            
        teams_data = [t.model_dump() for t in teams]
        
    raw_data_str = f"Users: {users_data} | Teams: {teams_data}"
    
    # Make the response conversational and friendly
    system_prompt = "You are a cheerful, friendly assistant. Describe the user and their teams data provided to you in a warm, conversational way. Keep it natural and engaging."
    friendly_response = sequence_agent.execute(raw_data_str, system_prompt=system_prompt)

    return {
        "response": friendly_response,
        "raw_data": {
            "users": users_data,
            "teams": teams_data
        }
    }

if __name__ == "__main__":
    module_str = "src.main:app" if __package__ else "main:app"
    uvicorn.run(module_str, host="127.0.0.1", port=8000, reload=True)
