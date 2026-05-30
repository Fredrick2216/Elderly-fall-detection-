import smtplib
import json
import os
import threading
import winsound  
import time  
from email.message import EmailMessage

class DynamicNotifier:
    def __init__(self, registry_path='patients.json'):
        self.registry_path = registry_path
        self.sender_email = "leonardfredrick2203@gmail.com" 
        self.sender_pass = "iaxx pipu dqct wwwt" 

    def get_patient_data(self, patient_id):
        try:
            with open(self.registry_path, 'r') as f:
                return json.load(f).get(patient_id)
        except: return None

    def _play_alarm(self, severity):
        """
        Distinct 5-6 second patterns for different medical events.
        """
        try:
            if severity == "LOW":
                # BENDING: 5 seconds of soft rhythmic 'reminder' beeps
                for _ in range(5):
                    winsound.Beep(800, 600) 
                    time.sleep(0.4)
            
            elif severity == "MEDIUM":
                # MISSING: 5 seconds of rapid high-pitched 'search' chirps
                for _ in range(10):
                    winsound.Beep(1500, 200)
                    winsound.Beep(1800, 200)
                    time.sleep(0.1)

            elif severity == "HIGH":
                # FALL: 5 seconds of a high-intensity 'Emergency Siren'
                for _ in range(5):
                    winsound.Beep(2500, 500) 
                    winsound.Beep(1200, 500) 
                    
        except Exception as e:
            print(f"Audio Output Error: {e}")

    # ... keep _async_send, trigger_staff_only, and trigger_emergency_all the same ...
    def _async_send(self, to_list, subject, body, priority):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(to_list)
        if priority: msg['X-Priority'] = '1'
        msg.set_content(body)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.sender_email, self.sender_pass)
                smtp.send_message(msg)
                print(f"SUCCESS: Email sent to {to_list}")
        except Exception as e: print(f"ERROR: {e}")

    def trigger_staff_only(self, patient_id, alert_type):
        data = self.get_patient_data(patient_id)
        if data:
            threading.Thread(target=self._play_alarm, args=("LOW",)).start()
            staff = data.get('staff_emails', [])
            subject = f"STAFF ALERT: {alert_type} - {data['name']}"
            body = f"Patient {data['name']} is currently: {alert_type}. Staff check required."
            threading.Thread(target=self._async_send, args=(staff, subject, body, False)).start()

    def trigger_emergency_all(self, patient_id, alert_type):
        data = self.get_patient_data(patient_id)
        if data:
            sev = "HIGH" if "FALL" in alert_type.upper() else "MEDIUM"
            threading.Thread(target=self._play_alarm, args=(sev,)).start()
            staff = data.get('staff_emails', [])
            relatives = [r['email'] for r in data.get('relatives', []) if 'email' in r]
            subject = f"!!! EMERGENCY: {alert_type} - {data['name']} !!!"
            body = f"CRITICAL: {data['name']} has been in a {alert_type} position for 15s. Staff and Family notified."
            threading.Thread(target=self._async_send, args=(staff + relatives, subject, body, True)).start()




            
