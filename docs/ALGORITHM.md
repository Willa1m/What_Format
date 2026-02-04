# What Format 算法实现说明

## 1. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│                    (Vue.js + TailwindCSS)                   │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP API
┌─────────────────────────▼───────────────────────────────────┐
│                     FastAPI Backend                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ FileParser  │  │ Template    │  │ Content             │ │
│  │             │  │ Analyzer    │  │ Extractor           │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         │                │                     │            │
│         ▼                ▼                     ▼            │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Format Converter                           ││
│  └────────────────────────┬────────────────────────────────┘│
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │           Document Generator                            ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 核心模块说明

### 2.1 FileParser（文件解析器）

**功能**: 解析多种格式的文件，提取文本内容和样式信息。

**支持格式**:
- PDF: 使用 `pdfplumber` 提取文本和布局信息
- DOCX: 使用 `python-docx` 读取文档结构
- PNG/JPG: 使用 `pytesseract` 进行OCR识别

**算法流程**:
```
1. 检测文件格式（通过扩展名）
2. 调用对应的解析器
3. 提取文本内容
4. 分析段落结构
5. 识别章节
6. 返回 ParsedContent 和 ParsedStyle
```

**章节识别算法**:
```python
关键词匹配法:
1. 遍历每个段落
2. 检查段落是否包含预定义的章节关键词
3. 如果匹配且段落长度<50字符，判定为章节标题
4. 将后续段落归入该章节
```

### 2.2 TemplateAnalyzer（模板分析器）

**功能**: 分析模板文件的视觉结构和样式信息。

**提取信息**:
- 字体信息（名称、大小、粗体、斜体）
- 段落格式（对齐、间距、缩进）
- 页面布局（边距、分栏）
- 章节样式（标题样式、内容样式、分隔线）

**算法流程**:
```
1. 调用 FileParser 解析模板
2. 分析字体分布，确定主要字体
3. 找出最大字体作为标题字体
4. 为每个章节创建样式配置
5. 返回 AnalyzedTemplate
```

### 2.3 ContentExtractor（内容提取器）

**功能**: 智能识别并结构化提取简历各部分内容。

**提取内容**:
- 联系信息（姓名、邮箱、电话、地址、社交链接）
- 教育经历（学校、学位、专业、GPA、时间）
- 技能列表（分类技能）
- 工作经历（公司、职位、时间、职责描述）
- 项目经验
- 领导力经历

**正则表达式模式**:
```python
邮箱: [\w\.-]+@[\w\.-]+\.\w+
电话: [\+]?[\d\-\(\)\s]{7,20}
URL:  (?:https?://)?(?:www\.)?[\w\.-]+\.\w+(?:/[\w\.-]*)*
日期: (?:Jan|Feb|...)\s*\d{0,4}\s*[-–]\s*(?:Present|...)
GPA:  GPA[:\s]*(\d+\.?\d*)[/\s]*(\d+\.?\d*)?
```

**内容提取算法**:
```
1. 全文提取联系信息（使用正则匹配）
2. 按章节分割文本
3. 对每个章节应用专门的解析规则:
   - 教育: 识别学校名 -> 学位 -> 课程
   - 技能: 识别 "类别: 列表" 格式
   - 经历: 识别 "组织|地点" -> 职位 -> bullet points
4. 返回 ResumeContent 结构化数据
```

### 2.4 FormatConverter（格式转换器）

**功能**: 将提取的内容按照模板样式进行格式映射。

**算法流程**:
```
1. 读取模板的章节顺序
2. 格式化header（姓名）
3. 格式化联系信息（合并为单行）
4. 按模板顺序格式化各章节:
   - 教育 -> _format_education()
   - 技能 -> _format_skills()
   - 经历 -> _format_experiences()
5. 返回 FormattedDocument
```

**内容适配算法**:
```python
def adjust_content_fit(document, max_pages=1):
    # 计算总bullet点数
    total_bullets = sum(len(item.descriptions) for section...)
    
    # 如果超过阈值，进行缩减
    if total_bullets > 25:
        for item in items:
            if len(item.descriptions) > 3:
                item.descriptions = item.descriptions[:3]
```

### 2.5 DocumentGenerator（文档生成器）

**功能**: 根据格式化后的内容生成最终文档。

**生成流程**:
```
1. 创建新的Word文档
2. 设置页面边距
3. 添加header（居中、大字体、粗体）
4. 添加联系信息（居中）
5. 遍历章节:
   a. 添加章节标题（带下划线）
   b. 根据内容类型添加内容
6. 保存文档
```

**样式应用**:
```python
# 标题样式
run.bold = True
run.font.size = Pt(18)
run.font.name = "Times New Roman"

# 章节标题
run.bold = True
run.font.size = Pt(11)
# 添加下划线边框

# 正文
run.font.size = Pt(10)
# Bullet缩进
para.paragraph_format.left_indent = Inches(0.25)
```

---

## 3. 关键技术选型

| 功能 | 技术选择 | 选择理由 |
|------|----------|----------|
| Web框架 | FastAPI | 高性能、异步支持、自动文档生成 |
| PDF解析 | pdfplumber | 精确的文本和布局提取 |
| DOCX处理 | python-docx | 官方支持、功能完整 |
| OCR | pytesseract | 开源、多语言支持 |
| 日志 | loguru | 简单易用、功能强大 |

---

## 4. 性能优化策略

### 4.1 异步处理
- 使用 `aiofiles` 进行异步文件操作
- FastAPI的异步路由处理

### 4.2 重试机制
```python
async def process_document(max_retries=3):
    for attempt in range(max_retries):
        try:
            return await do_process()
        except Exception:
            if attempt < max_retries - 1:
                await asyncio.sleep(1 * (attempt + 1))
    raise last_error
```

### 4.3 临时文件清理
```python
def cleanup_temp_files(directory, max_age_hours=24):
    for file in directory.iterdir():
        if file_age > max_age_hours * 3600:
            file.unlink()
```

---

## 5. 准确性保证

### 5.1 内容完整性
- 保存原始文本用于验证
- 结构化提取后保留 `raw_text` 字段

### 5.2 格式准确性
- 使用模板的实际样式信息
- 预定义标准样式作为后备

### 5.3 错误处理
- 每个模块独立的错误处理
- 详细的日志记录
- 自动重试机制

---

## 6. 扩展性设计

### 6.1 新格式支持
在 `FileParser` 中添加新的解析方法:
```python
def _parse_new_format(self, file_path):
    # 实现新格式解析
    return content, style
```

### 6.2 新输出格式
在 `DocumentGenerator` 中添加新的生成方法:
```python
def _generate_new_format(self, formatted_doc, output_path):
    # 实现新格式生成
    return output_path
```

### 6.3 自定义模板样式
通过 `config.py` 的 `TEMPLATE_STYLE_MAP` 配置:
```python
TEMPLATE_STYLE_MAP = {
    "header": {"font_name": "Arial", "font_size": 24},
    ...
}
```
