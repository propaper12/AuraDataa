class BaseConnector:
    def connect(self): raise NotImplementedError
    def fetch_sample(self): raise NotImplementedError

class KafkaConnector(BaseConnector):
    """Milisaniyelik veri akışları (Kafka) için otonom denetim eklentisi."""
    def connect(self, topic):
        print(f"Connecting to Kafka Topic: {topic}...")
        return True

    def fetch_sample(self, topic):
        # Gerçek dünyada burada broker'dan veri çekilir
        return {"id": 1, "data": "streaming_payload", "timestamp": 170000000}

class SQLConnector(BaseConnector):
    """Veritabanları için otonom denetim eklentisi."""
    def connect(self, connection_string):
        print(f"Connecting to Database...")
        return True

# Ajan bu eklentileri (plugins) otonom olarak kullanır
CONNECTOR_HUB = {
    "kafka": KafkaConnector(),
    "sql": SQLConnector(),
    "file": "DataAuditor" # Mevcut DuckDB motorumuz
}
