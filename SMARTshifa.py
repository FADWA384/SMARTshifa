import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import datetime
import pandas as pd
import numpy as np
import random
import base64
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="SMARTshifa ", page_icon="🧠", layout="centered")

# =========================
# 🌍 LANGUAGE
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "العربية"

lang = st.selectbox(
    "🌍 Language",
    ["العربية", "Français", "English", "Español"],
    index=["العربية", "Français", "English", "Español"].index(st.session_state.lang),
    label_visibility="collapsed"
)
st.session_state.lang = lang

if lang == "العربية":
    st.markdown("<div dir='rtl'>", unsafe_allow_html=True)

# =========================
# 📚 TRANSLATIONS
# =========================
translations = {
    "title": {"العربية": "🧠 سمارت شفاء و", "Français": "SMARTshifa ", "English": "SMARTshifa ", "Español": "SMARTshifa "},
    "subtitle": {"العربية": "متابعة ذكية للسكري ", "Français": "Suivi intelligent du diabète ", "English": "Smart Diabetes Tracking ", "Español": "Seguimiento inteligente de diabetes "},
    "login": {"العربية": "تسجيل الدخول", "Français": "Connexion", "English": "Login", "Español": "Iniciar sesión"},
    "signup": {"العربية": "إنشاء حساب", "Français": "Créer un compte", "English": "Sign up", "Español": "Crear cuenta"},
    "username": {"العربية": "اسم المستخدم", "Français": "Nom d'utilisateur", "English": "Username", "Español": "Usuario"},
    "password": {"العربية": "كلمة المرور", "Français": "Mot de passe", "English": "Password", "Español": "Contraseña"},
    "logout": {"العربية": "تسجيل الخروج", "Français": "Déconnexion", "English": "Logout", "Español": "Cerrar sesión"},
    "role": {"العربية": "👤 اختر الدور", "Français": "👤 Choisir le rôle", "English": "👤 Choose role", "Español": "👤 Elegir rol"},
    "patient": {"العربية": "مريض", "Français": "Patient", "English": "Patient", "Español": "Paciente"},
    "doctor": {"العربية": "طبيب", "Français": "Médecin", "English": "Doctor", "Español": "Médico"},
    "tab1": {"العربية": "📊 قياس جديد", "Français": "📊 Nouvelle mesure", "English": "📊 New Reading", "Español": "📊 Nueva medida"},
    "tab2": {"العربية": "💊 الأدوية", "Français": "💊 Médicaments", "English": "💊 Medications", "Español": "💊 Medicamentos"},
    "tab3": {"العربية": "📈 السجل", "Français": "📈 Historique", "English": "📈 History", "Español": "📈 Historial"},
    "tab4": {"العربية": "🤖 مساعد ذكي", "Français": "🤖 Assistant IA", "English": "🤖 AI Assistant", "Español": "🤖 Asistente IA"},
    "upload_bilan": {"العربية": "📤 حلل التحليلة ولا دخل يدوي", "Français": "📤 Analyser un bilan ou saisie manuelle", "English": "📤 Analyze report or manual entry", "Español": "📤 Analizar informe o entrada manual"},
    "upload_img": {"العربية": "حمل صورة التحليلة", "Français": "Uploader l'image du bilan", "English": "Upload report image", "Español": "Subir imagen del informe"},
    "manual": {"العربية": "**أو دخل يدوي**", "Français": "**Ou saisir manuellement**", "English": "**Or enter manually**", "Español": "**O introducir manualmente**"},
    "glucose_val": {"العربية": "قيمة السكر g/L", "Français": "Valeur de glycémie g/L", "English": "Glucose value g/L", "Español": "Valor de glucosa g/L"},
    "save": {"العربية": "💾 حفظ القياس", "Français": "💾 Enregistrer la mesure", "English": "💾 Save reading", "Español": "💾 Guardar medida"},
    "success_save": {"العربية": "تم الحفظ!", "Français": "Mesure enregistrée!", "English": "Reading saved!", "Español": "¡Medida guardada!"},
    "last_measure": {"العربية": "آخر قياس", "Français": "Dernière mesure", "English": "Last reading", "Español": "Última medida"},
    "age": {"العربية": "🎂 العمر", "Français": "🎂 Âge", "English": "🎂 Age", "Español": "🎂 Edad"},
    "diseases": {"العربية": "🧬 أمراض مزمنة", "Français": "🧬 Maladies chroniques", "English": "🧬 Chronic diseases", "Español": "🧬 Enfermedades crónicas"},
    "hypertension": {"العربية": "ضغط الدم", "Français": "Hypertension", "English": "Hypertension", "Español": "Hipertensión"},
    "obesity": {"العربية": "السمنة", "Français": "Obésité", "English": "Obesity", "Español": "Obesidad"},
    "kidney": {"العربية": "مرض الكلى", "Français": "Maladie rénale", "English": "Kidney disease", "Español": "Enfermedad renal"},
    "advice": {"العربية": "💡 نصائح سمارت شفاء", "Français": "💡 Conseils SMARTshifa", "English": "💡 SMARTshifa Advice", "Español": "💡 Consejos SMARTshifa"},
    "my_meds": {"العربية": "💊 الأدوية ديالي", "Français": "💊 Mes médicaments", "English": "💊 My medications", "Español": "💊 Mis medicamentos"},
    "med_name": {"العربية": "اسم الدواء", "Français": "Nom du médicament", "English": "Medication name", "Español": "Nombre del medicamento"},
    "doses": {"العربية": "عدد الجرعات فاليوم", "Français": "Nombre de prises par jour", "English": "Doses per day", "Español": "Dosis por día"},
    "hour": {"العربية": "⏰ الساعة", "Français": "⏰ Heure", "English": "⏰ Time", "Español": "⏰ Hora"},
    "add_med": {"العربية": "➕ زيد الدواء", "Français": "➕ Ajouter le médicament", "English": "➕ Add medication", "Español": "➕ Añadir medicamento"},
    "added": {"العربية": "تضاف", "Français": "ajouté", "English": "added", "Español": "añadido"},
    "med_list": {"العربية": "**لائحة الأدوية ديالي:**", "Français": "**Liste de mes médicaments :**", "English": "**My medication list:**", "Español": "**Lista de mis medicamentos:**"},
    "alarm": {"العربية": "⏰ نظام التنبيه", "Français": "⏰ Système d'alarme", "English": "⏰ Alarm system", "Español": "⏰ Sistema de alarma"},
    "alarm_info": {"العربية": "✅ التنبيهات كتخدم حتى إلا التطبيق مسدود. قبل الإذن لتحت", "Français": "✅ Les notifications fonctionnent même si l'app est fermée. Acceptez l'autorisation ci-dessous", "English": "✅ Notifications work even if app is closed. Accept permission below", "Español": "✅ Las notificaciones funcionan incluso si la app está cerrada. Acepta el permiso abajo"},
    "enable_notif": {"العربية": "🔔 فعل التنبيهات", "Français": "🔔 Activer les notifications", "English": "🔔 Enable notifications", "Español": "🔔 Activar notificaciones"},
    "no_data": {"العربية": "ما كاين حتى داتا دابا", "Français": "Aucune donnée pour le moment", "English": "No data yet", "Español": "Aún no hay datos"},
    "export_pdf": {"العربية": "📄 صدّر PDF للطبيب", "Français": "📄 Exporter en PDF pour le médecin", "English": "📄 Export PDF for doctor", "Español": "📄 Exportar PDF para el médico"},
    "soon": {"العربية": "قريباً. دير لقطة شاشة دابا", "Français": "Fonctionnalité bientôt disponible", "English": "Coming soon", "Español": "Próximamente"},
    "doc_space": {"العربية": "👨‍⚕️ فضاء الطبيب", "Français": "👨‍⚕️ Espace Médecin", "English": "👨‍⚕️ Doctor Space", "Español": "👨‍⚕️ Espacio Médico"},
    "alert_doc": {"العربية": "🚨 2.8 مليون مغربي عندهم السكر. 50% ما عارفينش!", "Français": "🚨 2,8 millions de Marocains diabétiques. 50% l'ignorent!", "English": "🚨 2.8 million Moroccans have diabetes. 50% don't know!", "Español": "🚨 ¡2,8 millones de marroquíes tienen diabetes. 50% lo ignora!"},
    "adherence": {"العربية": "نسبة الالتزام بالعلاج", "Français": "Taux d'adhérence au traitement", "English": "Treatment adherence rate", "Español": "Tasa de adherencia al tratamiento"},
    "not_adherent": {"العربية": "🚨 المريض ما ملتازمش. خطر المضاعفات x10", "Français": "🚨 Patient non adhérent. Risque de complications x10", "English": "🚨 Patient not adherent. Risk of complications x10", "Español": "🚨 Paciente no adherente. Riesgo de complicaciones x10"},
    "recommendation": {"العربية": "**التوصية:** تواصل مع المريض + بدل طريقة التذكير", "Français": "**Recommandation :** Contacter le patient + changer la méthode de rappel", "English": "**Recommendation:** Contact patient + change reminder method", "Español": "**Recomendación:** Contactar al paciente + cambiar método de recordatorio"},
    "adherent": {"العربية": "✅ المريض ملتازم", "Français": "✅ Patient adhérent", "English": "✅ Patient adherent", "Español": "✅ Paciente adherente"},
    "no_patient_data": {"العربية": "المريض ما دخل حتى داتا", "Français": "Le patient n'a pas encore saisi de données", "English": "Patient hasn't entered data yet", "Español": "El paciente aún no ha ingresado datos"},
    "evolution": {"العربية": "تطور السكر عند المريض", "Français": "Évolution de la glycémie du patient", "English": "Patient glucose evolution", "Español": "Evolución de glucosa del paciente"},
    "average": {"العربية": "المعدل العام", "Français": "Moyenne générale", "English": "General average", "Español": "Promedio general"},
    "dangerous": {"العربية": "خطير إلا > 1.8", "Français": "Dangereux si > 1.8", "English": "Dangerous if > 1.8", "Español": "Peligroso si > 1.8"},
    "normal": {"العربية": "عادي", "Français": "Normal", "English": "Normal", "Español": "Normal"},
    "ask_ai": {"العربية": "اسأل الذكاء الاصطناعي", "Français": "Demander à l'IA", "English": "Ask AI", "Español": "Preguntar a la IA"},
    "high_glucose": {"العربية": "⚠️ السكر طالع بزاف. نقص السكريات و سير للطبيب", "Français": "⚠️ Glycémie très élevée. Réduisez le sucre et consultez votre médecin", "English": "⚠️ Very high glucose. Reduce sugar and see your doctor", "Español": "⚠️ Glucosa muy alta. Reduce el azúcar y consulta a tu médico"},
    "drink_water": {"العربية": "💧 شرب الما و تمشى 30 دقيقة", "Français": "💧 Buvez de l'eau et marchez 30 minutes", "English": "💧 Drink water and walk 30 minutes", "Español": "💧 Bebe agua y camina 30 minutos"},
    "low_glucose": {"العربية": "⚠️ هبوط فالسكر! خود سكر دابا", "Français": "⚠️ Hypoglycémie! Prenez du sucre immédiatement", "English": "⚠️ Hypoglycemia! Take sugar now", "Español": "⚠️ ¡Hipoglucemia! Toma azúcar ahora"},
    "normal_glucose": {"العربية": "✅ السكر مزيان", "Français": "✅ Glycémie dans la norme", "English": "✅ Glucose normal", "Español": "✅ Glucosa normal"},
    "high_chol": {"العربية": "⚠️ الكوليسترول طالع. نقص الدهون", "Français": "⚠️ Cholestérol élevé. Réduisez les graisses saturées", "English": "⚠️ High cholesterol. Reduce saturated fats", "Español": "⚠️ Colesterol alto. Reduce grasas saturadas"},
    "walk_30": {"العربية": "🚶‍♂️ 30 دقيقة مشي كل نهار كتنقص 80% من المضاعفات", "Français": "🚶‍♂️ 30 min de marche par jour réduit 80% des complications", "English": "🚶‍♂️ 30 min daily walk reduces 80% of complications", "Español": "🚶‍♂️ 30 min de caminata diaria reduce 80% de complicaciones"},
    "reduce_salt": {"العربية": "🧂 نقص الملح لأقل من 5غ فاليوم", "Français": "🧂 Réduire le sel à < 5g par jour", "English": "🧂 Reduce salt to < 5g per day", "Español": "🧂 Reduce la sal a < 5g por día"},
    "balanced_diet": {"العربية": "🥗 ريجيم متوازن. نقص 5% من الوزن كيحسن السكر بزاف", "Français": "🥗 Régime équilibré. Perdre 5% du poids améliore fortement le diabète", "English": "🥗 Balanced diet. Losing 5% weight greatly improves diabetes", "Español": "🥗 Dieta equilibrada. Perder 5% de peso mejora mucho la diabetes"},
}

