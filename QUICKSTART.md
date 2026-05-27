# ⚡ QUICKSTART - Chạy Streamlit App trong 5 Phút

## 🎯 Mục Tiêu
Chạy Streamlit app để phân tích tin nhắn lừa đảo qua giao diện web.

---

## ⏱️ 5 Bước

### **Step 1: Cài Đặt Tesseract** (2 min)
**Windows:**
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Chọn `tesseract-ocr-w64-setup-v5.x.x.exe`
- Cài vào `C:\Program Files\Tesseract-OCR`

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

---

### **Step 2: Cài Dependencies** (1 min)
```bash
# Activate venv
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

---

### **Step 3: Kiểm Tra Model** (1 min)
Kiểm tra xem có model training sẵn không:

```bash
# List models
ls models/

# Nếu không có, train model (takes 5-10 min)
python main.py
```

---

### **Step 4: Chạy App** (1 min)
```bash
streamlit run app.py
```

**Output:**
```
Local URL: http://localhost:8501
```

---

### **Step 5: Sử Dụng** (Instant!)
1. **Sidebar**: Load model
2. **Main**: Upload ảnh
3. **Extract**: Click OCR button
4. **Analyze**: Click Analyze button
5. **Results**: See fraud detection results

---

## 📂 Các File Đã Tạo

| File | Mục Đích |
|------|----------|
| `app.py` | 🔴 **Main Streamlit app** |
| `PROJECT_OVERVIEW.md` | 📄 Tài liệu chi tiết project |
| `STREAMLIT_SETUP.md` | 🚀 Hướng dẫn setup Streamlit |
| `README.md` | 📖 README project |
| `.streamlit/config.toml` | ⚙️ Streamlit configuration |
| `requirements.txt` | 📦 Updated dependencies |

---

## 🎨 App Structure

```
Streamlit UI
├── 📌 Sidebar
│   ├── ⚙️ Model Selection
│   ├── 📊 Model Status
│   ├── 🔤 OCR Settings
│   └── 💾 Export Settings
│
└── 📌 Main Page
    ├── 📤 Step 1: Upload & Extract
    │   ├── Image upload
    │   ├── OCR button
    │   └── Text area
    │
    └── 🔍 Step 2: Analyze & Results
        ├── 🚀 Analyze button
        ├── 📊 Risk Score
        ├── ⚠️ Severity
        ├── 💬 Detection Reasons
        └── 💾 Export (JSON/CSV)
```

---

## 🔧 Troubleshooting

### **"Tesseract is not installed"**
→ Install from https://github.com/UB-Mannheim/tesseract/wiki

### **"No models found"**
→ Run: `python main.py`

### **"pytesseract module not found"**
→ Run: `pip install pytesseract`

### **"Streamlit command not found"**
→ Run: `pip install streamlit`

---

## 📊 Expected Output

```
Risk Analysis Result:
├── Risk Score: 74%
├── Severity: HIGH 🟠
├── Fraud Probability: 87%
├── Cluster ID: 1
└── Reasons:
    • High fraud probability (0.87)
    • Matched 2 suspicious rules
    • Cluster 1 has 70% fraud rate
```

---

## ✅ Checklist

- [ ] Tesseract installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Model trained or found in `models/` folder
- [ ] `streamlit run app.py` successful
- [ ] App opens at http://localhost:8501
- [ ] Can upload image and extract text
- [ ] Can analyze and see results

---

## 📚 Next Steps

1. **Upload test images** with fraud messages
2. **Extract text** using OCR
3. **Analyze** to see fraud detection
4. **Export results** as JSON/CSV
5. **Train custom model** with your data

---

## 🎓 Documentation

For more info, see:
- 📄 `PROJECT_OVERVIEW.md` - Full project details
- 🚀 `STREAMLIT_SETUP.md` - Detailed setup guide
- 📖 `README.md` - Project README

---

## 🚀 Deploy to Cloud (Optional)

### **Streamlit Cloud (FREE)**
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Deploy in 2 min

### **Heroku/Docker**
See `STREAMLIT_SETUP.md` for instructions

---

## 💡 Tips

✅ Use clear, well-lit images for OCR
✅ Check OCR result before analyzing
✅ Try different messages to test accuracy
✅ Export results for record keeping
✅ Check sidebar for model status

---

**Ready? Let's go! 🚀**

```bash
streamlit run app.py
```

---

Last updated: May 27, 2026
