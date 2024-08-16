# Chatbot Kebijakan Ekspor Impor
Chatbot ini dibuat untuk memudahkan masyarakat dalam mendapatkan informasi mengenai kebijakan ekspor impor terbaru yang diatur sesuai dengan peraturan kementerian. Chatbot ini dibuat dengan metode LLM RAG.

## Dataset
Dataset yang digunakan adalah 10 Peraturan Kementerian 2023-2024 seputar kebijakan dan prosedur barang ekspor-impor, tarif kepabeanan, dan lainnya.

## Model
Pre-trained model yang digunakan adalah Gemma 2 9B yang diakses melalui server Ollama. Berikut merupakan langkah untuk setup server Ollama:


1. Install Ollama melalui website resmi atau melalui terminal dengan command berikut:
```
curl -fsSL https://ollama.com/install.sh | sh
```
2. Start server Ollama dan download model Gemma 2 9B dengan command berikut:
```
ollama serve & ollama pull gemma2:latest
```

## Endpoint `/chat`
Berikut merupakan tahapan untuk testing endpoint `/chat`.
```
pip install -r requirements.txt

uvicorn api-chat:app --reload
```

Selanjutnya, akses URL https://127.0.0.0:5000/chat untuk mencoba memasukkan pertanyaan seputar kebijakan ekspor impor melalui Postman atau melalui app Streamlit dengan menjalankan command `streamlit run ui-api-chat.py`. 