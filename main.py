from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from langchain.schema import LLMResult
from langchain.llms.base import BaseLLM
from typing import Any, Dict, List, Optional, Union
from pydantic import Field

app = FastAPI(trust_proxy_headers=True)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OllamaLLM(BaseLLM):
    """Ollama 大语言模型的 LangChain 实现"""
    model_url: str = Field(default="http://localhost:11434/api/generate", description="Ollama模型的API地址")
    model_name: str = Field(default="deepseek-r1:14b", description="Ollama模型名称")

    @property
    def _llm_type(self) -> str:
        return "ollama"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        """调用Ollama模型"""
        try:
            response = self._generate_response(prompt)
            return response.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def _generate_response(self, prompt: str) -> str:
        import requests

        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model_name,  # 使用初始化时传入的模型名称
            "prompt": prompt,
            "stream": False,
            "options": {}
        }

        response = requests.post(self.model_url, json=data)
        if not response.ok:
            raise ValueError(f"Request to Ollama failed: {response.text}")

        return response.json()["response"]

    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None, **kwargs) -> LLMResult:
        """实现抽象方法 _generate"""
        responses = [self._call(prompt, stop=stop, **kwargs) for prompt in prompts]
        return LLMResult(generations=[{"text": response} for response in responses])


# 创建LangChain的LLM实例
llm = OllamaLLM()


@app.get("/ping")
async def ping():
    """测试API是否正常运行"""
    return {"status": "ok"}

@app.post("/generate")
async def generate(prompt: str):
    """生成LLM响应"""
    try:
        response = llm._call(prompt)
        return {"result": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)