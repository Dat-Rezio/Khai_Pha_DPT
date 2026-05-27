"""
🛡️ Fraud Message Analyzer - Streamlit Web Application
Upload an image with fraud message text to analyze
"""

# ⚠️ MUST set Tesseract path BEFORE importing pytesseract
import os
import sys
from pathlib import Path

# Configure Tesseract path for Windows - check all common locations
tesseract_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Tesseract-OCR\tesseract.exe',
]

tesseract_cmd = None
for path in tesseract_paths:
    if os.path.exists(path):
        tesseract_cmd = path
        break

import pytesseract

# Set the path to the correct attribute: tesseract_cmd (not pytesseract_cmd)
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

import streamlit as st
from PIL import Image
import json
import pandas as pd
from datetime import datetime
import numpy as np
import subprocess
from src.pipeline import FraudDetectionPipeline

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="🛡️ Fraud Message Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .severity-critical {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .severity-high {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .severity-medium {
        background: linear-gradient(135deg, #fbc02d 0%, #f57f17 100%);
    }
    
    .severity-low {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .reason-item {
        background-color: #f0f2f6;
        border-left: 4px solid #dc2626;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

# Create output directory
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR - MODEL MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    
    # Model selection
    st.subheader("🤖 Model Management")
    
    models_dir = Path("models")
    model_files = []
    
    if models_dir.exists():
        model_files = sorted(models_dir.glob("fraud_detection_model_*.pkl"))
    
    if model_files:
        selected_model = st.selectbox(
            "Available Models:",
            options=model_files,
            format_func=lambda x: x.name
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📂 Load Model", use_container_width=True):
                with st.spinner("⏳ Loading model..."):
                    try:
                        st.session_state.model = FraudDetectionPipeline.load_model(str(selected_model))
                        st.session_state.model_loaded = True
                        st.success(f"✅ Model loaded: {selected_model.name}")
                    except Exception as e:
                        st.error(f"❌ Error loading model: {str(e)}")
        
        with col2:
            if st.button("ℹ️ Model Info", use_container_width=True):
                st.info(f"**File**: {selected_model.name}\n**Size**: {selected_model.stat().st_size / 1024:.2f} KB")
    else:
        st.warning("⚠️ No trained models found. Please train a model using `main.py`")
    
    st.markdown("---")
    
    # Model status
    st.subheader("📊 Model Status")
    if st.session_state.model_loaded:
        st.success("✅ Model Ready")
        st.info(f"Loaded: {selected_model.name}")
    else:
        st.warning("⚠️ No Model Loaded")
    
    st.markdown("---")
    
    # OCR Settings
    st.subheader("🔤 OCR Settings")
    ocr_language = st.selectbox(
        "OCR Language:",
        ["eng+vie", "eng", "vie"],
        help="Language for text extraction from images"
    )
    
    st.markdown("---")
    
    # Export settings
    st.subheader("💾 Export Settings")
    export_format = st.multiselect(
        "Export Format:",
        ["JSON", "CSV"],
        default=["JSON"],
        help="Choose formats for exporting results"
    )
    
    st.markdown("---")
    
    # About
    st.subheader("ℹ️ About")
    st.markdown("""
    **Fraud Message Analyzer**
    
    Analyze fraud/spam messages using:
    - 🔄 Random Forest Classification
    - 📊 K-Means++ Clustering
    - 🔗 Association Rules Mining
    
    **Version**: 1.0.0
    **Status**: Production Ready ✅
    """)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align: center;">
    <h1>🛡️ Fraud Message Analyzer</h1>
    <p style="font-size: 18px; color: #666;">
        Upload an image with fraud message text to get instant analysis
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# CHECK MODEL STATUS
# ═══════════════════════════════════════════════════════════════════════════════

if not st.session_state.model_loaded:
    st.error("❌ Please load a model first using the sidebar!")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT - TWO COLUMNS
# ═══════════════════════════════════════════════════════════════════════════════

col1, col2 = st.columns(2)

# ═══════════════════════════════════════════════════════════════════════════════
# COLUMN 1: INPUT
# ═══════════════════════════════════════════════════════════════════════════════

with col1:
    st.subheader("📤 Step 1: Upload & Extract")
    
    # Upload area
    uploaded_file = st.file_uploader(
        "Choose an image with fraud message text",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        help="Supported formats: JPG, PNG, BMP, TIFF"
    )
    
    if uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Image", use_column_width=True)
        
        # Get image info
        img_info = f"Size: {image.size[0]}x{image.size[1]} | Format: {image.format}"
        st.caption(img_info)
        
        # Extract text button
        st.markdown("---")
        
        if st.button("🔤 Extract Text (OCR)", use_container_width=True, key="extract_btn"):
            with st.spinner("🔄 Extracting text from image..."):
                try:
                    extracted = pytesseract.image_to_string(image, lang=ocr_language)
                    st.session_state.extracted_text = extracted.strip()
                    
                    if st.session_state.extracted_text:
                        st.success("✅ Text extracted successfully!")
                        
                        # Display extracted text prominently
                        with st.expander("📝 View Extracted Text", expanded=True):
                            st.text_area(
                                "Extracted text from image:",
                                value=st.session_state.extracted_text,
                                height=150,
                                disabled=True,
                                key="extracted_text_display"
                            )
                    else:
                        st.warning("⚠️ No text found in image. Please check the image quality.")
                except pytesseract.TesseractNotFoundError:
                    st.error("""
❌ **Tesseract Not Found!**

Tesseract-OCR is not installed or not in your PATH.

**Installation Instructions:**
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Standard path: `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`
  - After installing, restart Streamlit: `streamlit run app.py`
  
- **Linux**: `sudo apt-get install tesseract-ocr`
- **Mac**: `brew install tesseract`

See [STREAMLIT_SETUP.md](STREAMLIT_SETUP.md) for detailed setup instructions.
                    """)
                except Exception as e:
                    st.error(f"""
❌ **OCR Error**: {str(e)}

**Troubleshooting:**
1. Ensure Tesseract is installed
2. Try restarting Streamlit
3. Check that image file is valid (JPG, PNG, BMP, TIF)
4. For detailed help, see STREAMLIT_SETUP.md
                    """)
    else:
        st.info("📌 Please upload an image to start")
    
    # Manual text input option
    st.markdown("---")
    st.subheader("✏️ Or Input Text Manually")
    
    manual_text = st.text_area(
        "Paste message text here:",
        value=st.session_state.extracted_text,
        height=200,
        placeholder="Paste the fraud message text here...",
        key="manual_text_input"
    )
    
    if manual_text:
        st.session_state.extracted_text = manual_text

# ═══════════════════════════════════════════════════════════════════════════════
# COLUMN 2: RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

with col2:
    st.subheader("🔍 Step 2: Analyze & Results")
    
    if st.session_state.extracted_text:
        # Analyze button
        if st.button("🚀 ANALYZE MESSAGE", use_container_width=True, key="analyze_btn"):
            with st.spinner("⏳ Analyzing message..."):
                try:
                    # Predict
                    results = st.session_state.model.predict([st.session_state.extracted_text])
                    result = results.iloc[0]
                    st.session_state.analysis_results = result
                    st.success("✅ Analysis complete!")
                except Exception as e:
                    st.error(f"❌ Analysis error: {str(e)}")
        
        # Display results if available
        if st.session_state.analysis_results is not None:
            result = st.session_state.analysis_results
            
            # Severity badge with color
            severity_colors = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢"
            }
            
            severity_emoji = severity_colors.get(result['severity'], "⚪")
            
            st.markdown("---")
            st.subheader("📊 Results")
            
            # Metrics
            metric_cols = st.columns(3)
            
            with metric_cols[0]:
                st.metric(
                    "Risk Score",
                    f"{result['risk_score']:.1%}",
                    delta=f"{int(result['risk_score']*100)}/100"
                )
            
            with metric_cols[1]:
                st.metric(
                    "Fraud Probability",
                    f"{result['fraud_probability']:.1%}",
                    delta=f"{int(result['fraud_probability']*100)}/100"
                )
            
            with metric_cols[2]:
                st.metric(
                    "Severity",
                    f"{severity_emoji} {result['severity'].upper()}",
                    delta=f"Cluster {int(result['cluster_id'])}"
                )
            
            # Risk gauge
            st.markdown("**Risk Level:**")
            severity_color = {
                "critical": "#f5576c",
                "high": "#fa709a",
                "medium": "#fbc02d",
                "low": "#00f2fe"
            }.get(result['severity'], "#999")
            
            progress_value = result['risk_score']
            st.progress(progress_value)
            
            # Detailed reasons
            st.markdown("---")
            st.subheader("⚠️ Detection Reasons")
            
            # Risk factors breakdown
            reason_cols = st.columns(2)
            
            with reason_cols[0]:
                st.info(f"""
                **Fraud Probability**: {result['fraud_probability']:.1%}
                (Random Forest Model Score)
                """)
            
            with reason_cols[1]:
                st.info(f"""
                **Cluster Risk**: {result['cluster_id']}
                (Message Type Classification)
                """)
            
            # Reasons list
            for i, reason in enumerate(result['reasons'], 1):
                st.markdown(f"""
                <div class="reason-item">
                    <strong>#{i}</strong> {reason}
                </div>
                """, unsafe_allow_html=True)
            
            # Additional info
            st.markdown("---")
            st.subheader("📋 Additional Info")
            
            additional_cols = st.columns(2)
            
            with additional_cols[0]:
                st.json({
                    "cluster_id": int(result['cluster_id']),
                    "risk_score": round(float(result['risk_score']), 4),
                    "fraud_probability": round(float(result['fraud_probability']), 4)
                })
            
            with additional_cols[1]:
                st.json({
                    "severity": result['severity'],
                    "timestamp": datetime.now().isoformat(),
                    "model_version": "1.0.0"
                })
            
            # Export results
            st.markdown("---")
            st.subheader("💾 Export Results")
            
            export_cols = st.columns(len(export_format))
            
            # Prepare export data
            export_data = {
                "message": st.session_state.extracted_text,
                "analysis": {
                    "fraud_probability": float(result['fraud_probability']),
                    "risk_score": float(result['risk_score']),
                    "severity": result['severity'],
                    "cluster_id": int(result['cluster_id']),
                    "reasons": result['reasons'].tolist() if hasattr(result['reasons'], 'tolist') else result['reasons']
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # JSON export
            if "JSON" in export_format and len(export_cols) > 0:
                with export_cols[0]:
                    json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_str,
                        file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            # CSV export
            if "CSV" in export_format and len(export_cols) > 1:
                with export_cols[1]:
                    csv_data = pd.DataFrame([{
                        "Message": st.session_state.extracted_text[:100] + "...",
                        "Risk_Score": f"{result['risk_score']:.2%}",
                        "Fraud_Probability": f"{result['fraud_probability']:.2%}",
                        "Severity": result['severity'],
                        "Cluster_ID": int(result['cluster_id']),
                        "Timestamp": datetime.now().isoformat()
                    }])
                    
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data.to_csv(index=False),
                        file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
    else:
        st.info("📌 Upload an image or paste text to analyze")

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 2rem;">
    <p>🛡️ Fraud Message Analyzer v1.0.0 | Powered by ML</p>
    <p>Built with Streamlit, scikit-learn, and K-Means++ Clustering</p>
</div>
""", unsafe_allow_html=True)

st.info("""
**💡 Tips:**
- Upload clear images of fraud messages
- Extract text using OCR or paste manually
- Click "ANALYZE MESSAGE" to get results
- Export results in JSON or CSV format
- Severity levels: 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low
""")
