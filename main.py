import cloudscraper
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, Optional
import uvicorn

app = FastAPI(
    title="ScraperCookie",
    description="一个用于获取外部网站cookie的服务",
    version="0.1.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CookieResponse(BaseModel):
    cookies: Dict[str, str]


@app.get("/get-cookies", response_model=CookieResponse)
async def get_cookies(url: str = Query(..., description="要获取cookie的网站URL")):
    """
    获取指定URL的cookies
    """
    try:
        # 创建cloudscraper实例
        scraper = cloudscraper.create_scraper()
        
        # 发送请求获取cookies
        response = scraper.get(url)
        
        # 检查请求是否成功
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"请求失败: {response.status_code}")
        
        # 提取cookies
        cookies = {}
        for name, value in response.cookies.items():
            cookies[name] = value
        
        return {"cookies": cookies}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取cookies时出错: {str(e)}")


@app.get("/")
async def root():
    return {"message": "欢迎使用ScraperCookie API，访问 /docs 查看API文档"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)