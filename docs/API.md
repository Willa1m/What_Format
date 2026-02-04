# What Format API 接口文档

## 概述

What Format 是一个简历/求职信格式转换服务，提供RESTful API接口。

**基础URL**: `http://localhost:8000`

**API前缀**: `/api`

---

## 接口列表

### 1. 健康检查

检查服务运行状态。

**端点**: `GET /api/health`

**响应示例**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-29T16:00:00.000Z"
}
```

---

### 2. 获取支持的格式

获取系统支持的文件格式列表。

**端点**: `GET /api/supported-formats`

**响应示例**:
```json
{
  "template_formats": [".pdf", ".docx", ".png", ".jpg", ".jpeg"],
  "content_formats": [".pdf", ".docx"],
  "output_formats": [".docx", ".pdf"]
}
```

---

### 3. 文件处理（主接口）

上传模板文件和内容文件，生成格式化后的文档。

**端点**: `POST /api/process`

**请求格式**: `multipart/form-data`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| template_file | File | 是 | 模板文件 (PDF/DOCX/PNG/JPG) |
| content_file | File | 是 | 内容文件 (PDF/DOCX) |
| doc_type | String | 否 | 文档类型: "resume"(简历) 或 "cl"(求职信)，默认"resume" |

**文件限制**:
- 最大文件大小: 15MB
- 模板格式: .pdf, .docx, .png, .jpg, .jpeg
- 内容格式: .pdf, .docx

**响应**:
- 成功: 返回DOCX文件 (Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document)
- 失败: 返回JSON错误信息

**成功响应**:
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="formatted_xxx.docx"
```

**错误响应示例**:
```json
{
  "detail": "不支持的模板格式: .txt。支持的格式: ['.pdf', '.docx', '.png', '.jpg', '.jpeg']"
}
```

**cURL 示例**:
```bash
curl -X POST "http://localhost:8000/api/process" \
  -F "template_file=@template.pdf" \
  -F "content_file=@resume.docx" \
  -F "doc_type=resume" \
  --output formatted_resume.docx
```

**JavaScript 示例**:
```javascript
const formData = new FormData();
formData.append('template_file', templateFile);
formData.append('content_file', contentFile);
formData.append('doc_type', 'resume');

const response = await fetch('/api/process', {
  method: 'POST',
  body: formData
});

if (response.ok) {
  const blob = await response.blob();
  // 处理下载
}
```

---

### 4. 样例文件处理

使用预设的样例文件进行处理测试。

**端点**: `POST /api/process-sample`

**说明**: 使用 `PDF_sample.pdf` 作为模板，`Haoran_Tu RESUME.docx` 作为内容

**响应**: 返回格式化后的DOCX文件

---

### 5. XIAOMING样例处理

使用图片模板和PDF内容进行处理。

**端点**: `POST /api/process-xiaoming`

**说明**: 使用 `Sample_Picture_format.png` 作为模板，`XIAOMING's Resume.pdf` 作为内容

**响应**: 返回格式化后的DOCX文件

---

## 错误码

| HTTP状态码 | 说明 |
|------------|------|
| 200 | 成功 |
| 400 | 请求参数错误（格式不支持、文件过大等） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

---

## 注意事项

1. **文件大小限制**: 单个文件不超过15MB
2. **并发处理**: 系统支持最多5个并发处理任务
3. **重试机制**: 处理失败时会自动重试最多3次
4. **临时文件**: 上传的临时文件会在处理完成后自动清理
5. **OCR支持**: 图片模板需要系统安装Tesseract OCR

---

## 交互式文档

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
