# 🚀 Hướng Dẫn Chạy Streamlit App

## 📦 Prerequisites

Trước khi chạy app, hãy đảm bảo bạn đã cài đặt các dependencies cần thiết.

### 1. **Cài Đặt Python Dependencies**

```bash
# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. **Cài Đặt Tesseract OCR** (Bắt buộc)

Pytesseract cần Tesseract binary để hoạt động.

#### **Windows**
1. Download từ: https://github.com/UB-Mannheim/tesseract/wiki
2. Chọn bản `tesseract-ocr-w64-setup-v5.x.x.exe`
3. Chạy installer, cài đặt ở `C:\Program Files\Tesseract-OCR` ✅ (Khuyến khích)
4. **Tự động**: `app.py` sẽ tự động detect Tesseract từ standard paths
5. **Manual** (nếu cài ở vị trí khác): Xem phần Troubleshooting

#### **Linux (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### **macOS**
```bash
brew install tesseract
```

### 3. **Chuẩn Bị Trained Model**

Streamlit app cần một trained model. Bạn có 2 cách:

#### **Option A: Train Model Mới**
```bash
python main.py --n-clusters 5 --n-estimators 300
# Sẽ tạo file: models/fraud_detection_model_YYYYMMDD_HHMMSS.pkl
```

#### **Option B: Dùng Model Existing**
Nếu đã có file model trong `models/`, app sẽ tự động detect.

---

## ▶️ Chạy Streamlit App

### **1. Basic**
```bash
streamlit run app.py
```

**Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
External URL: https://xxxxx.streamlit.app

If you'd like to turn off this message, set the STREAMLIT_LOGGER_LEVEL environment variable to error.
```

### **2. Với Custom Port**
```bash
streamlit run app.py --server.port 8000
```

### **3. Với Configuration File**
Tạo file `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[logger]
level = "info"
```

---

## 🎯 Cách Sử Dụng App

### **Workflow:**

```
┌─────────────────────────────────────────┐
│ 1. Open Browser                         │
│    http://localhost:8501                │
└─────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────┐
│ 2. Sidebar: Load Model                  │
│    - Select model from dropdown          │
│    - Click "📂 Load Model"              │
└─────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────┐
│ 3. Main Page: Upload Image              │
│    - Choose image file (JPG/PNG)        │
│    - Click "🔤 Extract Text (OCR)"      │
└─────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────┐
│ 4. Review Extracted Text                │
│    - Check if OCR is correct             │
│    - Edit if needed                     │
└─────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────┐
│ 5. Click "🚀 ANALYZE MESSAGE"           │
│    - Wait for analysis                  │
│    - See results                        │
└─────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────┐
│ 6. View Results                         │
│    - Risk Score                         │
│    - Severity Level                     │
│    - Detection Reasons                  │
│    - Export (JSON/CSV)                  │
└─────────────────────────────────────────┘
```

### **Step-by-Step:**

1. **Tải ảnh tin nhắn**
   - Click vào upload area hoặc kéo thả ảnh
   - Hỗ trợ: JPG, PNG, BMP, TIFF
   - Kích thước tối đa: không giới hạn

2. **Nhận diện text (OCR)**
   - Click "🔤 Extract Text (OCR)"
   - Hệ thống sẽ tự động nhận diện text từ ảnh
   - Có thể chọn ngôn ngữ: English, Vietnamese, hoặc cả hai

3. **Xem và chỉnh sửa text**
   - Text sẽ hiển thị ở text area
   - Bạn có thể chỉnh sửa text nếu OCR nhận diện không chính xác

4. **Phân tích message**
   - Click "🚀 ANALYZE MESSAGE"
   - Hệ thống sẽ sử dụng 3 model để phân tích:
     - Random Forest: Fraud probability
     - K-Means: Message cluster
     - Apriori: Rule matching

5. **Xem kết quả**
   - **Risk Score**: Tổng hợp điểm từ 3 model (0-100%)
   - **Fraud Probability**: Khả năng lừa đảo từ RF (0-100%)
   - **Severity**: Mức độ nguy hiểm (Critical/High/Medium/Low)
   - **Reasons**: Giải thích chi tiết

6. **Xuất kết quả**
   - JSON: Dữ liệu chi tiết
   - CSV: Để import vào Excel/Sheets

---

## 🛠️ Troubleshooting

### **Error: "ModuleNotFoundError: No module named 'pytesseract'"**
```bash
pip install pytesseract
```

### **Error: "Tesseract is not installed"**
- Windows: Download từ https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr`
- Mac: `brew install tesseract`

### **Error: "No trained models found"**
```bash
# Train a new model
python main.py

