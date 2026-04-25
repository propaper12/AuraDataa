import os
from fpdf import FPDF
import yagmail
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SentinelReporter:
    """PDF rapor üretimi ve E-posta gönderimi yapan modül."""
    
    def __init__(self):
        self.report_dir = "reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def generate_pdf(self, state):
        """Ajanın bulgularını profesyonel bir PDF formatına dönüştürür."""
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(16, 185, 129) # Emerald Green
        pdf.cell(200, 10, txt="AURADATA SENTINEL - QUALITY REPORT", ln=True, align='C')
        
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(100, 100, 100)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(200, 10, txt=f"Date: {date_str}", ln=True, align='C')
        
        pdf.ln(10)
        
        # Summary Section
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt="1. EXECUTIVE SUMMARY", ln=True)
        pdf.set_font("Arial", '', 10)
        status = "STABLE" if not state.get('issue_found', False) else "CRITICAL"
        pdf.multi_cell(0, 8, txt=f"Target: {state['task']}\nStatus: {status}\nQuality Score: {state.get('quality_score', 0) * 100}%")
        
        pdf.ln(5)
        
        # Metrics Section
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="2. DETAILED METRICS", ln=True)
        pdf.set_font("Courier", '', 9)
        metrics_text = str(state.get('quality_metrics', {}))
        pdf.multi_cell(0, 5, txt=metrics_text)
        
        pdf.ln(5)
        
        # AI Analysis Section
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="3. AI AUTONOMOUS ANALYSIS (RCA)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 7, txt=state.get('analysis', 'No analysis available.'))
        
        # Save
        filename = f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.report_dir, filename)
        pdf.output(filepath)
        return filepath

    def send_email(self, filepath, state):
        """Raporu e-posta ile gönderir."""
        user_email = os.getenv("SENTINEL_EMAIL_TARGET")
        sender_email = os.getenv("SMTP_USER")
        sender_password = os.getenv("SMTP_PASS")
        
        if not all([user_email, sender_email, sender_password]):
            logger.warning("Email settings missing in .env. Skipping email dispatch.")
            return False
        
        try:
            yag = yagmail.SMTP(sender_email, sender_password)
            subject = f"🚨 AuraData Sentinel Alert: {state['task']}" if state.get('issue_found') else f"✅ AuraData Sentinel Daily Report"
            body = f"AuraData Sentinel has completed a quality audit.\n\nTarget: {state['task']}\nQuality: {state.get('quality_score', 0) * 100}%\n\nPlease find the detailed PDF report attached."
            
            yag.send(to=user_email, subject=subject, contents=body, attachments=filepath)
            logger.info(f"Report sent to {user_email}")
            return True
        except Exception as e:
            logger.error(f"Email Dispatch Failed: {e}")
            return False

reporter = SentinelReporter()
