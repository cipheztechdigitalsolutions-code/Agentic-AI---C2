import asyncio, os, gradio as gr
from dotenv import load_dotenv
load_dotenv(override=True)

os.environ["OPENAI_API_KEY"] = os.getenv("API_TOKEN")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

server = MCPServerStreamableHttp(
    name="Demo Server",
    params={"url": "http://localhost:8000/mcp"}
)

async def ask(message, history):

    async with server:

        agent = Agent(
            name="Assistant",
            instructions="Use tools from the mcp server when needed",
            model="gpt-4o-mini",
            mcp_servers=[server]
        )

        result = await Runner.run(agent, message)

        return result.final_output


def respond(message, history):
    return asyncio.run(ask(message, history))


gr.ChatInterface(fn=respond, title="MCP Demo Chat").launch()