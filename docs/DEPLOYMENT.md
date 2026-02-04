# What Format 部署指南

## 1. 本地开发环境部署

### 1.1 快速启动

```bash
# 1. 克隆/进入项目目录
cd d:\Learn\2026SPR\intern\what_format

# 2. 创建并激活虚拟环境
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 1.2 访问服务

- 前端界面: http://localhost:8000
- API文档: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 2. 生产环境部署

### 2.1 使用Gunicorn (Linux/macOS)

```bash
# 安装gunicorn
pip install gunicorn

# 启动（4个worker进程）
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 2.2 使用Waitress (Windows)

```bash
# 安装waitress
pip install waitress

# 启动
waitress-serve --host=0.0.0.0 --port=8000 backend.main:app
```

### 2.3 Systemd服务配置 (Linux)

创建 `/etc/systemd/system/whatformat.service`:

```ini
[Unit]
Description=What Format Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/what_format
Environment=PATH=/path/to/what_format/venv/bin
ExecStart=/path/to/what_format/venv/bin/gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl daemon-reload
sudo systemctl start whatformat
sudo systemctl enable whatformat
sudo systemctl status whatformat
```

---

## 3. Docker部署（可选）

### 3.1 Dockerfile

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p logs uploads outputs

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.2 Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  whatformat:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
      - ./outputs:/app/outputs
      - ./Samples:/app/Samples
    environment:
      - DEBUG=false
      - HOST=0.0.0.0
      - PORT=8000
    restart: unless-stopped
```

### 3.3 构建和运行

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 4. Nginx反向代理配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 文件上传大小限制
    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

---

## 5. 监控和日志

### 5.1 日志位置

```
logs/
├── app_YYYY-MM-DD.log           # 应用日志
├── error_YYYY-MM-DD.log         # 错误日志
├── user_operations_YYYY-MM-DD.log  # 用户操作日志
└── processing_YYYY-MM-DD.log    # 处理日志
```

### 5.2 日志查看

```bash
# 实时查看应用日志
tail -f logs/app_$(date +%Y-%m-%d).log

# 查看错误日志
cat logs/error_$(date +%Y-%m-%d).log

# 搜索特定错误
grep "ERROR" logs/app_*.log
```

### 5.3 健康检查

```bash
# 简单健康检查
curl http://localhost:8000/api/health

# 监控脚本示例
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health)
if [ $response != "200" ]; then
    echo "Service is down!"
    # 发送告警...
fi
```

---

## 6. 安全建议

### 6.1 生产环境配置

```env
# .env
DEBUG=false
# 限制CORS来源
# CORS_ORIGINS=https://your-domain.com
```

### 6.2 文件安全

- 限制上传文件大小（默认15MB）
- 验证文件类型
- 定期清理临时文件

### 6.3 HTTPS配置

使用Let's Encrypt获取免费SSL证书:
```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com
```

---

## 7. 性能优化

### 7.1 Worker数量

```bash
# 推荐: CPU核心数 * 2 + 1
gunicorn backend.main:app -w $(($(nproc) * 2 + 1)) -k uvicorn.workers.UvicornWorker
```

### 7.2 并发限制

在 `config.py` 中配置:
```python
MAX_CONCURRENT_TASKS = 5
PROCESSING_TIMEOUT = 60
```

### 7.3 临时文件清理

设置定时任务清理:
```bash
# crontab -e
0 * * * * find /path/to/what_format/uploads -mmin +60 -delete
0 0 * * * find /path/to/what_format/outputs -mtime +7 -delete
```

---

## 8. 故障排除

### 问题1: 服务无法启动

```bash
# 检查端口占用
netstat -tlnp | grep 8000

# 检查日志
cat logs/error_*.log
```

### 问题2: 文件处理超时

- 增加 `PROCESSING_TIMEOUT` 配置
- 检查OCR是否正常工作
- 检查文件大小是否过大

### 问题3: 内存不足

```bash
# 监控内存使用
free -m
top -p $(pgrep -f uvicorn)

# 减少worker数量
gunicorn backend.main:app -w 2 ...
```

### 问题4: 权限问题

```bash
# 确保目录可写
chmod -R 755 logs/ uploads/ outputs/
chown -R www-data:www-data /path/to/what_format
```
