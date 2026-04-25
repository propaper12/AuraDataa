# 🛡️ AuraData Sentinel: Autonomous Data Quality Agent

**AuraData Sentinel**, veri mühendisliği projeleriniz için geliştirilmiş, **otonom** ve **genişletilebilir** bir Veri Kalitesi Denetçisi (Sentinel) eklentisidir. Geleneksel denetçilerin aksine, sadece hata bulmakla kalmaz; **LangGraph** ve **Llama 3 / Phi-3** kullanarak hataların kök nedenini (RCA) analiz eder ve çözüm önerileri sunar.

![Status](https://img.shields.io/badge/Status-Autonomous_Agent-emerald)
![Tech](https://img.shields.io/badge/Tech-LangGraph_|_DuckDB_|_FastAPI-blue)
![Mode](https://img.shields.io/badge/Mode-Universal_Plugin-orange)

## 🚀 Öne Çıkan Özellikler

- 🤖 **Agentic Workflow:** LangGraph tabanlı otonom döngü (Denetle -> Analiz Et -> Raporla).
- 🔌 **Universal Connectors:** Kafka akışlarını, SQL veritabanlarını ve yerel dosyaları (CSV, Parquet, JSON) otonom olarak tanır ve denetler.
- ⚡ **Ultra-Fast Audit:** DuckDB motoru sayesinde milisaniyeler içinde veri sağlığı metrikleri üretir.
- 🧠 **AI-Powered RCA:** Veri kalitesindeki düşüşün nedenini yerel LLM (Ollama) ile otonom olarak açıklar.
- 🎨 **Premium UI Dashboard:** Gerçek zamanlı izleme için karanlık tema, yüksek kaliteli "Plugin" arayüzü.

## 🛠️ "Plug & Play" Entegrasyonu

AuraData'yı kendi projenize (örn: Airflow, Spark veya Kafka pipeline) bir eklenti olarak eklemek için `docker-compose.yml` dosyanıza şu bloğu eklemeniz yeterlidir:

```yaml
services:
  auradata-sentinel:
    image: propaper12/auradata:latest # Veya build: ./auradata
    container_name: auradata_sentinel
    ports:
      - "3300:8000"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
    networks: [ your-data-network ]
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

## 📖 Kullanım Senaryoları

- **Kafka Akışı İzleme:** `kafka://sales_stream` yazın; ajan canlı akışı denetler.
- **Veritabanı Sağlık Kontrolü:** `sql://orders_db` yazın; ajan şemayı ve veri tutarlılığını ölçer.
- **Dosya Denetimi:** `data/test.csv` yazın; veri profilini anlık çıkarın.

## 📦 Kurulum (Quick Start)

1. **Bağımlılıkları Kurun (Ollama):**
   ```bash
   ollama pull phi3
   ```
2. **Sistemi Başlatın:**
   ```bash
   docker-compose up --build
   ```
3. **Dashboard'a Erişin:** `http://localhost:3300`

## 👨‍💻 Geliştirici Notu (Junior to Senior Vision)
Bu proje, veri boru hatlarında (Data Pipelines) insanın manuel müdahalesini azaltmak ve veri kalitesini "otonom bir ajan" seviyesine taşımak için mimari edilmiş bir **Engineering Solution**'dır.

---
⭐ Bu projeyi beğendiyseniz "Star" vermeyi unutmayın!
🔗 **Bana Ulaşın:** [LinkedIn-Profil-Linkin]