# Or download pre-trained model from releases
```

### **Error: "pytesseract.TesseractNotFoundError" (When Uploading Image)**

**Auto-Detection**: `app.py` tự động detect Tesseract từ các đường dẫn phổ biến trên Windows:
- `C:\Program Files\Tesseract-OCR\tesseract.exe` ✅ (Standard)
- `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`
- `D:\Tesseract-OCR\tesseract.exe`

**Nếu lỗi vẫn xuất hiện:**

**Option 1: Cài lại Tesseract (Cách nhanh nhất)**
1. Uninstall Tesseract từ Control Panel
2. Download từ https://github.com/UB-Mannheim/tesseract/wiki
3. Cài lại chọn path: `C:\Program Files\Tesseract-OCR`
4. Restart Streamlit: `streamlit run app.py`

**Option 2: Add path manually (Nếu cài ở vị trí khác)**
- Mở `app.py`
- Tìm phần "CONFIGURE PYTESSERACT PATH" (dòng ~20)
- Thêm path của bạn vào `_TESSERACT_PATHS` list:
```python
_TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"D:\Tesseract-OCR\tesseract.exe",
    r"C:\Your\Custom\Path\tesseract.exe",  # ← Thêm dòng này
]
```

**Option 3: System PATH (Linux/Mac)**
Đảm bảo Tesseract có trong system PATH:
```bash
# Check if tesseract is in PATH
tesseract --version

# On Linux, if not found:
sudo apt-get install tesseract-ocr

# On Mac:
brew install tesseract
```

### **OCR không chính xác**
- Ảnh phải có quality tốt (min 300 DPI)
- Text phải rõ ràng, không bị tilt
- Chọn đúng language setting

### **App chạy chậm**
- Có thể model đang load lần đầu
- Hoặc image quá lớn (resize về ~1920x1080)

---

## 📊 Features Chi Tiết

### **Sidebar Features**

1. **⚙️ Settings**
   - Model management
   - OCR language selection
   - Export format selection

2. **🤖 Model Management**
   - Dropdown để chọn model
   - Button load model
   - Model info

3. **📊 Model Status**
   - Status indicator (Ready/Not Loaded)
   - Loaded model name

4. **🔤 OCR Settings**
   - Language: eng+vie (English + Vietnamese)
   - Language: eng (English only)
   - Language: vie (Vietnamese only)

5. **💾 Export Settings**
   - JSON checkbox
   - CSV checkbox

### **Main Page Features**

1. **📤 Upload Area**
   - Drag & drop support
   - File browser
   - Image preview
   - Image info (size, format)

2. **✏️ Manual Text Input**
   - Text area với history
   - Pre-fill từ OCR result

3. **🚀 Analyze Button**
   - One-click analysis
   - Loading spinner
   - Error handling

4. **📊 Results Display**
   - Risk score metric
   - Fraud probability metric
   - Severity badge
   - Risk gauge
   - Detection reasons
   - Additional info (JSON)

5. **💾 Export**
   - JSON download button
   - CSV download button
   - Auto-generated filename

---

## 🚀 Deploy to Cloud

### **Option 1: Streamlit Cloud (FREE)**

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select GitHub repo, branch, and `app.py`
5. Deploy (takes 2-3 min)
6. Share link automatically

### **Option 2: Heroku**

1. Create `Procfile`:
   ```
   web: streamlit run app.py --logger.level=error
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### **Option 3: Docker**

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   RUN apt-get update && apt-get install -y tesseract-ocr
   COPY . .
   CMD ["streamlit", "run", "app.py"]
   ```

2. Build & run:
   ```bash
   docker build -t fraud-analyzer .
   docker run -p 8501:8501 fraud-analyzer
   ```

---

## 📈 Performance Tips

1. **Pre-load Model**: App tự động cache model khi load lần đầu
2. **Image Optimization**: Resize ảnh lớn trước khi upload
3. **OCR Speed**: English-only OCR nhanh hơn English+Vietnamese
4. **Batch Processing**: Để lần sau implement

---

## 🔐 Security Considerations

- App không save uploaded images
- Results không được lưu (optional: add database)
- Model file có thể protect bằng encryption

---

## 📞 Support

Nếu gặp vấn đề:
1. Check Tesseract installation
2. Verify model file exists
3. Check Python version (3.8+)
4. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

## 📝 File Structure

```
.
├── app.py                      ← Streamlit app (chính)
├── PROJECT_OVERVIEW.md         ← Project documentation
├── STREAMLIT_SETUP.md          ← File này
├── requirements.txt            ← Dependencies (updated)
├── models/
│   └── fraud_detection_model_*.pkl
├── src/
│   ├── pipeline.py
│   ├── preprocessing.py
│   ├── clustering.py
│   ├── classification.py
│   ├── association_rules.py
│   ├── recommendation.py
│   └── features.py
└── dataset/
    ├── sms/
    └── email/
```

---

**Happy analyzing! 🛡️**
