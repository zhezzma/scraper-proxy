FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装uv
RUN pip install uv

# 复制项目文件
COPY . /app/

# 使用uv安装依赖
RUN uv pip install -r requirements.txt

# 暴露端口
EXPOSE 7860

# 启动服务
CMD ["python", "main.py"]