def t(key):
    return translations.get(key, {}).get(lang, key)

# =========================
# 📱 PWA + Service Worker
# =========================
st.markdown("""
<link rel="manifest" href="data:application/manifest+json,{
  'name': 'SMARTshifa PRO',
  'short_name': 'SMARTshifa',
  'start_url': '.',
  'display': 'standalone',
  'background_color': '#031525',
  'theme_color': '#0A84FF',
  'description': 'Suivi intelligent du diabète',
  'icons': [{'src': 'https://cdn-icons-png.flaticon.com/512/4006/4006511.png', 'sizes': '512x512', 'type': 'image/png'}]
}">
<meta name="theme-color" content="#0A84FF">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="SMARTshifa">
<link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/4006/4006511.png">
<script>
if ('serviceWorker' in navigator && 'Notification' in window) {
    navigator.serviceWorker.register('data:text/javascript,self.addEventListener("message",e=>{if(e.data.type==="SCHEDULE"){const t=e.data.time,r=e.data.med;setTimeout(()=>{self.registration.showNotification("SMARTshifa - وقت الدواء",{body:"وقت تاخد: "+r,icon:"https://cdn-icons-png.flaticon.com/512/4006/4006511.png",badge:"https://cdn-icons-png.flaticon.com/512/4006/4006511.png",vibrate:[200,100,200],requireInteraction:true})},t-Date.now())}})');
}
function enableNotif() {
    Notification.requestPermission().then(function(permission) {
        if (permission === "granted") {
            alert("التنبيهات تفعّلات! غادي تصوني حتى إلا التطبيق مسدود");
        }
    });
}
function scheduleNotif(med, time) {
    if (Notification.permission === "granted") {
        navigator.serviceWorker.ready.then(function(reg) {
            reg.active.postMessage({type: "SCHEDULE", med: med, time: new Date(time).getTime()});
        });
    }
}
</script>
""", unsafe_allow_html=True)

