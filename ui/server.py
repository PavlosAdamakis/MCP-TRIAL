from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from starlette.templating import Jinja2Templates
import shutil
import os

from mcp.protocol import FastMCP, Message
from agents.ops_agent import OpsAgent
from tools.shell import run_shell_tool
from tools.weather import run_weather_tool
from tools.store_data import run_store_data_tool
from tools.excel import run_excel_tool

app = FastAPI()
templates = Jinja2Templates(directory="ui/templates")

# Initialize MCP and tools
mcp = FastMCP()

tools = {
    "shell": run_shell_tool,
    "weather": run_weather_tool,
    "store_data": run_store_data_tool,
    "excel": run_excel_tool,
}

# Register OpsAgent
ops_agent = OpsAgent("OpsAgent", mcp, tools=tools)

# Register WebUser agent
class WebUser:
    def __init__(self, name, mcp):
        self.name = name
        self.mcp = mcp
        self.response = ""
        self.response_html = ""
        mcp.register(self)

    def receive(self, message):
        self.response = message.content.get("result", "No result returned.")
        self.response_html = message.content.get("html", "")

user = WebUser("WebUser", mcp)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": "",
        "response_html": "",
        "file_ready": False
    })

@app.post("/", response_class=HTMLResponse)
def handle_command(
    request: Request,
    tool: str = Form(...),
    command: str = Form(...),
    file: UploadFile = File(None)
):
    filepath = None

    if tool in ["store_data", "excel"] and file and file.filename:
        filepath = f"uploaded_{file.filename}"
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    msg = Message(
        sender="WebUser",
        receiver="OpsAgent",
        performative="run_tool",
        content={
            "tool": tool,
            "input": {
                "command": command,
                "text": command,
                "filepath": filepath,
                "instructions": command,
                "city": command if tool == "weather" else None
            }
        }
    )
    mcp.dispatch(msg)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": user.response,
        "response_html": user.response_html,
        "file_ready": (tool == "excel")
    })

@app.get("/download")
def download_file():
    filepath = "cleaned_data.xlsx"
    if os.path.exists(filepath):
        return FileResponse(filepath, filename="cleaned_data.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return {"error": "File not found."}
