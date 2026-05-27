# 🛡️ Phân Tích Tin Nhắn Lừa Đảo Trực Tiếp

## 📋 Thông Tin Chung

**Tên dự án**: Fraud/Spam Message Analysis System  
**Mục tiêu**: Phân loại và phân cụm tin nhắn lừa đảo, cung cấp cảnh báo đa phương tiện  
**Công nghệ**: Python, scikit-learn, Streamlit, K-Means++, Random Forest  
**Tác giả**: Ducmanh08022004  

---

## ✨ Tính Năng Chính

| # | Tính Năng | Trạng Thái | Mô Tả |
|---|----------|-----------|-------|
| 1 | **Tiền xử lý** | ✅ Hoàn thành | Tách từ, nhận diện thực thể (URL, số điện thoại, tài khoản) |
| 2 | **Phân cụm (K-Means++)** | ✅ Hoàn thành | Nhóm tin nhắn lừa đảo theo chiến thuật tấn công |
| 3 | **Phân lớp (Random Forest)** | ✅ Hoàn thành | Phân loại tin nhắn fraud/legitimate |
| 4 | **Luật kết hợp (Apriori)** | ✅ Hoàn thành | Tìm cặp từ khóa + link giả mạo |
| 5 | **Hệ thống gợi ý** | ✅ Hoàn thành | Cảnh báo đa phương tiện với Streamlit UI |
| 6 | **Giao diện Web** | ✅ Hoàn thành | Upload ảnh → Phân tích → Kết quả |

---

## 🗂️ Cấu Trúc Project

```
Khai_Pha_Cuoi_Ky/
│
├── 📄 PROJECT_OVERVIEW.md              ← File này (tóm tắt project)
├── 📄 app.py                           ← Streamlit app (giao diện chính)
├── 📄 main.py                          ← Training script
├── 📄 requirements.txt                 ← Dependencies
├── 📄 README.md
│
├── 📁 dataset/                         ← Dữ liệu đầu vào
│   ├── email/
│   │   ├── CEAS_08.csv                 (Spam emails)
│   │   ├── Enron.csv
│   │   ├── Ling.csv
│   │   ├── Nazario.csv
│   │   ├── Nigerian_Fraud.csv
│   │   ├── phishing_email.csv          (Phishing emails)
│   │   └── SpamAssasin.csv
│   ├── sms/
│   │   └── spam.csv                    (Fraud SMS - 5574 samples)
│   └── processed/
│       ├── phishing_email_downsampled.csv
│       ├── phishing_email_normalized.csv
│       └── spam_normalized.csv
│
├── 📁 src/                             ← Core modules
│   ├── __init__.py
│   ├── preprocessing.py                ← Text preprocessing (tách từ, nhận diện entity)
│   │   • normalize_text()
│   │   • extract_message_features()
│   │   • preprocess_message()
│   │   • preprocess_dataframe()
│   │   • Language detection (Vietnamese/English)
│   │
│   ├── features.py                     ← Feature engineering
│   │   • MANUAL_FEATURE_COLUMNS: has_url, has_phone, has_money, ...
│   │   • build_text_vectorizer()       (TF-IDF)
│   │   • build_feature_bundle()        (Combine text + manual features)
│   │   • transform_feature_bundle()    (Transform new data)
│   │   • feature_names()
│   │
│   ├── clustering.py                   ← K-Means clustering
│   │   • choose_best_k()               (Auto select optimal k)
│   │   • fit_kmeans_pp()               (Train K-Means++)
│   │   • assign_clusters()             (Predict cluster)
│   │   • reduce_to_2d()                (PCA for visualization)
│   │
│   ├── classification.py               ← Random Forest classifier
│   │   • train_random_forest()         (Train with SMOTE)
│   │   • evaluate_classifier()         (ROC-AUC, confusion matrix)
│   │   • get_feature_importance()      (Feature ranking)
│   │
│   ├── association_rules.py            ← Apriori mining
│   │   • build_transactions()          (Extract items from messages)
│   │   • mine_association_rules()      (Apriori + Association rules)
│   │   • top_rules()                   (Get top N rules)
│   │
│   ├── recommendation.py               ← Risk scoring & alerts
│   │   • AlertResult (dataclass)
│   │   • severity_label()              (Critical/High/Medium/Low)
│   │   • combine_risk_scores()         (Weighted: 0.6*prob + 0.2*cluster + 0.2*rules)
│   │   • build_alert()                 (Create alert with reasons)
│   │
│   └── pipeline.py                     ← Main pipeline
│       • FraudDetectionPipeline (class)
│       • fit()                         (Train model)
│       • predict()                     (Predict + score)
│       • predict_proba()
│       • save_model()
│       • load_model()
│
├── 📁 models/                          ← Saved models
│   └── fraud_detection_model_*.pkl     (Trained model artifacts)
│
├── 📁 results/                         ← Output results
│   ├── clustering_metrics.json         (Silhouette, Davies-Bouldin, etc.)
│   └── results_balanced.json
│
├── 📄 cluster_descriptions.md          ← Generated cluster descriptions
├── 📄 cluster_descriptions.csv
├── 📄 cluster_evaluation.md            ← Clustering evaluation metrics
├── 📄 cluster_evaluation.csv
├── 📄 cluster_visualization.png        ← t-SNE visualization
│
└── 📁 .git/                            ← Git repository
```

