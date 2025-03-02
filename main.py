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





# 读取 HTML 模板
def get_html_template():
    # 这里可以从文件读取 HTML，或者直接返回上面的 HTML 字符串
    # 为了简化示例，我们直接返回一个字符串变量
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScraperProxy API - 网页请求代理服务</title>
    <style>
        :root {
            --primary-color: #3498db;
            --secondary-color: #2980b9;
            --accent-color: #e74c3c;
            --text-color: #333;
            --light-bg: #f5f7fa;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: var(--card-shadow);
        }
        
        h1 {
            color: var(--primary-color);
            margin-bottom: 10px;
            font-size: 2.5rem;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 20px;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .feature-card {
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: var(--card-shadow);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-card h3 {
            color: var(--primary-color);
            margin-bottom: 15px;
            font-size: 1.4rem;
        }
        
        .code-section {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: var(--card-shadow);
            margin-bottom: 40px;
        }
        
        .code-block {
            background-color: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: 'Courier New', Courier, monospace;
            margin: 15px 0;
            white-space: pre-wrap;
        }
        
        .code-title {
            margin-bottom: 15px;
            color: var(--primary-color);
            font-size: 1.3rem;
        }
        
        .button {
            display: inline-block;
            background-color: var(--primary-color);
            color: white;
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s ease;
            margin: 10px 5px;
        }
        
        .button:hover {
            background-color: var(--secondary-color);
        }
        
        .button.accent {
            background-color: var(--accent-color);
        }
        
        .button.accent:hover {
            background-color: #c0392b;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
        }
        
        .try-it-section {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: var(--card-shadow);
            margin-bottom: 40px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        
        .input-group input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
        }
        
        .checkbox-group {
            margin: 15px 0;
        }
        
        #response-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 6px;
            min-height: 100px;
            margin-top: 20px;
            white-space: pre-wrap;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ScraperProxy API</h1>
            <p class="subtitle">强大的网页请求代理服务，轻松绕过访问限制</p>
            <div>
                <a href="/docs" class="button">API 文档</a>
                <a href="#try-it" class="button accent">立即尝试</a>
            </div>
        </header>
        
        <div class="features">
            <div class="feature-card">
                <h3>绕过访问限制</h3>
                <p>使用 cloudscraper 技术，轻松绕过常见的网站防护机制，如 Cloudflare 的反爬虫保护。</p>
            </div>
            <div class="feature-card">
                <h3>支持流式响应</h3>
                <p>通过流式响应处理大型数据，保持连接稳定，实现更高效的数据传输。</p>
            </div>
            <div class="feature-card">
                <h3>简单易用</h3>
                <p>简洁的 API 设计，只需一个 URL 参数即可使用，支持多种请求方法和自定义选项。</p>
            </div>
        </div>
        
        <div class="code-section">
            <h2 class="code-title">快速开始</h2>
            <p>使用我们的代理服务非常简单，只需发送请求到以下端点：</p>
            
            <div class="code-block">
# 基本用法
GET /proxy?url=https://example.com

# 启用流式响应
GET /proxy?url=https://example.com&stream=true

# 自定义请求方法和头信息
POST /proxy
{
    "url": "https://example.com",
    "method": "POST",
    "headers": {"Custom-Header": "Value"},
    "data": {"key": "value"},
    "stream": true
}
            </div>
        </div>
        
        <div class="try-it-section" id="try-it">
            <h2 class="code-title">立即尝试</h2>
            <div class="input-group">
                <label for="url-input">输入要请求的 URL:</label>
                <input type="text" id="url-input" placeholder="https://example.com" value="https://example.com">
            </div>
            
            <div class="checkbox-group">
                <input type="checkbox" id="stream-checkbox" checked>
                <label for="stream-checkbox">启用流式响应</label>
            </div>
            
            <button id="send-request" class="button">发送请求</button>
            
            <div id="response-container"></div>
        </div>
    </div>
    
    <footer>
        <p>&copy; 2025 ScraperProxy API. 所有权利保留。</p>
    </footer>
    
    <script>
        document.getElementById('send-request').addEventListener('click', async function() {
            const url = document.getElementById('url-input').value;
            const streamEnabled = document.getElementById('stream-checkbox').checked;
            const responseContainer = document.getElementById('response-container');
            
            if (!url) {
                alert('请输入有效的 URL');
                return;
            }
            
            responseContainer.style.display = 'block';
            responseContainer.textContent = '正在加载...';
            
            try {
                const proxyUrl = `/proxy?url=${encodeURIComponent(url)}&stream=${streamEnabled}`;
                
                if (streamEnabled) {
                    responseContainer.textContent = '';
                    const response = await fetch(proxyUrl);
                    const reader = response.body.getReader();
                    
                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) break;
                        const text = new TextDecoder().decode(value);
                        responseContainer.textContent += text;
                    }
                } else {
                    const response = await fetch(proxyUrl);
                    const data = await response.text();
                    responseContainer.textContent = data;
                }
            } catch (error) {
                responseContainer.textContent = `错误: ${error.message}`;
            }
        });
    </script>
</body>
</html>
    """
    return html_content


@app.get("/", response_class=HTMLResponse)
async def root():
    return get_html_template()

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
        # response = scraper.get('https://httpbin.org/ip')
        # print(response.text)

        # 获取home_url
        home_url = request.query_params.get("home")
        if not home_url:
            # 从target_url中提取home_url
            parsed_url = urlparse(target_url)
            home_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # 重试获取主页响应
        max_retries = 5
        retry_delay = 1  # 重试间隔秒数
        home_response = None
        
        for attempt in range(max_retries):
            try:
                home_response = scraper.get(home_url, headers={"sec-fetch-dest": "document"})
                print(f"主页{home_url}响应 (尝试 {attempt + 1}): {home_response.status_code}")
                
                if home_response.status_code == 200:
                    break
                    
                if attempt < max_retries - 1:  # 如果不是最后一次尝试
                    time.sleep(retry_delay)
                    
            except Exception as e:
                print(f"主页请求失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)

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
            "headers": {"sec-fetch-dest": "document"},
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
