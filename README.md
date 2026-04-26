# 🛡️ AuraData Sentinel: Enterprise-Grade Autonomous Data Quality Agent

**AuraData Sentinel**, veri mühendisliği ekosistemleri için tasarlanmış, **tam otonom** ve **gerçek zamanlı** bir Veri Kalitesi Güvenlik Katmanı'dır. Geleneksel izleme araçlarından farklı olarak AuraData; veri boru hatlarınıza (Kafka, SQL, File) bir **eklenti (plugin)** olarak takılır ve otonom kök neden analizi (RCA) yapar.

![Scale](https://img.shields.io/badge/Scale-Enterprise-blue)
![Intelligence](https://img.shields.io/badge/Intelligence-Autonomous_AI-emerald)
![Reliability](https://img.shields.io/badge/Reliability-Atomic_Health_Check-orange)

## 🔌 Kurumsal Entegrasyon (Plugin Mode)

AuraData Sentinel bir "standalone" uygulama değil, bir **Data Engineering Plugin**'dir. Mevcut `docker-compose.yml` dosyanıza şu bloğu ekleyerek sisteminize bir "denetçi" atayabilirsiniz:

```yaml
services:
  # AuraData Otonom Bekçi Eklentisi
  auradata-sentinel:
    image: propaper12/auradata-sentinel:latest # Docker Hub üzerinden saniyeler içinde çekin
    container_name: auradata_sentinel
    ports:
      - "${AURA_PORT:-3300}:8000"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASS=${SMTP_PASS}
      - SENTINEL_EMAIL_TARGET=${ALERT_EMAIL}
    networks: 
      - your_data_network # Kafka/Postgres ağınıza dahil edin
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

## 📖 Veri Kaynaklarını Bağlama Rehberi (Connection Guide)

Ajan, arayüzdeki komut satırına yazdığınız prefix'e göre otonom konnektörünü seçer:

| Kaynak Türü | Komut Formatı | Açıklama |
| :--- | :--- | :--- |
| **Kafka** | `kafka://broker:port/topic` | Canlı veri akışlarındaki null ve şema sapmalarını denetler. |
| **SQL DB** | `sql://host:port/database` | Postgres, MySQL vb. veritabanlarındaki tablo sağlığını ölçer. |
| **Local Files** | `data/filename.parquet` | Yerel CSV, Parquet veya JSON dosyalarını anlık profiller. |
| **Cloud S3** | `s3://bucket/path` | (V1.5+ Yakında) Bulut depolama alanlarını otonom tarar. |

## 🧩 Desteklenen Ekosistemler (Compatibility)

- **Pipelines:** Apache Airflow, Dagster, Prefect ile uyumlu tetiklenebilir.
- **Processing:** Spark, Flink veya dbt çıktılarını denetlemek için idealdir.
- **Storage:** MinIO, Postgres, TimescaleDB ve Kafka ekosistemlerine tam destek.
- **Platforms:** Docker Desktop (Windows/Mac) ve Linux Server ortamlarında sorunsuz çalışır.

## 🌟 Neden AuraData Sentinel?

1. **Otonom RCA:** Sadece "Hata var" demez, LLM gücüyle "Neden Var?" sorusunu teknik olarak yanıtlar.
2. **Sıfır Veri Sızıntısı:** Analiz yerel modelinizde (Ollama) yapılır, verileriniz asla internete çıkmaz.
3. **Milisaniyelik Ölçüm:** DuckDB motoru sayesinde GB'larca veriyi saniyeler içinde tarar.
4. **Zamanlanmış Denetim:** Scheduler ile her 10 dakikada bir kendi kendine denetim yapar ve PDF raporunuzu mail kutunuza atar.

## 🏁 Hızlı Başlangıç (Standalone Mode)

Eklentiyi bağımsız olarak test etmek için:
1. `ollama pull phi3`
2. `docker-compose up --build`
3. Tarayıcıdan: `http://localhost:3300`

---
⭐ **Yıldız Vererek Destek Olun:** Bu otonom çözüm veri kalitesine bakış açınızı değiştirdiyse star vermeyi unutmayın!

🔗 **LinkedIn:** [Profil Linkin]
🔗 **Medium:** [Blog Yazısı Linkin]
<img width="2794" height="1531" alt="Ekran görüntüsü 2026-04-25 163210" src="https://github.com/user-attachments/assets/fb91b061-f04a-4519-bb3c-33882791cc50" />
<img width="2679" height="1452" alt="Ekran görüntüsü 2026-04-25 163237" src="https://github.com/user-attachments/assets/80f14f03-afdf-42ac-bace-47238f10d64f" />
<img width="2789" height="1549" alt="Ekran görüntüsü 2026-04-25 163319" src="https://github.com/user-attachments/assets/02e93a04-1a78-42bc-95bb-f1625e5e62b5" />
<img width="2784" height="1550" alt="Ekran görüntüsü 2026-04-25 163203" src="https://github.com/user-attachments/assets/8839a899-f734-49e3-8319-bf41f9f6d5dc" />
