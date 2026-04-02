# Industrial AQI Predictor

A Streamlit app that predicts Air Quality Index (AQI) using Polynomial Regression (Degree-3 + Ridge Regularization).

---

## ⚙️ Setup & Run

### 1. Clone / Open in VS Code
Open the `pollution_predictor/` folder in VS Code.

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your model
Copy `pollution_model.pkl` into the `model/` subfolder:
```
pollution_predictor/model/pollution_model.pkl
```

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 🔢 Inputs
| Parameter | Range | Unit |
|---|---|---|
| Production | 0 – 1000 | tons/day |
| Temperature | -10 – 50 | °C |
| Humidity | 0 – 100 | % |

## 📊 AQI Classification
| Level | AQI Range | Color |
|---|---|---|
| ✅ LOW | ≤ 150 | Green |
| ⚠️ MEDIUM | 151 – 300 | Yellow |
| 🔴 HIGH | > 300 | Red |

---

## 🧠 Model Info
- Algorithm: Polynomial Regression (Degree 3)
- Regularization: Ridge
- Input features: Production, Temperature, Humidity
- Output: Predicted AQI (continuous) → classified into 3 levels
