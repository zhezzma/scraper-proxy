import os
import cloudscraper
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Optional
import uvicorn
import asyncio

app = FastAPI(
    title="ScraperCookie",
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

@app.get("/")
async def root():
    return {"message": "欢迎使用ScraperProxy API，访问 /docs 查看API文档"}

@app.api_route("/proxy", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy(request: Request):
    """
    通用代理端点，转发所有请求到目标URL，支持流式响应
    """
    try:
        # 获取请求方法
        method = request.method
        
        target_url = request.query_params.get("url")
        if not target_url:
            raise HTTPException(status_code=400, detail="必须提供目标URL")
        
        # 检查是否请求流式响应
        stream_request = "stream" in request.query_params and request.query_params["stream"].lower() in ["true", "1", "yes"]
        
        # 创建带有代理的 scraper
        # 创建cloudscraper实例
        scraper = cloudscraper.create_scraper()
        
        # 从请求中获取cookies并设置到scraper
        cookies = request.cookies
        for key, value in cookies.items():
            scraper.cookies.set(key, value)
            
        # 检查环境变量PROXY是否存在
        proxy = os.environ.get('PROXY')
        if proxy:
            # 如果环境变量存在，则设置代理
            scraper.proxies = {
                'http': proxy,
                'https': proxy
            }
        # 测试代理是否生效
        response = scraper.get('https://httpbin.org/ip')
        print(response.text)


            
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
        headers.pop("cookie", None)
        headers.pop("x-forwarded-for", None)
        headers.pop("x-forwarded-proto", None)
        headers.pop("x-forwarded-port", None)
        headers.pop("x-amzn-trace-id", None)
        headers.pop("x-request-id", None)
        headers.pop("x-ip-token", None)
        headers.pop("x-direct-url", None)
        headers.pop("x-direct-url", None)
        headers.pop("accept", None)
        headers.pop("accept-language", None)
        headers.pop("accept-encoding", None)
        headers.pop("content-type", None)
        headers.pop("content-length", None)
        headers.pop("user-agent", None)
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
        
        # 发送请求
        if method == "GET":
            response = scraper.get(**request_kwargs)
        elif method == "POST":
            response = scraper.post(**request_kwargs)
        elif method == "PUT":
            response = scraper.put(**request_kwargs)
        elif method == "DELETE":
            response = scraper.delete(**request_kwargs)
        elif method == "HEAD":
            response = scraper.head(**request_kwargs)
        elif method == "OPTIONS":
            response = scraper.options(**request_kwargs)
        elif method == "PATCH":
            response = scraper.patch(**request_kwargs)
        else:
            raise HTTPException(status_code=405, detail=f"不支持的方法: {method}")
        
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
        raise HTTPException(status_code=500, detail=f"代理请求失败: {str(e)}")



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)