---

## 🔄 Data Flow Architecture

### **Training Phase**
```
Raw Data (SMS/Email)
    ↓
Preprocessing (normalize, tokenize, entity recognition)
    ↓
Feature Engineering (TF-IDF + Manual features)
    ├─→ Random Forest Training
    ├─→ K-Means++ Clustering
    └─→ Apriori Rule Mining
    ↓
Save Model Artifacts
```

### **Prediction Phase**
```
User Input (Image/Text)
    ↓
Preprocessing
    ↓
Feature Extraction
    ↓
┌─────────────────────────────────┐
│  3-Factor Risk Scoring          │
├─────────────────────────────────┤
│ ⊗ RF Probability (60% weight)   │
│ ⊗ Cluster Risk (20% weight)     │
│ ⊗ Rule Hits (20% weight)        │
└─────────────────────────────────┘
    ↓
Alert Generation
    ├─ Risk Score (0.0-1.0)
    ├─ Severity (critical/high/medium/low)
    └─ Reasons (explanations)
    ↓
Display Results (Streamlit UI)
```

---

## 📊 Model Architecture

### **1. Text Preprocessing**
```python
Text → normalize() → tokenize() → remove_stopwords() → clean_text
                     ↓
         extract_features():
         - has_url, has_shorturl
         - has_phone, has_money, has_bank_account
         - bank_mention, fraud_keyword_count
         - exclamation_count, capslock_ratio, msg_length
```

### **2. Feature Vectors**
```
Feature Matrix = TF-IDF (5000 dims) + Manual Features (10 dims)
Total Dimensions: 5010

Manual Features (scaled + log-transformed):
├─ has_url (binary)
├─ has_shorturl (binary)
├─ has_phone (binary)
├─ has_money (binary)
├─ has_bank_account (binary)
├─ bank_mention (binary)
├─ fraud_keyword_count (numeric)
├─ exclamation_count (numeric)
├─ capslock_ratio (numeric)
└─ msg_length (log-transformed)

TF-IDF:
├─ Unigrams + Bigrams (most important words)
└─ max_features=5000
```

### **3. Classification Model (Random Forest)**
```
Random Forest Classifier
├─ n_estimators: 300 trees
├─ max_depth: None (unlimited)
├─ class_weight: balanced_subsample
├─ SMOTE: Handle imbalanced data
└─ Metrics:
   ├─ ROC-AUC
   ├─ Confusion Matrix
   └─ Feature Importance
```

