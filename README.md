# DesignGuard AI — Simulation Demo
### Varroc Eureka Challenge 3.0 | Problem Statement 9
**KKS Suhith Babu** | B.Tech CSE | SRM IST Trichy | 2027

---

## Run the demo

```bash
pip install streamlit
streamlit run app.py
```

## What it demonstrates
- 6-step animated pipeline (CAD ingestion → feature extraction → RAG retrieval → LLM reasoning → anomaly detection → report)
- 3 realistic sample CAD files (bracket, headlamp housing, EV motor bracket)
- Real violation detection with severity classification (Critical / Warning / Info)
- RAG chunk retrieval simulation with similarity scores
- ML anomaly score from Isolation Forest
- Live terminal execution log
- Full validation report with LLM-generated fix suggestions

## Stack shown
LangChain · Pinecone · GPT-4o · Isolation Forest · FastAPI · PyVista · Trimesh · OpenCascade · FreeCAD API
