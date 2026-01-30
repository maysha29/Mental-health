# 🧠 NeuroDiag: AI-Enhanced Mental Health Assessment
### Clinical-Grade Automated Screening System via DASS-42

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)  
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)  
![Interface](https://img.shields.io/badge/UI-Gradio-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)  
![Deployment](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

</div>

---

## 📖 Project Overview
**NeuroDiag** is a production-oriented machine learning framework built to assist clinicians and researchers with preliminary screening for **Depression, Anxiety, and Stress** using the standardized **DASS-42** instrument. The system ingests user responses, runs inference with a pre-trained model (or ensemble), and produces clinical-style, verifiable reports that include digital authentication (stamps and signature images).

NeuroDiag is designed with clinical usability in mind: clear outputs, reproducible preprocessing, bias mitigation, and optional explainability via SHAP/LIME.

---

## 🚀 Key Capabilities

- **Real-time Intelligent Inference** — Fast, clinically-oriented severity predictions using optimized ML algorithms.
- **High-Resolution Smart Reports** — Auto-generated diagnostic reports produced with `Pillow`, including dynamic text, watermarks, and verification elements.
- **Bias Mitigation** — SMOTETomek hybrid resampling to address class imbalance during training.
- **Browser UI** — User-friendly Gradio interface for non-technical interaction.
- **Explainability Support** — Integrates with SHAP / LIME for global and local feature explanations (optional).

---

## 🛠 Technical Architecture

### Repository Layout
The project uses a modular organization to separate assets, inference logic, and model artifacts:

```text
root/
├── img/                     # Digital assets for report generation
│   ├── verified.png         # Official verification stamp
│   └── signature.png        # Authorized signatory image
│
├── app.py                   # Core engine (UI layout + inference logic)
├── mental_health_models.pkl # Serialized ML model (excluded via .gitignore)
├── requirements.txt         # Dependency manifest
└── .gitignore               # Version control safety rules
```

### Machine Learning Pipeline (Summary)
- Data Source: Standardized DASS-42 dataset.
- Preprocessing:
  - Missing-value handling / imputation
  - SMOTETomek hybrid resampling for class imbalance
  - Z-score (standard) normalization for features
- Model selection and evaluation:
  - Candidates: Logistic Regression, Random Forest, LightGBM, etc.
  - Selection based on cross-validated metrics and clinical suitability
- Explainability:
  - Optional SHAP/LIME integration for feature-level explanations

---

## ⚡ Getting Started

### Prerequisites
- Python 3.10+
- Git

### Quick Install & Run
1. Clone the repository:
```bash
git clone https://github.com/maysha29/Mental-Health-Diagnostic-System.git
cd Mental-Health-Diagnostic-System
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Place the trained model file
- The file `mental_health_models.pkl` is intentionally excluded from the repository for size and security reasons. Place your trained model in the project root before running the app.

5. Launch the application:
```bash
python app.py
```
Open the interface at: `http://127.0.0.1:7860`

---

## ☁️ Deployment Recommendations
- **Hugging Face Spaces:** Suitable for rapid demos — upload `app.py`, `requirements.txt`, and `img/` assets. Note: model size limits apply.
- **Docker:** Containerize the app for consistent deployment across cloud providers (AWS/GCP/Azure).
- **External Model Storage:** Host large model artifacts (e.g., `.pkl`) on S3, GCS, or a secured file store and download at runtime to keep the repo lightweight.

---

## 🛡 Security & Reproducibility
Important files that should remain local and not be checked into source control:
- Model artifacts: `*.pkl`, `*.h5`
- Environment configs: `.env`, `venv/`
- Temporary / cache: `__pycache__/`

Reproducibility checklist:
- Keep `requirements.txt` pinned to exact versions.
- Record `random_state` seeds and cross-validation configuration in training scripts.
- Document all preprocessing steps and store training metadata (data splits, dates, model version) alongside model artifacts.

---

## 👩‍💻 Author & Acknowledgements
**Maysha Tabassum**  
Machine Learning Engineer & Researcher

This tool is intended as a decision-support system and must not be used as a standalone clinical diagnosis. Clinical oversight is required for any deployment that impacts patient care.

---

## License & Contact
Include your preferred license (e.g., MIT, Apache 2.0) and contact details for collaboration or support.

--- 

If you want, I can:
- provide a Dockerfile and example deployment manifest,
- add a model-card template and training metadata example,
- or prepare a concise "How to contribute" guide and issue templates.
```