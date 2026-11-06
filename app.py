import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print(BASE_DIR)
print(BASE_DIR / "static")



from prompts import (
    system_promptsAnalizer,
    system_promptsImplementer,
    system_analizer,
    system_implementer,
    system_evaluator,
    system_reimplementer
)

from config import *

from openai import AzureOpenAI

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

print("ENDPOINT =", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("DEPLOYMENT =", os.getenv("AZURE_OPENAI_DEPLOYMENT"))

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2025-04-01-preview"
)

DEPLOYMENT_NAME = AZURE_OPENAI_DEPLOYMENT

def reply(system, prompt):

    try:

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role":"system",
                    "content":system
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        print("GPT ERROR")
        print(e)

        return "模型回應被 Azure 安全政策攔截"


def developer(prompt):

    # Prompts Analize
    promptsAnalizer_prompt = f"這是一段用於生成圖片的原始指令/描述：\n{prompt}\n\n幫我過濾雜訊並進行結構化資訊萃取"
    promptsAnalizer_output = reply(
        system=system_promptsAnalizer,
        prompt=promptsAnalizer_prompt,
        )

    # Prompts Implement
    promptsImplementer_prompt = f"這是針對一張圖片的分析：\n{promptsAnalizer_output}\n\n提供我適合用於 PixAI 的英文提示詞，並推薦 LoRA 模型。"
    promptsImplementer_output = reply(
        system=system_promptsImplementer,
        prompt=promptsImplementer_prompt,
        )

    # Analize
    analize_prompt = f"這是一段用於生成圖片的原始指令/描述：\n{promptsImplementer_output}\n\n幫我過濾雜訊並進行結構化資訊萃取。"
    analizer_output = reply(
        system=system_analizer,
        prompt=analize_prompt,
        )

    # Implement
    implement_prompt = f"這是針對一張圖片的描述：\n{analizer_output}\n\n將圖片描述改寫為極具情緒渲染力與畫面感的主持人介紹文。"
    implementer_output = reply(
        system=system_implementer,
        prompt=implement_prompt,
        )

    # Evaluate
    evaluate_prompt = f"這是我剛剛寫的圖片介紹貼文：\n{implementer_output}\n\n提供修改建議，以條列式呈現。"
    evaluator_output = reply(
        system=system_evaluator,
        prompt=evaluate_prompt,
        )

    # Re-Implement
    reimplement_prompt = f"這是我剛剛寫的圖片介紹貼文：\n{implementer_output}\n\n這是修改建議：\n{evaluator_output}\n\n根據這些建議，將文章修改得更生活化。必須使用台灣習慣的中文，只需要輸出修改後的文章。"
    reimplementer_output = reply(
        system=system_reimplementer,
        prompt=reimplement_prompt,
        )

    return promptsAnalizer_output, promptsImplementer_output, analizer_output, implementer_output, evaluator_output, reimplementer_output

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):

    (
        promptsAnalizer_output,
        promptsImplementer_output,
        analizer_output,
        implementer_output,
        evaluator_output,
        reimplementer_output
    ) = developer(req.message)

    return {
        "promptAnalyze": promptsAnalizer_output,
        "pixPrompt": promptsImplementer_output,
        "imageAnalyze": analizer_output,
        "draft": implementer_output,
        "suggestions": evaluator_output,
        "final": reimplementer_output
    }

@app.get("/", response_class=HTMLResponse)
async def home():

    with open(
        "templates/index.html",
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()