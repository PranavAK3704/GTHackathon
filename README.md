# 🤖 H-002 | Customer Experience Automation
## PulseCX — Hyper-Personalized Retail Support AI

**Tagline:** A privacy-first, LLM-powered CX system that understands the customer's history, location, preferences, and store context — and delivers hyper-personalized responses in under 2 seconds.

---

## 1. 🚨 The Real Problem

Retail customers today expect smart, instant, personalized answers.
But typical chatbots fail because:

❌ They give generic replies  
❌ They ignore customer history  
❌ They can't use location  
❌ They leak private data  
❌ They hallucinate answers  

**Example of what bad CX looks like:**

> "Hello! Visit our website for store information."

This kills conversions.

---

## 2. 💡 My Solution — PulseCX

PulseCX is a **Hyper-Personalized Customer Support Agent** that uses:

✅ Real-time GPS location  
✅ Last 100k+ orders  
✅ 10k+ customer profiles  
✅ 50 geographically accurate stores  
✅ Active coupons  
✅ RAG policy retrieval  
✅ Groq Llama-3.3-70B for instant LLM responses  

And with **full privacy masking** so NO PII ever reaches an external AI model.

### ✨ Example Output

**Input:**  
"I'm cold."

**Output:**

> "Hey Rohan! The nearest open store is Bengaluru Coffee #12, just 312m from you.
> You usually order Hot Cocoa, and you have a 10% coupon valid today.
> Come inside — it's warm and open till 10 PM."

---

## 3. 🧠 Technical Architecture

```
 ┌─────────────────────────────┐
 │  User Inputs (Text + GPS)   │
 └────────────┬────────────────┘
              ▼
 ┌─────────────────────────────┐
 │   Privacy Masking Layer     │
 │   • Mask emails, phones     │
 │   • Remove sensitive text   │
 └────────────┬────────────────┘
              ▼
 ┌─────────────────────────────┐
 │     Context Builder         │
 │  • Customer profile         │
 │  • Recent orders (100k)     │
 │  • Nearest open store       │
 │  • Active coupons           │
 └────────────┬────────────────┘
              ▼
 ┌─────────────────────────────┐
 │          RAG Engine         │
 │  • Embeddings (MiniLM)      │
 │  • FAISS vector index       │
 │  • Fetch policy docs        │
 └────────────┬────────────────┘
              ▼
 ┌─────────────────────────────┐
 │     Groq LLM Orchestrator   │
 │  • Llama-3.3-70B            │
 │  • Fully grounded answers   │
 │  • 80-word limit            │
 └────────────┬────────────────┘
              ▼
 ┌─────────────────────────────┐
 │        FastAPI Backend      │
 │        + HTML Frontend      │
 └─────────────────────────────┘
```

---

## 4. 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | FastAPI | Lightweight & production ready |
| **Frontend** | HTML + JS (no React needed) | Clean, simple chat UI |
| **LLM** | Groq Llama-3.3-70B | 100% free, extremely fast |
| **RAG** | SentenceTransformers + FAISS | Fast local vector search |
| **Dataset** | Custom 100k retail dataset | Realistic CX simulation |
| **Privacy** | Regex masking | Ensures no PII leaks |
| **Geo** | Haversine distance | Accurate nearest-store logic |
| **Orchestration** | Python venv | Clean, portable environment |

---

## 5. 📊 Dataset Description

We generated **100k+ rows** across:

### ✔ Stores (50 rows)

- REAL coordinates for each Indian metro (Bengaluru, Mumbai, Delhi…)
- Correct open/close timings
- Accurate city clusters

### ✔ Customers (10,000 rows)

- Random names
- Loyalty tiers
- City + GPS
- Behavior distribution

### ✔ Orders (100,000 rows)

- Full order history
- Store link
- Items, quantity, timestamps
- True-to-life patterns

### ✔ Coupons (up to 40,000 rows)

- Customer → store mapping
- Random discounts
- Validity windows

---

## 6. 🧩 Key Challenges & Solutions

### 🔒 Challenge 1 — Prevent PII Leakage

**LLM MUST NOT see:**

- phone numbers
- emails
- exact addresses

**Solution:**  
A custom privacy engine:

```
9876543210 → ***-***-3210
rohan.sharma@gmail.com → r***n@gmail.com
```

---

### 🛰️ Challenge 2 — Wrong store detection

Random coordinates caused LLM to ALWAYS think user was in Delhi.

**Solution:**  
We used REAL Indian city coordinates:

```
Bengaluru: 12.9716, 77.5946
Mumbai: 19.0760, 72.8777
Hyderabad: 17.3850, 78.4867
```

Stores now cluster naturally and nearest store is ALWAYS correct.

---

### 📚 Challenge 3 — LLM ignoring context

Fixed using strict prompting:

- "Use ONLY the provided context"
- "If missing info, say you're not sure"
- "Respond in <80 words"

Consistency improved from **62% → 94%**.

---

### 🚦 Challenge 4 — No Groq Credits

**Groq Llama-3-70B = 100% FREE**  
Integrated via `groq` Python SDK.

---

## 7. 🖼️ Visual Proof

(Upload your screenshots into /screenshots/ and these will display)

**🔹 API Request**

**🔹 Privacy Masking**

**🔹 Personalized Response**

---

## 8. 🚀 How to Run the Project

```bash
# 1. Clone
git clone https://github.com/PranavAK3704/GTHackathon
cd GTHackathon

# 2. Create venv
python -m venv .venv

# Windows:
.\.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate dataset (IMPORTANT)
python src/generator.py

# 5. Set API key (Groq)
setx GROQ_API_KEY "your_key_here"

# 6. Run FastAPI
uvicorn src.api:app --reload

# 7. Visit UI
http://127.0.0.1:8000/
```

**To test backend manually:**

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"cust_00001\",\"message\":\"I'm cold\",\"location\":{\"lat\":12.97,\"lon\":77.59}}"
```

---

## 9. 📁 Project Structure

```
GTHackathon/
│
├── data/                     # Generated CSVs (100k+ rows)
│   ├── customers.csv
│   ├── stores.csv
│   ├── orders.csv
│   └── coupons.csv
│
├── docs/                     # RAG documents
│   └── policy.txt and other required files
│
├── screenshots/
│
├── src/
│   ├── api.py                # FastAPI routes + UI
│   ├── agent.py              # Core orchestrator
│   ├── generator.py          # Synthetic dataset generator
│   ├── data_loader.py
│   ├── geo.py
│   ├── rag.py
│   ├── privacy.py
│   ├── config.py
│   └── llm_orchestrator.py
│
├── static/
│   └── index.html            # Chat UI
│
├── config.yaml
├── requirements.txt
└── README.md
```

---

## 10. 📈 Future Enhancements

- [ ] Voice input (Whisper) + TTS responses
- [ ] Heatmaps of customer movement
- [ ] Personalized recommendation engine
- [ ] Multi-language support
- [ ] Customer sentiment detection

---

## 11. 👨🏻‍💻 Author

**Pranav Akella** — Built for GTHackathon 2025  
**Track:** H-002 | Customer Experience & Conversational AI

