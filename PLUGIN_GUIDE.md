# AuraData Sentinel - ONE-LINE INTEGRATION GUIDE

Eğer bu projeyi başka bir projenin yanına "eklenti" olarak eklemek istersen, 
kendi docker-compose.yml dosyana şu servisi eklemen yeterli:

```yaml
services:
  # Senin Mevcut Projen
  my-data-app:
    image: my-company/app
    networks:
      - data-net

  # AuraData Otonom Gözcü (Eklenti)
  auradata-sentinel:
    image: omercakan/auradata:latest # Docker Hub'daki imajın
    ports:
      - "${AURA_PORT:-8000}:8000"    # Çakışma olursa buradan değiştirilir
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
      - DATABASE_URL=duckdb:///auradata.db
    extra_hosts:
      - "host.docker.internal:host-gateway"
    networks:
      - data-net
    volumes:
      - ./shared-data:/app/data # Veri paylaşımı için
```
