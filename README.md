# 🛡️ Fraud/Spam Message Analysis System

> Phân tích tin nhắn lừa đảo trực tiếp sử dụng AI/ML

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-green.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)](#)

## 🎯 Overview

Hệ thống phân tích tin nhắn lừa đảo sử dụng **machine learning** để:
- ✅ **Phân loại** tin nhắn (Fraud vs Legitimate)
- ✅ **Phân cụm** theo chiến thuật lừa đảo
- ✅ **Khai thác luật kết hợp** từ cặp từ khóa + link giả mạo
- ✅ **Cảnh báo đa phương tiện** với giao diện Streamlit

### 🎨 Tech Stack
```
Frontend:        Streamlit + HTML/CSS
ML Algorithms:   scikit-learn, mlxtend, imbalanced-learn
NLP:             underthesea (Vietnamese), TF-IDF
OCR:             pytesseract (Tesseract)
Visualization:   matplotlib, seaborn
```

---

## 🚀 Quick Start

### **1. Clone & Setup**
```bash
# Clone repository
git clone https://github.com/Ducmanh08022004/Khai_Pha_Cuoi_Ky
cd Khai_Pha_Cuoi_Ky

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### **2. Install Tesseract (for OCR)**
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux**: `sudo apt-get install tesseract-ocr`
- **Mac**: `brew install tesseract`

### **3. Train Model** (Optional - if no pre-trained model)
```bash
python main.py --n-clusters 5 --n-estimators 300
```

### **4. Run Streamlit App**
```bash
streamlit run app.py
```

**Open**: http://localhost:8501

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | 📄 Complete project documentation |
| [STREAMLIT_SETUP.md](STREAMLIT_SETUP.md) | 🚀 Streamlit app setup guide |

---

## 💻 Usage

### **Web Interface (Streamlit)**
```
1. Load trained model from sidebar
2. Upload image with message text
3. Extract text using OCR
4. Click "Analyze"
5. View results & export
```

### **Python API**
```python
from src.pipeline import FraudDetectionPipeline

# Load model
model = FraudDetectionPipeline.load_model("models/fraud_detection_model.pkl")

# Predict
result = model.predict(["Click here to verify your account"])
print(result)

# Output:
#    text  fraud_probability  risk_score severity
# 0  "..."             0.87        0.77     high
```

---

## 🎯 Features

### ✨ Core Features
- 🔍 **Text Preprocessing**: Vietnamese/English support
- 🎲 **Random Forest Classification**: 92%+ ROC-AUC
- 📊 **K-Means++ Clustering**: Group similar fraud patterns
- 🔗 **Association Rules Mining**: Find suspicious patterns
- 🖼️ **OCR Support**: Extract text from images
- 📱 **Responsive UI**: Desktop & mobile friendly

### 🛠️ Advanced Features
- Multi-language support (VI/EN)
- Entity recognition (URL, phone, money, bank)
- Risk scoring with 3-factor weighting
- Severity classification (Critical/High/Medium/Low)
- Export to JSON/CSV
- Model persistence & loading

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **ROC-AUC** | 0.92+ |
| **Accuracy** | 88-92% |
| **Precision** | 85-90% |
| **Recall** | 85-90% |
| **Silhouette Score** | 0.45-0.60 |
| **Rules Found** | 20-50 |

---

## 📁 Project Structure

```
Khai_Pha_Cuoi_Ky/
├── app.py                      ← Streamlit app
├── main.py                     ← Training script
├── PROJECT_OVERVIEW.md         ← Full documentation
├── STREAMLIT_SETUP.md          ← App setup guide
├── requirements.txt            ← Dependencies
│
├── src/                        ← Core modules
│   ├── pipeline.py            (Main pipeline)
│   ├── preprocessing.py       (Text processing)
│   ├── clustering.py          (K-Means++)
│   ├── classification.py      (Random Forest)
│   ├── association_rules.py   (Apriori)
│   ├── recommendation.py      (Risk scoring)
│   └── features.py            (Feature engineering)
│
├── models/                     ← Trained models
│   └── fraud_detection_model_*.pkl
│
├── dataset/                    ← Training data
│   ├── sms/
│   │   └── spam.csv
│   └── email/
│       ├── phishing_email.csv
│       └── other_datasets...
│
└── results/                    ← Output results
    ├── clustering_metrics.json
    └── results_balanced.json
```

---

## 🔄 Data Flow

```
Raw Message
    ↓
Preprocessing (normalize, tokenize, extract features)
    ↓
Feature Engineering (TF-IDF + manual features)
    ↓
┌─────────────────────────────────┐
│ 3-Factor Risk Scoring           │
├─────────────────────────────────┤
│ • RF Probability (60%)          │
│ • Cluster Risk (20%)            │
│ • Rule Hits (20%)               │
└─────────────────────────────────┘
    ↓
Risk Score + Severity Alert
```

---

## 🎓 Datasets

| Dataset | Size | Purpose |
|---------|------|---------|
| **SMS Spam** | 5,574 | Fraud SMS messages |
| **Phishing Email** | Various | Phishing emails |
| **CEAS 2008** | ~4,327 | Email spam |
| **Enron** | ~16,545 | Email corpus |
| **Nigerian Fraud** | Various | Scam emails |

---

## 🔧 Configuration

### **Training Parameters**
```python
FraudDetectionPipeline(
    n_clusters=5,          # K-Means clusters
    n_estimators=300,      # RF trees
    max_features=5000,     # TF-IDF features
    min_support=0.15,      # Apriori support
)
```

### **Preprocessing**
- Language: Auto-detect (VI/EN)
- Tokenization: word_tokenize (VI), whitespace (EN)
- Entity Detection: URL, phone, money, bank accounts
- Stopwords: Removed (urgent words kept)

---

## 🚀 Deployment

### **Local**
```bash
streamlit run app.py
```

### **Streamlit Cloud** (FREE)
1. Push to GitHub
2. Connect Streamlit account
3. Deploy automatically

### **Docker**
```bash
docker build -t fraud-analyzer .
docker run -p 8501:8501 fraud-analyzer
```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Submit pull request

---

## 📝 License

MIT License - See LICENSE file

---

## 👨‍💻 Author

**Ducmanh08022004**
- GitHub: [@Ducmanh08022004](https://github.com/Ducmanh08022004)
- Project: [Khai_Pha_Cuoi_Ky](https://github.com/Ducmanh08022004/Khai_Pha_Cuoi_Ky)

---

## 🙏 Acknowledgments

- **Datasets**: CEAS, Enron, Ling, Nazario, Nigerian Fraud, SpamAssasin
- **Libraries**: scikit-learn, mlxtend, Streamlit, pytesseract
- **Inspiration**: Real-world fraud detection problems

---

## 📞 Support

| Issue | Solution |
|-------|----------|
| **Tesseract not found** | Install from [GitHub Wiki](https://github.com/UB-Mannheim/tesseract/wiki) |
| **No models available** | Run `python main.py` to train |
| **OCR errors** | Check image quality (min 300 DPI) |
| **Dependencies error** | `pip install -r requirements.txt --force-reinstall` |

---

## 📈 Roadmap

- [x] ✅ Text preprocessing
- [x] ✅ Random Forest classifier
- [x] ✅ K-Means clustering
- [x] ✅ Apriori rule mining
- [x] ✅ Streamlit UI
- [x] ✅ OCR support
- [ ] 🔄 Database integration
- [ ] 🔄 Batch processing API
- [ ] 🔄 Advanced visualizations
- [ ] 🔄 Mobile app

---

<div align="center">

**🛡️ Fraud Detection System v1.0.0**

Built with ❤️ for fraud detection

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

</div>
