# 使用 Azure OpenAI + FastAPI + HTML 建立 AI 圖片解說網站完整實作紀錄

## 專案目標

建立一個部署於 Microsoft Azure 的 AI 網頁系統：

```text
使用者
    ↓
HTML + JavaScript
    ↓
FastAPI
    ↓
Azure OpenAI
    ↓
GPT-4o
    ↓
六階段 Agent Pipeline
```

功能：

- 圖片提示詞分析
- PixAI Prompt 生成
- LoRA 推薦
- 圖片結構分析
- 主持人風格文案生成
- 修改建議
- 最終文案產出

---

# 第一階段：Azure OpenAI 建立

## 建立 Azure OpenAI Resource

Azure Portal：

```text
建立資源
→ Azure OpenAI
```

建立完成後取得：

```text
API Key
Endpoint
Deployment Name
```

---

# 第二階段：移除 Groq

原程式：

```python
import aisuite as ai
client = ai.Client()
```

改用 Azure OpenAI SDK。

---

# 第三階段：Prompt 外部化

建立 prompts/ 資料夾並將各 Agent Prompt 拆分成獨立 txt 檔案。

---

# 第四階段：環境變數管理

建立 .env：

```env
AZURE_OPENAI_KEY=xxxxx
AZURE_OPENAI_ENDPOINT=https://pixaiprompts.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt4o
```

並透過 config.py 讀取。

---

# 第五階段：FastAPI 建置

建立 app.py：

```python
app = FastAPI()
```

建立：

```python
@app.post('/chat')
```

提供前端呼叫。

---

# 第六階段：HTML 前端

建立：

```text
templates/index.html
static/css/style.css
static/js/app.js
```

並使用深色紫色主題介面。

---

# 第七階段：Azure GPT 模型測試

曾測試 GPT-5 Pro，遭遇：

```text
404 Resource not found
The requested operation is unsupported
```

後續改用 GPT-4o Deployment。

---

# 第八階段：Azure Content Safety

發生：

```text
The response was filtered due to Azure OpenAI content policy
```

加入 try/except 防止網站 500 Error。

---

# 第九階段：GitHub 與 Azure App Service

建立 GitHub Repository：

```text
pixaiprompts/
├── app.py
├── config.py
├── prompts.py
├── requirements.txt
├── static/
├── prompts/
└── templates/
```

---

# 第十階段：Azure App Service

建立：

```text
App Service
Python 3.11
Linux
Japan East
```

設定環境變數：

```text
AZURE_OPENAI_KEY
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_DEPLOYMENT
```

---

# 第十一階段：GitHub Actions 自動部署

成功建立：

```text
GitHub
↓
GitHub Actions
↓
Azure App Service
```

自動部署流程。

---

# 第十二階段：FastAPI 部署錯誤排除

Azure 將 FastAPI 誤判為 Flask：

```text
TypeError: FastAPI.__call__() missing 1 required positional argument: 'send'
```

原因：

```text
Using worker: sync
```

改用：

```text
gunicorn --bind=0.0.0.0:8000 -k uvicorn.workers.UvicornWorker app:app
```

成功啟動。

---

# 最終成果

✅ Azure OpenAI 串接成功
✅ GPT-4o Deployment 成功
✅ FastAPI 成功部署於 Azure App Service
✅ GitHub Actions 自動部署成功
✅ HTML/CSS/JS 前端完成
✅ 六階段 Agent Pipeline 成功運作
✅ 網站正式上線

## 最終架構

```text
Azure App Service
        ↓
FastAPI
        ↓
Azure OpenAI GPT-4o
        ↓
Prompts Analyzer
        ↓
Prompts Implementer
        ↓
Analyzer
        ↓
Implementer
        ↓
Evaluator
        ↓
ReImplementer
        ↓
HTML 前端
```
