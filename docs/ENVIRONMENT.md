# What Format 环境配置文档

## 1. 系统要求

### 操作系统
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, CentOS 8+)

### Python版本
- Python 3.10 或更高版本

---

## 2. 依赖安装

### 2.1 创建虚拟环境

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.2 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2.3 依赖包列表

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| fastapi | >=0.109.0 | Web框架 |
| uvicorn | >=0.27.0 | ASGI服务器 |
| python-multipart | >=0.0.9 | 文件上传 |
| python-docx | >=1.1.0 | DOCX处理 |
| pdfplumber | >=0.10.0 | PDF文本提取 |
| PyPDF2 | >=3.0.0 | PDF读取 |
| pdf2image | >=1.17.0 | PDF转图片 |
| reportlab | >=4.0.0 | PDF生成 |
| Pillow | >=10.0.0 | 图片处理 |
| pytesseract | >=0.3.10 | OCR识别 |
| aiofiles | >=23.2.0 | 异步文件操作 |
| pydantic | >=2.5.0 | 数据验证 |
| pydantic-settings | >=2.0.0 | 配置管理 |
| loguru | >=0.7.0 | 日志 |
| pytest | >=8.0.0 | 测试 |
| httpx | >=0.26.0 | HTTP客户端测试 |

---

## 3. 系统依赖

### 3.1 Tesseract OCR（可选，用于图片模板）

#### Windows
1. 下载安装包：https://github.com/UB-Mannheim/tesseract/wiki
2. 安装时选择中文语言包
3. 添加到系统PATH或配置环境变量

```bash
# 验证安装
tesseract --version
```

#### macOS
```bash
brew install tesseract
brew install tesseract-lang  # 安装语言包
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-chi-sim  # 中文简体
sudo apt-get install tesseract-ocr-eng      # 英文
```

### 3.2 Poppler（用于PDF转图片，可选）

#### Windows
1. 下载：https://github.com/oschwartz10612/poppler-windows/releases
2. 解压并添加bin目录到PATH

#### macOS
```bash
brew install poppler
```

#### Linux
```bash
sudo apt-get install poppler-utils
```

---

## 4. 环境变量配置

创建 `.env` 文件（可选）:

```env
# 应用配置
APP_NAME=What Format
DEBUG=false

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 文件配置
MAX_FILE_SIZE=15728640

# OCR配置
TESSERACT_CMD=tesseract
OCR_LANGUAGE=chi_sim+eng
```

---

## 5. 目录结构确认

确保以下目录存在（程序会自动创建）:

```
what_format/
├── logs/          # 日志目录
├── uploads/       # 上传文件临时目录
├── outputs/       # 输出文件目录
├── Samples/       # 样例文件目录
│   ├── PDF_sample.pdf
│   ├── Haoran_Tu RESUME.docx
│   ├── Sample_Picture_format.png
│   └── XIAOMING's Resume.pdf
└── frontend/      # 前端文件
    └── index.html
```

---

## 6. 验证安装

### 6.1 运行测试

```bash
# 激活虚拟环境
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 运行测试
pytest tests/ -v
```

### 6.2 启动服务

```bash
# 方式1：使用uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 方式2：使用Python
python -m backend.main
```

### 6.3 验证服务

```bash
# 健康检查
curl http://localhost:8000/api/health

# 或在浏览器中访问
# http://localhost:8000/docs  # API文档
# http://localhost:8000/      # 前端界面
```

---

## 7. 常见问题

### Q1: pip install 报错

**解决方案**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: Tesseract未找到

**解决方案**:
- 检查是否已安装
- 确认PATH环境变量包含Tesseract安装路径
- 在 `.env` 中配置完整路径:
  ```env
  TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
  ```

### Q3: PDF转图片失败

**解决方案**:
- 安装Poppler
- 确认PATH包含Poppler bin目录

### Q4: 中文乱码

**解决方案**:
- 安装中文字体
- 确认Tesseract安装了中文语言包
- Windows: 安装SimSun（宋体）字体

### Q5: 权限错误

**解决方案**:
```bash
# Windows以管理员身份运行
# Linux/macOS
chmod -R 755 what_format/
```

---

## 8. 开发环境推荐

### IDE
- VS Code + Python扩展
- PyCharm

### VS Code 推荐扩展
- Python
- Pylance
- Python Docstring Generator
- REST Client (API测试)
