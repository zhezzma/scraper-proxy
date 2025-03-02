import os
import cloudscraper
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from typing import Optional
import uvicorn
import asyncio
from urllib.parse import urlparse
import time
from curl_cffi import requests 
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

app = FastAPI(
    title="ScraperProxy",
    description="一个使用CloudScraper进行请求转发的代理，支持流式响应",
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

async def stream_generator(response):
    """生成流式响应的生成器函数"""
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            yield chunk
            await asyncio.sleep(0.001)  # 让出控制权，保持异步特性

# 获取环境变量中的请求库选择
REQUEST_LIB = os.environ.get('REQUEST_LIB', 'cloudscraper').lower()

async def make_request(method: str, **kwargs):
    """统一的请求处理函数"""
    if REQUEST_LIB == 'cloudscraper':
        scraper = cloudscraper.create_scraper(delay=10)
        
        # 设置代理
        proxy = os.environ.get('PROXY')
        if proxy:
            scraper.proxies = {
                'http': proxy,
                'https': proxy
            }
            
        # 根据方法发送请求
        return getattr(scraper, method.lower())(**kwargs)
    else:
        # 使用 curl_cffi
        proxy = os.environ.get('PROXY')
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        
        # curl_cffi 的请求配置
        request_config = {
            **kwargs,
            'proxies': proxies,
            'impersonate': 'chrome110',
        }
        
        return requests.request(method, **request_config)

@app.get("/", response_class=HTMLResponse)
async def root():
    """返回index.html的内容"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Welcome to Scraper Proxy!"

@app.api_route("/proxy", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy(request: Request):
    """
    通用代理端点，转发所有请求到目标URL，支持流式响应
    """
    try:
        # 获取环境变量中的token
        env_token = os.environ.get('TOKEN')
        if env_token:
            # 从请求头获取Authorization
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                raise HTTPException(
                    status_code=401,
                    detail="未提供有效的Authorization header",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            # 提取Bearer token
            token = auth_header.split(' ')[1]
            # 验证token
            if token != env_token:
                raise HTTPException(
                    status_code=403,
                    detail="Token无效"
                )

        # 获取target_url
        target_url = request.query_params.get("url")
        if not target_url:
            raise HTTPException(status_code=400, detail="必须提供目标URL")
        
        # 获取home_url
        home_url = request.query_params.get("home")
        if not home_url:
            # 从target_url中提取home_url
            parsed_url = urlparse(target_url)
            home_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        
        # 检查是否请求流式响应
        stream_request = "stream" in request.query_params and request.query_params["stream"].lower() in ["true", "1", "yes"]
        
        # 获取请求体
        body = await request.body()
        
        # 获取查询参数
        params = dict(request.query_params)
        # 从查询参数中移除url和stream参数
        params.pop("url", None)
        params.pop("stream", None)
        
        # 获取原始请求头
        headers = dict(request.headers)
        # 移除可能导致问题的头
        headers.pop("host", None)
        headers.pop("authorization", None) 
        headers.pop("x-forwarded-for", None)
        headers.pop("x-forwarded-proto", None)
        headers.pop("x-forwarded-port", None)
        headers.pop("x-amzn-trace-id", None)
        headers.pop("x-request-id", None)
        headers.pop("x-ip-token", None)
        headers.pop("x-direct-url", None)
        headers.pop("x-direct-url", None)
        print(f"{headers}")
        
        # 构建请求参数
        request_kwargs = {
            "url": target_url,
            "headers": headers,
            "params": params,
            "stream": stream_request  # 设置stream参数
        }
        
        # 如果有请求体，添加到请求参数中
        if body:
            request_kwargs["data"] = body
            
        # 使用统一的请求函数发送请求
        response = await make_request(request.method, **request_kwargs)
        
        # 处理流式响应
        if stream_request:
            # 创建响应头字典
            headers_dict = {}
            for header_name, header_value in response.headers.items():
                if header_name.lower() not in ('content-encoding', 'transfer-encoding', 'content-length'):
                    headers_dict[header_name] = header_value
            
            # 返回流式响应
            return StreamingResponse(
                stream_generator(response),
                status_code=response.status_code,
                headers=headers_dict,
                media_type=response.headers.get("content-type", "application/octet-stream")
            )
        else:
            # 创建普通响应
            proxy_response = Response(
                content=response.content,
                status_code=response.status_code,
            )
            
            # 转发响应头
            for header_name, header_value in response.headers.items():
                if header_name.lower() not in ('content-encoding', 'transfer-encoding', 'content-length'):
                    proxy_response.headers[header_name] = header_value
                    
            # 转发cookies
            for cookie_name, cookie_value in response.cookies.items():
                proxy_response.set_cookie(key=cookie_name, value=cookie_value)
                
            return proxy_response
        
    except Exception as e:
        error = f"代理请求失败: {str(e)}"
        print(error)
        raise HTTPException(status_code=500, detail=error)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)
