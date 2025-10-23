import streamlit as st
import pickle
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Phishing Detector", page_icon="🔐", layout="centered")

st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f8fafb 0%, #f0f4f8 100%);
        min-height: 100vh;
    }
    
    .detector-container {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        max-width: 600px;
        margin: 0 auto;
    }
    
    .header-section {
        text-align: center;
        margin-bottom: 2.5rem;
        border-bottom: 2px solid #f0f4f8;
        padding-bottom: 1.5rem;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 0.95rem;
        color: #8b92a9;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    .input-wrapper {
        margin-bottom: 1.5rem;
    }
    
    .input-label {
        display: block;
        font-size: 0.95rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.7rem;
        letter-spacing: 0.2px;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px !important;
        font-size: 1rem;
        background-color: #f8fafb;
        transition: all 0.3s ease;
        letter-spacing: 0.3px;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        background-color: #ffffff;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 13px 40px !important;
        font-size: 1.05rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.5px;
        width: 100%;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.45);
        border-color: #764ba2;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
    }
    
    .result-container {
        margin-top: 2rem;
        padding: 1.8rem;
        border-radius: 15px;
        animation: slideIn 0.4s ease-out;
    }
    
    .result-phishing {
        background: linear-gradient(135deg, #fee 0%, #fdd 100%);
        border-left: 4px solid #e53e3e;
    }
    
    .result-safe {
        background: linear-gradient(135deg, #e6f2ff 0%, #d4e6ff 100%);
        border-left: 4px solid #0066cc;
    }
    
    .result-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }
    
    .result-prediction {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        margin-top: 0.3rem;
    }
    
    .result-phishing .result-prediction {
        color: #c53030;
    }
    
    .result-safe .result-prediction {
        color: #0052a3;
    }
    
    .confidence-bar {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 8px;
        height: 6px;
        margin-top: 1rem;
        overflow: hidden;
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.6s ease;
    }
    
    .result-phishing .confidence-fill {
        background: linear-gradient(90deg, #e53e3e 0%, #c53030 100%);
    }
    
    .result-safe .confidence-fill {
        background: linear-gradient(90deg, #0066cc 0%, #0052a3 100%);
    }
    
    .confidence-text {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.8rem;
        letter-spacing: 0.3px;
    }
    
    .result-phishing .confidence-text {
        color: #742a2a;
    }
    
    .result-safe .confidence-text {
        color: #003366;
    }
    
    .error-box {
        background-color: #fff5f5;
        border: 2px solid #fc8181;
        border-radius: 12px;
        padding: 1.2rem;
        color: #c53030;
        font-size: 0.95rem;
        font-weight: 500;
        line-height: 1.5;
    }
    
    .features-section {
        margin-top: 1.5rem;
        padding: 1.2rem;
        background-color: #f8fafb;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .features-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    .feature-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e2e8f0;
        font-size: 0.9rem;
    }
    
    .feature-item:last-child {
        border-bottom: none;
    }
    
    .feature-label {
        color: #718096;
        font-weight: 500;
    }
    
    .feature-value {
        color: #2d3748;
        font-weight: 600;
    }
    
    .model-section {
        margin-top: 1.5rem;
        padding: 1.2rem;
        background-color: #f8fafb;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .model-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    .model-item {
        padding: 0.8rem;
        background: white;
        border-radius: 8px;
        margin-bottom: 0.8rem;
        border: 1px solid #e2e8f0;
    }
    
    .model-item:last-child {
        margin-bottom: 0;
    }
    
    .model-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .model-pred {
        font-size: 0.85rem;
        color: #667eea;
        font-weight: 600;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    [data-testid="stMarkdownContainer"] p {
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)
@st.cache_resource
def load_models():
    try:
        with open('rf_model.pkl', 'rb') as f:
            rf_model = pickle.load(f)
        with open('xgb_model.pkl', 'rb') as f:
            xgb_model = pickle.load(f)
        with open('lr_model.pkl', 'rb') as f:
            lr_model = pickle.load(f)
        with open('le_sector.pkl', 'rb') as f:
            le_sector = pickle.load(f)
        with open('le_ext.pkl', 'rb') as f:
            le_ext = pickle.load(f)
        return rf_model, xgb_model, lr_model, le_sector, le_ext
    except FileNotFoundError:
        st.error("❌ Model files not found!")
        st.stop()
def get_main_part(value):
    return str(value).split('.')[1] if '.' in str(value) else ''
def extract_main_domain(value):
    value = str(value)
    return value.rsplit('.', 1)[0] if '.' in value else value
def extract_features(domain):
    extension = get_main_part(domain)
    main_domain = extract_main_domain(domain)
    return {
        'extension': extension,
        'domain_length': len(str(main_domain)),
        'hyphen_count': str(main_domain).count('-'),
        'digit_count': sum(char.isdigit() for char in str(main_domain)),
        'word_count': len(str(main_domain).split('-'))
    }
def encode_features(features, le_ext, le_sector, sector):
    try:
        ext_encoded = le_ext.transform([features['extension']])[0]
    except:
        ext_encoded = le_ext.transform([le_ext.classes_[0]])[0]
    try:
        sector_encoded = le_sector.transform([sector])[0]
    except:
        sector_encoded = le_sector.transform(['Unknown'])[0]
    return np.array([[
        ext_encoded,
        sector_encoded,
        features['domain_length'],
        features['hyphen_count'],
        features['digit_count'],
        features['word_count']
    ]])
def ensemble_predict(rf_pred, xgb_pred, lr_pred):
    votes = [rf_pred, xgb_pred, lr_pred]
    return 1 if votes.count(1) >= 2 else 0
rf_model, xgb_model, lr_model, le_sector, le_ext = load_models()
st.markdown('<div class="detector-container">', unsafe_allow_html=True)

st.markdown("""
    <div class="header-section">
        <div class="header-title">Phishing Detector</div>
        <div class="header-subtitle">Analyze domains for phishing threats using ML</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">Domain Name</label>', unsafe_allow_html=True)
    domain = st.text_input("", placeholder="example.com", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">Sector</label>', unsafe_allow_html=True)
    sector = st.selectbox("", ["Unknown"] + sorted(list(le_sector.classes_)[:-1]), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔍 Analyze Domain", use_container_width=True):
    if not domain.strip():
        st.markdown('<div class="error-box">⚠️ Please enter a valid domain name</div>', unsafe_allow_html=True)
    else:
        features = extract_features(domain)
        feature_vector = encode_features(features, le_ext, le_sector, sector)
        
        # Get predictions
        rf_pred = rf_model.predict(feature_vector)[0]
        xgb_pred = xgb_model.predict(feature_vector)[0]
        lr_pred = lr_model.predict(feature_vector)[0]
        ensemble_pred = ensemble_predict(rf_pred, xgb_pred, lr_pred)
        
        # Get probabilities
        rf_conf = rf_model.predict_proba(feature_vector)[0]
        xgb_conf = xgb_model.predict_proba(feature_vector)[0]
        lr_conf = lr_model.predict_proba(feature_vector)[0]
        
        # Get ensemble confidence
        votes = [rf_pred, xgb_pred, lr_pred]
        vote_count = votes.count(ensemble_pred)
        ensemble_confidence = (vote_count / 3) * 100
        
        # Display result
        result_class = "result-phishing" if ensemble_pred == 1 else "result-safe"
        result_text = "🚨 PHISHING DETECTED" if ensemble_pred == 1 else "✓ NON-PHISHING"
        
        st.markdown(f"""
            <div class="result-container {result_class}">
                <div class="result-label">Analysis Result</div>
                <div class="result-prediction">{result_text}</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {ensemble_confidence}%"></div>
                </div>
                <div class="confidence-text">Ensemble Confidence: {ensemble_confidence:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="model-section">
                <div class="model-title">Individual Model Predictions</div>
        """, unsafe_allow_html=True)
        
        models_data = [
            ("Random Forest", rf_pred, rf_conf),
            ("XGBoost", xgb_pred, xgb_conf),
            ("Logistic Regression", lr_pred, lr_conf)
        ]
        
        for name, pred, conf in models_data:
            pred_text = "🚨 PHISHING" if pred == 1 else "✓ NON-PHISHING"
            confidence = float((conf[1] if pred == 1 else conf[0]) * 100)
            
            st.markdown(f"""
                <div class="model-item">
                    <div class="model-name">{name}</div>
                    <div class="model-pred">{pred_text} • {confidence:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Domain features
        st.markdown("""
            <div class="features-section">
                <div class="features-title">Domain Analysis</div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-item">
                <span class="feature-label">Domain Length</span>
                <span class="feature-value">{features['domain_length']}</span>
            </div>
            <div class="feature-item">
                <span class="feature-label">Hyphen Count</span>
                <span class="feature-value">{features['hyphen_count']}</span>
            </div>
            <div class="feature-item">
                <span class="feature-label">Digit Count</span>
                <span class="feature-value">{features['digit_count']}</span>
            </div>
            <div class="feature-item">
                <span class="feature-label">Word Count</span>
                <span class="feature-value">{features['word_count']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)