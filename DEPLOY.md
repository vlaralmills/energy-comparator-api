# 🚀 Οδηγίες Deploy στο Render

## Βήμα 1 — GitHub Repository

1. Πήγαινε στο https://github.com/new
2. Δημιούργησε νέο repo με όνομα: `energy-comparator-api`
3. Άνοιξε Git Bash / Terminal στον φάκελο:
   `C:\Users\vlasi\Documents\energy-comparator\backend`

```bash
git init
git add .
git commit -m "Initial commit - Energy Comparator API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/energy-comparator-api.git
git push -u origin main
```

---

## Βήμα 2 — Render Web Service

1. Πήγαινε στο https://render.com
2. **New → Web Service**
3. Σύνδεσε το GitHub repo `energy-comparator-api`
4. Ρυθμίσεις:
   - **Name:** `energy-comparator-api`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free

5. Κάνε κλικ **Create Web Service**

---

## Βήμα 3 — Ενημέρωση Frontend

Μόλις το Render δώσει URL (π.χ. `https://energy-comparator-api.onrender.com`),
άνοιξε το `frontend/index.html` και άλλαξε τη γραμμή:

```js
// ΠΡΙΝ:
const API_BASE = "http://localhost:5050";

// ΜΕΤΑ:
const API_BASE = "https://energy-comparator-api.onrender.com";
```

---

## Βήμα 4 — Test

Άνοιξε browser και δοκίμασε:
- https://energy-comparator-api.onrender.com/api/health
- https://energy-comparator-api.onrender.com/api/prices

---

## ⚠️ Σημείωση για Free Plan

Το Render Free Plan "κοιμάται" μετά από 15 λεπτά αδράνειας.
Η πρώτη κλήση μετά από αδράνεια παίρνει ~30 δευτερόλεπτα.
Για production χρήση, αναβάθμισε σε Starter ($7/μήνα).

Εναλλακτικά, το frontend έχει ήδη **fallback** — αν το API δεν απαντά,
υπολογίζει τοπικά από τα hardcoded δεδομένα.
