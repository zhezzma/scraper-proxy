# ScraperRequest

一个使用FastAPI和Cloudscraper的服务，用于获取代理外部网站

## 功能

- 接收网站URL作为输入
- 使用Cloudscraper绕过常见的反爬虫保护


## 技术栈

- FastAPI: 高性能的API框架
- Cloudscraper: 绕过Cloudflare等防护的爬虫工具
- uv: Python包管理工具
- Docker: 容器化部署

## 安装与运行


### 本地开发

```bash

# 初始化环境并指定版本
uv init ./

# 初始化环境并指定版本
uv init ./ --python=3.10.16

# 创建虚拟环境并指定版本
uv venv --python=3.10.16

# 创建虚拟环境并指定版本
uv venv 

# Windows 系统
.venv\Scripts\activate

# 安装依赖
uv sync 

# 生成锁文件
uv lock

# 在pyproject.tom中配置镜像
[tool.uv]
index-url = "https://mirrors.aliyun.com/pypi/simple/"

# 安装
uv add requests
uv add gradio==5.4.0

# 安装到dev组中,一般是tool之类的
uv add poethepoet --dev    

# 在pyproject.tom中添加命令脚本  poe freeze  | poe dev 
[tool.poe.tasks]
dev = "python main.py"
freeze =  { shell = "uv pip compile pyproject.toml -o requirements.txt" }

# 安装依赖
uv pip install -r requirements.txt

# 运行服务
python main.py
```

## API使用

```
请求 /proxy?url=https://example.com&stream=true
```
