# phishing-detection-ensemble
Ensemble-based phishing detection using majority voting
Phishing Detection is done using XGBoost, Logistic Regression, and Random Forest (Majority Voting)
It utilizes three models,  **XGBoost**, **Logistic Regression**, and **Random Forest** — and combines their predictions using **majority voting** to enhance accuracy and minimize false detections.
🚀 Features
- Combines three ML models for better reliability  
- Uses majority voting to finalize predictions  
- Detects phishing URLs or websites  
- Easy to train, test, and extend
- 
🧠 Models Used
1. **XGBoost** – Handles complex relationships and gives strong performance  
2. **Logistic Regression** – Simple and interpretable baseline  
3. **Random Forest** – Great at capturing non-linear patterns  
⚙️ How It Works
1. Extract and clean features from URLs or website data  
2. Train the three models on a phishing dataset  
3. Each model makes a prediction  
4. The final result is based on majority voting (e.g., if 2 out of 3 say *phishing*, the site is marked as phishing)

---
### 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|:------|:---------:|:----------:|:-------:|:----------:|
| Logistic Regression | 0.81 | 0.81 | 0.77 | 0.78 |
| Random Forest | 0.87 | 0.87 | 0.84 | 0.85 |
| XGBoost | 0.86 | 0.86 | 0.84 | 0.85 |
| **Voting Ensemble** | **0.88–0.89** | **≈0.88** | **≈0.86** | **≈0.87** |

> Evaluation metrics are based on **test data** to measure real-world performance.

### 🧾 Confusion Matrices
| Model | Confusion Matrix |
|:------|:----------------:|
| Logistic Regression | `[[184, 16], [44, 69]]` |
| Random Forest | `[[188, 12], [29, 84]]` |
| XGBoost | `[[186, 14], [29, 84]]` |

The ensemble voting method combines the strengths of all three models, improving overall stability and reducing false predictions.
****
These results may vary based on the dataset and preprocessing
