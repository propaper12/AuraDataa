from kafka import KafkaConsumer
import json

class BaseConnector:
    def connect(self, target): raise NotImplementedError
    def fetch_sample(self, target): raise NotImplementedError

class KafkaConnector(BaseConnector):
    """Milisaniyelik veri akışları (Kafka) için otonom denetim eklentisi."""
    def connect(self, topic):
        # Kafka bağlantısını test et (Opsiyonel)
        return True

    def fetch_sample(self, topic):
        """Broker'dan son mesajları çeker ve örneklem oluşturur."""
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=['kafka:29092'],
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                consumer_timeout_ms=3000, # 3 saniye örnek bekleme
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            
            samples = []
            for message in consumer:
                samples.append(message.value)
                if len(samples) >= 10: break # En son 10 mesajı örnekle
            
            consumer.close()
            return samples
        except Exception as e:
            print(f"Kafka Error: {e}")
            return []

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
