# 使用官方 Python 运行时作为父镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 修改 pip / uv 镜像源（国内加速）
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV UV_NO_CACHE=1

# 安装 uv
RUN pip install --no-cache-dir uv

# 复制全部
COPY . .

# 同步依赖
RUN uv sync

# 暴露端口
EXPOSE 8210

# 推荐使用这种方式启动
CMD ["uv", "run", "python", "main.py"]