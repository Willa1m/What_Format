<div align="center">

# 🎨 What Format

<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Three.js-r160-black?style=for-the-badge&logo=threedotjs&logoColor=white" alt="Three.js">
<img src="https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="TailwindCSS">

<br><br>

**✨ Transform chaos into order. ✨**

*A rule-based resume & cover-letter formatter with a Three.js web UI — a personal learning project*

[Features](#-features) • [Quick Start](#-quick-start) • [API](#-api-reference) • [Architecture](#-architecture) • [Contributing](#-contributing)

---

</div>

## 🌟 Overview

**What Format** is a personal learning project: it parses resumes and cover letters (PDF/DOCX), detects their sections with keyword, regex and synonym rules, and re-renders them into a clean DOCX template. Featuring an immersive 3D preview experience powered by Three.js and a sleek dark-mode UI.

<div align="center">

```
   ╔═══════════════════════════════════════════════════════════╗
   ║                                                           ║
   ║     📄  Upload Your Document                              ║
   ║           ↓                                               ║
   ║     🔎  Rule-Based Section Detection                      ║
   ║           ↓                                               ║
   ║     🎨  Smart Template Formatting                         ║
   ║           ↓                                               ║
   ║     ✨  Download Professional Result                      ║
   ║                                                           ║
   ╚═══════════════════════════════════════════════════════════╝
```

</div>

## 🚀 Features

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities
- **Multi-Format Input** - PDF, DOCX, DOC support
- **Section Detection** - keyword, regex and synonym rules (`backend/services/smart_classifier.py`)
- **Template Analysis** - Visual structure parsing
- **Professional Output** - Clean, formatted DOCX

</td>
<td width="50%">

### 🎨 User Experience
- **3D Document Preview** - Interactive Three.js visualization
- **Dark Mode UI** - Modern minimalist design
- **Real-time Feedback** - Live processing status
- **Bilingual Support** - English / 中文

</td>
</tr>
</table>

### 🔥 Highlights

| Feature | Description |
|---------|-------------|
| 🖼️ **3D Visualization** | Real-time 3D document preview with mouse interaction |
| 🌙 **Dark Mode** | Eye-friendly dark theme with high contrast |
| ⚡ **Fast Processing** | Async architecture for rapid conversion |
| 🔒 **Secure** | Local processing, no data leaves your server |
| 📱 **Responsive** | Works on desktop and mobile devices |

## 🛠️ Quick Start

### Prerequisites

- Python 3.10+
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Willa1m/What_Format.git
cd What_Format

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Launch

```bash
# Start Backend API Server (Port 8000)
python main.py

# Start Frontend Dev Server (Port 5173) - in another terminal
cd frontend
python -m http.server 5173
```

### Access

| Service | URL |
|---------|-----|
| 🌐 Frontend | http://localhost:5173 |
| 📡 API Docs | http://localhost:8000/docs |
| ❤️ Health Check | http://localhost:8000/api/health |

## 📁 Project Structure

```
What_Format/
│
├── 🎨 frontend/                 # Frontend Application
│   ├── index.html              # Home - Kinetic typography & 3D particles
│   ├── convert.html            # Format - 3D document preview
│   ├── about.html              # About - Mission & stats
│   ├── css/style.css           # Design system & animations
│   └── js/
│       ├── main.js             # Core logic & i18n
│       ├── scene.js            # 3D document renderer
│       └── home_bg.js          # Particle background
│
├── ⚙️ backend/                  # Backend API
│   ├── api/routes.py           # REST endpoints
│   ├── services/               # Business logic
│   │   ├── file_parser.py      # Document parsing
│   │   ├── content_extractor.py# Content extraction
│   │   ├── template_processor.py# Template processing
│   │   └── document_generator.py# DOCX generation
│   ├── models/schemas.py       # Pydantic models
│   ├── utils/                  # Helpers & logger
│   ├── config.py               # Configuration
│   └── main.py                 # FastAPI app
│
├── 📚 docs/                     # Documentation
├── 📄 Samples/                  # Sample files
├── 🧪 tests/                    # Test suite (excluded from repo)
├── main.py                     # Entry point
└── requirements.txt            # Dependencies
```

## 🔌 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/supported-formats` | List supported formats |
| `GET` | `/api/templates/info` | Get template information |
| `POST` | `/api/resume/convert` | Convert resume document |
| `POST` | `/api/cover-letter/convert` | Convert cover letter |
| `GET` | `/api/files/{filename}` | Download converted file |

### Example Request

```bash
# Convert a resume
curl -X POST "http://localhost:8000/api/resume/convert" \
  -F "content_file=@your_resume.pdf" \
  -H "accept: application/json"

# Response
{
  "task_id": "abc123",
  "status": "completed",
  "download_url": "/api/files/Your_Resume_Formatted.docx",
  "processing_time": 1.23
}
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  index.html │  │convert.html │  │ about.html  │              │
│  │   (Home)    │  │  (Format)   │  │   (About)   │              │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘              │
│         │                │                                       │
│         │    ┌───────────┴───────────┐                          │
│         │    │      Three.js         │                          │
│         │    │  3D Document Scene    │                          │
│         │    └───────────────────────┘                          │
└─────────┼────────────────────────────────────────────────────────┘
          │ HTTP/REST
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    API Router                            │    │
│  │   /resume/convert  /cover-letter/convert  /files/{id}   │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                     │
│  ┌─────────────────────────▼───────────────────────────────┐    │
│  │                   Services Layer                         │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │    │
│  │  │  Parser  │→│Extractor │→│Processor │→│Generator │   │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## 🎨 Design System

| Element | Value |
|---------|-------|
| **Background** | `#080808` (Deep Black) |
| **Text** | `#E0D4C5` (Warm Cream) |
| **Accent** | `#FFFFFF` (Pure White) |
| **Font Display** | Syne (800) |
| **Font Body** | Inter (300-500) |

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
# Server
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Processing
MAX_FILE_SIZE=15728640

# OCR (Optional)
TESSERACT_CMD=tesseract
OCR_LANGUAGE=chi_sim+eng
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [API.md](docs/API.md) | Complete API documentation |
| [ALGORITHM.md](docs/ALGORITHM.md) | Processing algorithms |
| [ENVIRONMENT.md](docs/ENVIRONMENT.md) | Environment setup |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deployment guide |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Three.js](https://threejs.org/) - 3D graphics library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [TailwindCSS](https://tailwindcss.com/) - Utility-first CSS framework
- [python-docx](https://python-docx.readthedocs.io/) - DOCX generation

---

<div align="center">

**Made with ❤️ by [Willa1m](https://github.com/Willa1m)**

*Transform your documents. Elevate your career.*

<br>

⭐ Star this repo if you find it useful!

</div>

## 中文说明

What Format 是我自己的学习项目，用来把简历和求职信整理成统一格式。

- 后端：用 FastAPI 接收 PDF 或 DOCX 文件，经过「解析 → 内容抽取 → 模板处理 → 生成 DOCX」四个步骤输出结果。
- 分段识别：基于关键词、正则表达式和同义词库的规则方法（见 `backend/services/smart_classifier.py`），没有使用机器学习模型。
- 前端：静态页面，带 Three.js 3D 文档预览，支持中英文切换。

运行方式：

1. 执行 `pip install -r requirements.txt` 安装依赖；
2. 执行 `python main.py` 启动后端（端口 8000）；
3. 在 `frontend/` 目录下执行 `python -m http.server 5173` 启动前端页面。
