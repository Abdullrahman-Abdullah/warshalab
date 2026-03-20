import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# تحميل الإعدادات من ملف .env
load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
# قراءة المسار من ملف البيئة، وإذا لم يوجد يستخدم المسار الافتراضي
cred_path = os.getenv("FIREBASE_KEY_PATH", os.path.join(base_dir, "serviceAccountKey.json"))

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Connection: SECURE & ACTIVE")
    except Exception as e:
        print(f"❌ Firebase Error: {e}")

db = firestore.client()

def get_db():
    return db