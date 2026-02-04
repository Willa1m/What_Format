# What Format

简历/求职信模板统一格式转换服务

## 功能特性

- **多格式输入**: 支持PDF、DOCX、PNG、JPG格式的模板文件
- **智能内容提取**: 自动识别简历各部分内容（教育、技能、经历等）
- **模板样式分析**: 分析模板的视觉结构和样式信息
- **格式统一输出**: 将内容按照选定模板样式重新排版
- **并发处理**: 支持多用户同时使用
- **错误重试**: 自动重试机制确保高成功率

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动服务

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问服务

- 前端界面: http://localhost:8000
- API文档: http://localhost:8000/docs

## 项目结构

```
what_format/
├── backend/                 # 后端代码
│   ├── api/                # API路由
│   ├── models/             # 数据模型
│   ├── services/           # 核心服务
│   │   ├── file_parser.py       # 文件解析
│   │   ├── template_analyzer.py # 模板分析
│   │   ├── content_extractor.py # 内容提取
│   │   ├── format_converter.py  # 格式转换
│   │   └── document_generator.py# 文档生成
│   ├── utils/              # 工具函数
│   ├── config.py           # 配置管理
│   └── main.py             # 主入口
├── frontend/               # 前端文件
├── tests/                  # 测试用例
├── docs/                   # 文档
│   ├── API.md             # API文档
│   ├── ALGORITHM.md       # 算法说明
│   ├── ENVIRONMENT.md     # 环境配置
│   └── DEPLOYMENT.md      # 部署指南
├── Samples/               # 样例文件
├── logs/                  # 日志目录
├── uploads/               # 上传临时目录
├── outputs/               # 输出目录
├── requirements.txt       # 依赖列表
└── README.md
```

## API接口

### 主要接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/supported-formats` | GET | 获取支持的格式 |
| `/api/process` | POST | 文件处理主接口 |
| `/api/process-sample` | POST | 样例文件处理 |

### 使用示例

```bash
# 处理文件
curl -X POST "http://localhost:8000/api/process" \
  -F "template_file=@template.pdf" \
  -F "content_file=@resume.docx" \
  --output formatted_resume.docx
```

## 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_integration.py -v
```

## 系统依赖

### 可选依赖（用于图片模板OCR）

- **Tesseract OCR**: 用于图片文字识别
  - Windows: [下载安装](https://github.com/UB-Mannheim/tesseract/wiki)
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

- **Poppler**: 用于PDF转图片
  - Windows: [下载安装](https://github.com/oschwartz10612/poppler-windows/releases)
  - macOS: `brew install poppler`
  - Linux: `sudo apt-get install poppler-utils`

## 配置

可通过 `.env` 文件或环境变量配置：

```env
DEBUG=false
HOST=0.0.0.0
PORT=8000
MAX_FILE_SIZE=15728640
TESSERACT_CMD=tesseract
OCR_LANGUAGE=chi_sim+eng
```

## 文档

- [API接口文档](docs/API.md)
- [算法实现说明](docs/ALGORITHM.md)
- [环境配置文档](docs/ENVIRONMENT.md)
- [部署指南](docs/DEPLOYMENT.md)

## 技术栈

- **后端**: FastAPI, Python 3.10+
- **前端**: Vue.js 3, TailwindCSS
- **文档处理**: python-docx, pdfplumber, pytesseract
- **日志**: loguru

## 许可证

MIT License

---

*Created: 2026-01-29*