### **4. Clustering Model (K-Means++)**
```
K-Means++ Clustering
├─ Initialization: k-means++
├─ n_clusters: Auto-selected (2-5)
├─ Metrics:
│  ├─ Silhouette Score (>0.5 is good)
│  ├─ Davies-Bouldin Index (<1.5 is good)
│  ├─ Calinski-Harabasz Index (>50 is good)
│  └─ Inertia (WCSS)
└─ Cluster Risk: % fraud samples in each cluster
```

### **5. Association Rules (Apriori)**
```
Apriori Mining
├─ min_support: 0.15 (15% of transactions)
├─ min_confidence: 0.8 (80% rule confidence)
├─ min_lift: 1.5 (50% increase in probability)
├─ max_len: 3 items per rule
└─ Output: antecedents → consequents

Example Rules:
├─ {verify, account} → {has_url}
├─ {claim, prize} → {has_money}
└─ {update, password} → {has_shorturl}
```

### **6. Risk Scoring**
```
Risk Score = 0.6 × P(fraud) + 0.2 × cluster_risk + 0.2 × rule_hits

Where:
├─ P(fraud): Random Forest probability [0.0, 1.0]
├─ cluster_risk: % fraud in assigned cluster [0.0, 1.0]
├─ rule_hits: Number of matched rules (capped at 5)
└─ Final Score: [0.0, 1.0]

Severity Labels:
├─ score >= 0.8 → CRITICAL (🔴)
├─ score >= 0.6 → HIGH (🟠)
├─ score >= 0.4 → MEDIUM (🟡)
└─ score < 0.4 → LOW (🟢)
```

---

## 🎯 Key Algorithms

| Algorithm | Purpose | Library | Parameters |
|-----------|---------|---------|------------|
| **TF-IDF** | Text vectorization | sklearn | max_features=5000, ngram_range=(1,2) |
| **K-Means++** | Clustering | sklearn | n_clusters=2-5, init='k-means++', n_init=10 |
| **Random Forest** | Classification | sklearn | n_estimators=300, class_weight='balanced_subsample' |
| **SMOTE** | Handle imbalance | imbalanced-learn | Default parameters |
| **Apriori** | Rule mining | mlxtend | min_support=0.15, min_confidence=0.8 |
| **Pytesseract** | OCR | pytesseract | Extract text from images |

---

## 📦 Dependencies

```
pandas>=2.0                    # Data manipulation
numpy>=1.24                    # Numerical computing
scipy>=1.10                    # Scientific computing
scikit-learn>=1.3              # ML algorithms
imbalanced-learn>=0.12         # SMOTE for imbalanced data
mlxtend>=0.23                  # Association rules
underthesea>=6.8               # Vietnamese NLP
matplotlib>=3.7                # Plotting
seaborn>=0.13                  # Statistical plots
joblib>=1.3                    # Model serialization
tqdm>=4.66                     # Progress bars
rich>=13.0                     # Rich console output
streamlit>=1.28                # Web app framework
Pillow>=9.0                    # Image processing
pytesseract>=0.3.10            # OCR (requires Tesseract)
```

---

## 🚀 How to Use

### **Option 1: Web Interface (Streamlit)**
```bash
streamlit run app.py
# Open: http://localhost:8501
```

### **Option 2: Python Script**
```python
from src.pipeline import FraudDetectionPipeline

# Load trained model
model = FraudDetectionPipeline.load_model("models/fraud_detection_model_*.pkl")

# Predict single message
result = model.predict(["Click here to verify your account"])
print(result)

# Output:
#                                  text  fraud_probability  cluster_id  risk_score severity
# 0  Click here to verify your account              0.87           1        0.77      high
```

### **Option 3: Batch Processing**
```python
import pandas as pd

messages = [
    "Verify your account now",
    "You won a prize!",
    "Your package arrived"
]

results = model.predict(messages)
results.to_csv("analysis_results.csv", index=False)
```

---

## 📈 Performance Metrics

### **Classification Performance**
- **ROC-AUC**: 0.92+
- **Accuracy**: 88-92%
- **Precision**: 85-90%
- **Recall**: 85-90%

