import duckdb
import os

class DataAuditor:
    """DuckDB kullanarak verileri otonom denetleyen motor."""
    
    def __init__(self, db_path="auradata.db"):
        self.db_path = db_path

    def audit_file(self, file_path):
        """Dosya üzerinde otonom kalite testi yapar."""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        try:
            # DuckDB ile direkt dosya üzerinden sorgu
            con = duckdb.connect(database=':memory:')
            
            # 1. Genel istatistikler
            total_rows = con.execute(f"SELECT COUNT(*) FROM '{file_path}'").fetchone()[0]
            
            # 2. Kolon bazlı analiz (Null taraması)
            cols_info = con.execute(f"DESCRIBE SELECT * FROM '{file_path}'").fetchall()
            null_metrics = {}
            
            for col in cols_info:
                col_name = col[0]
                null_count = con.execute(f"SELECT COUNT(*) FROM '{file_path}' WHERE \"{col_name}\" IS NULL").fetchone()[0]
                null_metrics[col_name] = (null_count / total_rows) * 100 if total_rows > 0 else 0

            # 3. Kalite Puanı Hesaplama (Basit Algoritma)
            # Örneğin: Toplam hata payı üzerinden 100 üzerinden puan
            avg_null_rate = sum(null_metrics.values()) / len(null_metrics) if null_metrics else 0
            quality_score = max(0, (100 - (avg_null_rate * 5)) / 100) # Her %1 null puanı 5 birim düşürür

            return {
                "total_rows": total_rows,
                "null_rates": null_metrics,
                "quality_score": quality_score,
                "status": "Success"
            }
        except Exception as e:
            return {"error": str(e), "status": "Failed"}

# Singleton instance
auditor = DataAuditor()
