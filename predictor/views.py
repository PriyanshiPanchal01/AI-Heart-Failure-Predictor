from django.shortcuts import render
import joblib
import os
from django.conf import settings
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from datetime import datetime
# 1. Model ko load karna (Taki baar-baar load na karna pade)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictor', 'ml_models', 'heart_model.pkl')
model = joblib.load(MODEL_PATH)

def home(request):
    result = None
    
    # Agar user ne form submit kiya hai
    if request.method == 'POST':
        try:
            # 2. Form se saara data nikalna
            data = [[
                float(request.POST.get('age', 0)),
                int(request.POST.get('anaemia', 0)),
                float(request.POST.get('creatinine_phosphokinase', 0)),
                int(request.POST.get('diabetes', 0)),
                float(request.POST.get('ejection_fraction', 0)),
                int(request.POST.get('high_blood_pressure', 0)),
                float(request.POST.get('platelets', 0)),
                float(request.POST.get('serum_creatinine', 0)),
                float(request.POST.get('serum_sodium', 0)),
                int(request.POST.get('sex', 0)),
                int(request.POST.get('smoking', 0)),
                float(request.POST.get('time', 0))
            ]]
            
            # 3. Data ko Dataframe mein badalna (Kyunki humne model dataframe par train kiya tha)
            columns = ['age', 'anaemia', 'creatinine_phosphokinase', 'diabetes', 
                       'ejection_fraction', 'high_blood_pressure', 'platelets', 
                       'serum_creatinine', 'serum_sodium', 'sex', 'smoking', 'time']
            df = pd.DataFrame(data, columns=columns)
            
            # 4. Model se prediction karwana
            prediction = model.predict(df)
            
            # 5. Result set karna
            if prediction[0] == 1:
                result = "⚠️ High Risk of Heart Failure"
            else:
                result = "✅ Low Risk of Heart Failure"
                
        except Exception as e:
            result = f"Error: Sahi details dalein."
    # Yahan session mein data save karein
        request.session['pdf_data'] = {
            'result': result,
            'date': datetime.now().strftime('%d-%m-%Y %H:%M')
            # Agar aapko age ya BP bhi chahiye toh yahan add kar sakti hain
        }
    # 6. Result ko HTML page par bhejna
    return render(request, 'predictor/index.html', {'result': result})

def generate_report(request):
    # 1. Response setup (browser ko batane ke liye ki ye PDF hai)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Heart_Health_Report.pdf"'

    # 2. PDF "Canvas" taiyar karna
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # --- Header Decoration ---
    p.setFillColorRGB(0.1, 0.4, 0.7)  # Blue color
    p.rect(0, height-80, width, 80, fill=1)
    p.setFillColorRGB(1, 1, 1)  # White text
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height-50, "AI HEART HEALTH ANALYSIS REPORT")

    # --- Patient Details ---
    p.setFillColorRGB(0, 0, 0)  # Black text
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height-120, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    p.drawString(50, height-140, "Platform: priyanshipanchal.com AI Diagnostics")
    p.line(50, height-150, 550, height-150)
    # --- Session se Asli Data Nikalein ---
    session_data = request.session.get('pdf_data', {})
    asli_result = session_data.get('result', 'No Prediction Found')
    # Symbols hatane ke liye
    clean_result = asli_result.replace("⚠️", "").replace("✅", "").strip()
    asli_date = session_data.get('date', 'N/A')
    
    # --- Analysis Result Section ---
    p.setFillColorRGB(0, 0, 0) # Black color
    p.setFont("Helvetica", 12)
    p.drawString(70, height - 180, "Analysis summary for the submitted patient metrics:")
    
    # Final Prediction Text (Red Color for High Risk / Green for Low Risk)
    p.setFont("Helvetica-Bold", 14)
    if "High" in asli_result:
        p.setFillColorRGB(0.8, 0.1, 0.1) # Red
    else:
        p.setFillColorRGB(0.1, 0.5, 0.1)
    p.drawString(70, height - 210, f"PREDICTION: {clean_result}")

    # Footer / Disclaimer ke upar detail
    p.setFillColorRGB(0, 0, 0) # Back to Black
    p.setFont("Helvetica-Oblique", 9)
    p.drawString(50, 130, f"Note: This analysis was performed on {asli_date}")
   
    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 100, "*Disclaimer: This is an AI-generated report and not a medical prescription.")

    # 3. PDF Close
    p.showPage()
    p.save()
    return response