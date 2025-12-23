# Adaptive Taxonomy Mapper

![Python](https://img.shields.io/badge/python-3.9+-blue)
![Status](https://img.shields.io/badge/status-prototype-success)
![AI](https://img.shields.io/badge/AI-hybrid--inference-green)

A hybrid AI inference system that maps noisy, user-generated story tags and descriptions to a strict internal fiction taxonomy using contextual understanding, lightweight NLP, and rule-based heuristics.

---

## 📌 Problem Statement

User-generated tags are often vague or misleading (e.g., `Love`, `Scary`), while recommendation engines require high-precision internal categories such as `Enemies-to-Lovers` or `Psychological Horror`.

This project bridges that gap by:
- Prioritizing **context over tags**
- Enforcing a **strict taxonomy**
- Producing **explainable, reliable outputs**

---

## 🧠 Approach

This system uses a **hybrid AI architecture**:

- **NLP** → text normalization and signal extraction  
- **LLM (optional)** → contextual understanding (themes, setting, tone)  
- **Rule-based heuristics** → final genre decision  
- **Validation layer** → prevents hallucinations  
- **Reasoning layer** → explains every decision  

> ⚠️ LLMs never decide the final genre.

---

## ⚙️ How It Works

1. **Load taxonomy** and extract valid leaf-level genres  
2. **Analyze story text** using NLP (+ optional LLM context extraction)  
3. **Map signals → candidate genre** using heuristics  
4. **Validate output** against taxonomy  
5. **Generate reasoning** for transparency  

---

## ▶️ Running the Project

### Requirements
- Python 3.9+
- No mandatory external dependencies  
  *(Optional: `nltk` for enhanced preprocessing)*

### Run

```bash
python main.py

