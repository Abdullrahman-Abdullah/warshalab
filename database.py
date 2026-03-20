import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

if not firebase_admin._apps:
    # 1. جلب محتوى الـ JSON من متغيرات البيئة
    firebase_info = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    
    if firebase_info:
        try:
            # تحويل النص إلى قاموس
            cert_dict = json.loads(firebase_info)
            
            # الخطوة السحرية: إصلاح الأسطر الجديدة في المفتاح الخاص
            if "private_key" in cert_dict:
                cert_dict["private_key"] = cert_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(cert_dict)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Connected Successfully on Vercel!")
        except Exception as e:
            print(f"❌ Error parsing Firebase JSON: {e}")
    else:
        # للعمل المحلي (Local)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(base_dir, "serviceAccountKey.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

db = firestore.client()
def get_db(): return db