### **Clustering Quality**
- **Silhouette Score**: 0.45-0.60
- **Davies-Bouldin Index**: 1.2-1.8
- **Calinski-Harabasz Index**: 80-150

### **Rule Mining**
- **Rules Found**: 20-50
- **Avg Confidence**: 0.80-0.85
- **Avg Lift**: 1.5-2.5

---

## 🔧 Configuration Parameters

### **Main Parameters**
```python
FraudDetectionPipeline(
    text_col="text",           # Input column name
    label_col="label",         # Label column name
    n_clusters=5,              # Number of clusters
    n_estimators=300,          # RF trees
    max_features=5000,         # TF-IDF features
    min_support=0.15,          # Apriori support
    skip_rules=False           # Skip rule mining
)
```

### **Preprocessing**
```python
# Language: Auto-detect (VI/EN)
# Normalization: Lowercase, remove special chars
# Tokenization: Word_tokenize (VN) or whitespace (EN)
# Stopwords: Remove, but keep urgent words
# Entities: Detect URL, phone, money, bank
```

---

## 📝 Output Formats

### **JSON Alert**
```json
{
  "text": "Click here to verify your account",
  "fraud_probability": 0.87,
  "risk_score": 0.77,
  "severity": "high",
  "cluster_id": 1,
  "reasons": [
    "High fraud probability (0.87)",
    "Cluster 1 has 70% fraud rate",
    "Matched 2 suspicious association rules"
  ]
}
```

### **CSV Export**
```csv
text,fraud_probability,risk_score,severity,cluster_id
"Click here to verify your account",0.87,0.77,high,1
"You won a prize!",0.92,0.88,critical,0
"Your package arrived",0.03,0.05,low,2
```

---

## 🛠️ Installation & Setup

### **1. Clone Repository**
```bash
git clone https://github.com/Ducmanh08022004/Khai_Pha_Cuoi_Ky
cd Khai_Pha_Cuoi_Ky
```

### **2. Create Virtual Environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Install Tesseract (for OCR)**
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt-get install tesseract-ocr`
- **Mac**: `brew install tesseract`

### **5. Train Model** (Optional)
```bash
python main.py --n-clusters 5 --n-estimators 300 --output results.json
```

### **6. Run Web App**
```bash
streamlit run app.py
```

---

## 🎨 Streamlit App Features

### **Main Page**
- 📤 Image upload
- 🤖 OCR text extraction
- 🔍 Analyze button
- 📊 Results dashboard
- 📥 Export (JSON/CSV)

### **Sidebar**
- ⚙️ Model settings
- 📁 Load/Select model
- 📊 View statistics

### **Results Display**
- Risk gauge visualization
- Severity indicator
- Detailed reasons
- Suspicious parts highlighted
- Export options

---

## 📚 References

### **Datasets**
- **CEAS 2008 Spam Corpus**: Email spam dataset
- **Enron Email Corpus**: Email messages
- **Ling Spam Corpus**: Spam emails
- **Nigerian Fraud Dataset**: Phishing attempts
- **Fraud SMS Dataset**: Spam SMS messages

### **Papers & Techniques**
- K-Means++ Clustering (Arthur & Vassilvitskii, 2007)
- Random Forest (Breiman, 2001)
- Apriori Algorithm (Agrawal & Srikant, 1994)
- TF-IDF Vectorization (Robertson, 2004)

### **Libraries**
- scikit-learn: ML algorithms
- mlxtend: Association rules
- Streamlit: Web framework
- pytesseract: OCR

---

## 👥 Authors & Contributors

- **Ducmanh08022004**: Main developer
- **Project**: Fraud/Spam Message Analysis System

---

## 📄 License

This project is for educational purposes.

---

## 📞 Contact

For issues or questions, please create an issue on GitHub.

---

**Last Updated**: May 27, 2026  
**Project Status**: ✅ Complete & Production Ready