# =========================
# 🎨 خلفية اللوجو
# =========================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    img_base64 = get_base64_of_bin_file('logo.png')
    background_style = f"""
        background: linear-gradient(rgba(3, 21, 37, 0.80), rgba(3, 21, 37, 0.80)),
                    url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position:  center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    """
except:
    background_style = "background-color: #031525;"

# =========================
# 🎨 CSS
# =========================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');
    :root {{ --primary: #0A84FF; --background: #031525; --card: #0A1F3D; --text: #FFFFFF; --text-secondary: #B0C4DE; --success: #30D158; --warning: #FF9F0A; --danger: #FF3B30; }}
.stApp {{ {background_style} font-family: 'Cairo', 'Inter', sans-serif; }}
    h1, h2, h3 {{ color: var(--primary)!important; font-weight: 700!important; text-align: center; }}
    h1 {{ font-size: 2.5rem!important; text-shadow: 0 2px 10px rgba(10, 132, 255, 0.5); }}
.stButton>button {{ background: linear-gradient(135deg, var(--primary), #0077ED); color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 600; width: 100%; transition: all 0.3s ease; }}
.stButton>button:hover {{ box-shadow: 0 6px 20px rgba(10, 132, 255, 0.5); transform: translateY(-2px); }}
    button[kind="secondary"] {{background: linear-gradient(135deg, #002366, #0047AB)!important; color: white!important; border: none!important; border-radius: 12px!important; }}
.stTextInput>div>div>input,.stNumberInput>div>div>input,.stTextArea>div>textarea {{ background: rgba(10, 31, 61, 0.7); backdrop-filter: blur(10px); color: var(--text); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px; }}
.stSelectbox>div>div,.stMultiSelect>div>div {{ background: rgba(10, 31, 61, 0.7); backdrop-filter: blur(10px); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); }}
.stTabs [data-baseweb="tab-list"] {{ gap: 8px; background: rgba(10, 31, 61, 0.5); border-radius: 16px; padding: 8px; }}
.stTabs [data-baseweb="tab"] {{ height: 50px; background-color: transparent; border-radius: 12px; color: var(--text-secondary); font-weight: 600; }}
.stTabs [aria-selected="true"] {{ background-color: var(--primary); color: white; }}
.stAlert,.stSuccess,.stWarning,.stError {{ border-radius: 16px; border: none; backdrop-filter: blur(10px); }}
    div[data-testid="stSuccess"] {{ background: rgba(48, 209, 88, 0.2); border-left: 4px solid var(--success); }}
    div[data-testid="stError"] {{ background: rgba(255, 59, 48, 0.2); border-left: 4px solid var(--danger); }}
    div[data-testid="stWarning"] {{ background: rgba(255, 159, 10, 0.2); border-left: 4px solid var(--warning); }}
.glucose-card {{ background: rgba(10, 31, 61, 0.8); backdrop-filter: blur(15px); padding: 25px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center; margin: 20px 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }}
.glucose-value {{ font-size: 3rem; font-weight: 700; margin: 10px 0; }}
.glucose-label {{ font-size: 1rem; color: var(--text-secondary); }}
.stDataFrame {{ background: rgba(10, 31, 61, 0.7); backdrop-filter: blur(10px); border-radius: 16px; }}
    [data-testid="stMetric"] {{ background: rgba(10, 31, 61, 0.7); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); }}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# =========================
# 🗄️ DATABASE
# =========================
conn = sqlite3.connect("smartshifa.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS glucose (username TEXT, valeur REAL, heure TEXT, source TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS medicaments (username TEXT, nom TEXT, heures TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS historique (username TEXT, medicament TEXT, heure TEXT, statut TEXT)")
conn.commit()

# =========================
# 🔐 AUTH
# =========================
def signup(u, p):
    try:
        c.execute("INSERT INTO users VALUES (?,?)", (u, p))
        conn.commit()
        return True
    except:
        return False

def login(u, p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    return c.fetchone()

# =========================
# 🤖 AI
# =========================
def ask_ai(q, history, lang="Arabe"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('models/gemini-2.5-flash')
      
        if lang == "Français":
            instruction = "Tu es un assistant médical pour diabétiques au Maroc. Réponds en français avec des conseils médicaux simples. Ne dis jamais 'je ne suis pas médecin'."
        elif lang == "English":
            instruction = "You are a medical assistant for diabetics in Morocco. Answer in English with simple medical advice. Never say 'I am not a doctor'."
        elif lang == "Español":
            instruction = "Eres un asistente médico para diabéticos en Marruecos. Responde en español con consejos médicos simples. Nunca digas 'no soy médico'."
        else:
            instruction = "أنت مساعد طبي لمرضى السكري في المغرب. أجب بالدارجة المغربية مع نصائح صحية بسيطة. لا تقل أبدا 'أنا لست طبيب'."
      
        prompt = f"""{instruction}
      
        معلومات المريض السابقة:
        {history}
      
        سؤال المريض الحالي:
        {q}
        """
      
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# 📊 FUNCTIONS
# =========================
def analyser_donnees_medicales():
    return {"glucose": round(random.uniform(0.7, 3.5), 1), "cholesterol": random.randint(120, 300)}

def generer_recommandations(glucose, cholesterol, age, maladies):
    reco = []
    if glucose > 1.8:
        reco.append(t("high_glucose"))
        reco.append(t("drink_water"))
    elif glucose < 0.7:
        reco.append(t("low_glucose"))
    else:
        reco.append(t("normal_glucose"))
    if cholesterol > 240:
        reco.append(t("high_chol"))
    if age > 50:
        reco.append(t("walk_30"))
    if t("hypertension") in maladies:
        reco.append(t("reduce_salt"))
    if t("obesity") in maladies:
        reco.append(t("balanced_diet"))
    return reco
def ai_agent_decision(glucose):
    lang = st.session_state.get("lang", "العربية")

    if glucose > 2:
        if lang == "Français":
            return "🚨 Danger ! Consultez un médecin immédiatement"
        elif lang == "English":
            return "🚨 Danger! See a doctor immediately"
        elif lang == "Español":
            return "🚨 ¡Peligro! Consulta a un médico"
        else:
            return "🚨 خطر! سير للطبيب فوراً"

    elif glucose < 0.6:
        if lang == "Français":
            return "⚠️ Hypoglycémie ! Prenez du sucre"
        elif lang == "English":
            return "⚠️ Low sugar! Take sugar now"
        elif lang == "Español":
            return "⚠️ Hipoglucemia! Toma azúcar"
        else:
            return "⚠️ هبوط خطير! خاصك السكر دابا"

    elif glucose > 1.8:
        if lang == "Français":
            return "⚠️ Glycémie élevée, réduisez le sucre"
        elif lang == "English":
            return "⚠️ High sugar, reduce intake"
        elif lang == "Español":
            return "⚠️ Azúcar alto, reduce consumo"
        else:
            return "⚠️ السكر طالع، نقص السكريات"

    else:
        if lang == "Français":
            return "✅ Glycémie normale"
        elif lang == "English":
            return "✅ Normal glucose"
        elif lang == "Español":
            return "✅ Glucosa normal"
        else:
            return "✅ الحالة مزيانة"
# =========================
# 🧠 SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
# =========================
# 🔐 LOGIN UI
# =========================
if not st.session_state.user:
    st.title(t("title"))
    st.markdown(f'<p style="text-align:center;color:#B0C4DE">{t("subtitle")}</p>', unsafe_allow_html=True)
    mode = st.selectbox("Mode", [t("login"), t("signup")], label_visibility="collapsed")
    u = st.text_input(t("username"))
    p = st.text_input(t("password"), type="password")
    if mode == t("signup"):
        if st.button(t("signup")):
            if signup(u, p):
                st.success(t("success_save"))
            else:
                st.error("Error")
    if mode == t("login"):
        if st.button(t("login")):
            if login(u, p):
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Error")
    st.stop()

# =========================
# 🧠 MAIN APP
# =========================
st.title(t("title"))
col1, col2 = st.columns([3,1])
with col2:
    if st.button(t("logout"), type="secondary"):
        st.session_state.user = None
        st.rerun()

role = st.selectbox(t("role"), [t("patient"), t("doctor")])

# =========================
# 👤 PATIENT
# =========================
if role == t("patient"):
    onglet1, onglet2, onglet3, onglet4 = st.tabs([t("tab1"), t("tab2"), t("tab3"), t("tab4")])

    with onglet1:
        st.subheader(t("upload_bilan"))
        col1, col2 = st.columns(2)
        with col1:
            fichier_uploade = st.file_uploader(t("upload_img"), type=["jpg","png","jpeg"])
            if fichier_uploade:
                    image = Image.open(fichier_uploade)
                    st.image(image, width=200)
    if st.button("🔍 تحليل البيانات"):
            try:
                # 1. Hna fin kankhliwo l-AI i-khdem bach i-3tina 'result'
                with st.spinner('جاري التحليل...'):
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('models/gemini-2.5-flash')
                  
                    # AI Analysis
                    response = model.generate_content(["حلل هذه الصورة واستخرج قيمة السكر", image])
                    result = response.text # Hna t-creeat l-variable li kant dayra l-mochkil!
              
                # 2. Daba mlli 'result' mojoda, n-jbdou l-arqam
                import re
                match = re.search(r"(\d+\.?\d*)", result)
              
                if match:
                    glucose_val = float(match.group(1))
                    st.session_state.analyzed = True
                    st.success(f"تم استخراج القيمة: {glucose_val} g/L")
                    st.write(result)
                else:
                    st.warning("الذكاء الاصطناعي لم يجد رقماً واضحاً، تأكد من الصورة.")
                    st.write(result)

            except Exception as e:
                st.error(f"حدث خطأ: {e}")
                                                  
   
          
            with col2:
                st.write(t("manual"))
                glucose_manuel = st.number_input(t("glucose_val"), 0.1, 5.0, 1.0, 0.1)
            if st.button(t("save")):
                c.execute("INSERT INTO glucose VALUES (?,?,?,?)", (st.session_state.user, glucose_manuel, str(datetime.datetime.now()), "Manuel"))
                conn.commit()
                st.success(t("success_save"))
                st.rerun()
if st.session_state.analyzed:  # <--- هادي هي اللي غتحكم ف الظهور
    c.execute("SELECT valeur, heure, source FROM glucose WHERE username=? ORDER BY heure DESC LIMIT 10", (st.session_state.user,))
    data = [{"valeur": r[0], "heure": r[1], "source": r[2]} for r in c.fetchall()]


    if data:
                derniere = data[0]
                couleur = "#30A2FF" if derniere["valeur"] > 1.8 else "#30D158"
                st.markdown(f"""<div class="glucose-card"><div class="glucose-value" style='color:{couleur}'>{derniere["valeur"]} g/L</div><div class="glucose-label">{t('last_measure')}</div></div>""", unsafe_allow_html=True)
                df_glucose = pd.DataFrame(data)
                df_glucose["heure"] = pd.to_datetime(df_glucose["heure"])
                st.line_chart(df_glucose.set_index("heure")["valeur"])
                age = st.number_input(t("age"), 1, 100, 30)
                maladies = st.multiselect(t("diseases"), [t("hypertension"), t("obesity"), t("kidney")])
                st.subheader(t("advice"))
                for r in generer_recommandations(derniere["valeur"], 200, age, maladies):
                    st.write("•", r)

with onglet2:
        st.subheader(t("my_meds"))
        st.info(t("alarm_info"))
        components.html("""<button onclick="enableNotif()" style="background:#0A84FF;color:white;padding:12px;border:none;border-radius:12px;width:100%;font-weight:600;">🔔 فعل التنبيهات</button>""", height=60)

        with st.form("form_medicament"):
            nom_med = st.text_input(t("med_name"))
            doses = st.number_input(t("doses"), 1, 6, 1)
            heures = []
            for i in range(int(doses)):
                t_input = st.time_input(f"{t('hour')} {i+1}", key=f"heure_{i}")
                heures.append(t_input)
            if st.form_submit_button(t("add_med")):
                if nom_med:
                    heures_str = ",".join([str(h)[:5] for h in heures])
                    c.execute("INSERT INTO medicaments VALUES (?,?,?)", (st.session_state.user, nom_med, heures_str))
                    conn.commit()
                    for h in heures:
                        today = datetime.datetime.now().date()
                        notif_time = datetime.datetime.combine(today, h)
                        if notif_time < datetime.datetime.now():
                            notif_time += datetime.timedelta(days=1)
                        components.html(f"""<script>scheduleNotif("{nom_med}", "{notif_time.isoformat()}");</script>""", height=0)
                    st.success(f"{nom_med} {t('added')}")
                    st.rerun()

        c.execute("SELECT nom, heures FROM medicaments WHERE username=?", (st.session_state.user,))
        meds = c.fetchall()
        st.write(t("med_list"))
        for med in meds:
            st.write(f"💊 {med[0]} : {med[1]}")

with onglet3:
        c.execute("SELECT medicament, heure, statut FROM historique WHERE username=?", (st.session_state.user,))
        hist = c.fetchall()
        if hist:
            st.dataframe(pd.DataFrame(hist, columns=["Medicament", "Heure", "Statut"]), use_container_width=True)
        else:
            st.info(t("no_data"))
        if st.button(t("export_pdf")):
            st.warning(t("soon"))

with onglet4:
        q = st.text_input(t("ask_ai"))
        if st.button("OK"):
            c.execute("SELECT valeur FROM glucose WHERE username=? ORDER BY heure DESC LIMIT 5", (st.session_state.user,))
            history = [r[0] for r in c.fetchall()]
            lang = st.session_state.get('lang', 'Arabe')
            rep = ask_ai(q, history, lang)
            st.success(rep)

# =========================
# 👨‍⚕️ DOCTOR
# =========================
if role == t("doctor"):
    st.subheader(t("doc_space"))
    st.error(t("alert_doc"))
    c.execute("SELECT medicament, heure, statut FROM historique WHERE username=?", (st.session_state.user,))
    hist = c.fetchall()
    if hist:
        df = pd.DataFrame(hist, columns=["Medicament", "Heure", "Statut"])
        st.dataframe(df, use_container_width=True)
        total = len(df)
        pris = len(df[df["Statut"] == "Pris"])
        adherence = pris / total * 100 if total > 0 else 0
        st.metric(t("adherence"), f"{adherence:.0f}%")
        if adherence < 50:
            st.error(t("not_adherent"))
            st.write(t("recommendation"))
        else:
            st.success(t("adherent"))
    else:
        st.warning(t("no_patient_data"))

    c.execute("SELECT valeur, heure FROM glucose WHERE username=? ORDER BY heure DESC", (st.session_state.user,))
    data = c.fetchall()
    if data:
        st.subheader(t("evolution"))
        df_g = pd.DataFrame(data, columns=["valeur", "heure"])
        df_g["heure"] = pd.to_datetime(df_g["heure"])
        st.line_chart(df_g.set_index("heure")["valeur"])
        moyenne = df_g["valeur"].mean()
        st.metric(t("average"), f"{moyenne:.2f} g/L", delta=t("dangerous") if moyenne > 1.8 else t("normal"))

if lang == "العربية":
    st.markdown("</div>", unsafe_allow_html=True)
