from django.shortcuts import render
import joblib
import os
from django.conf import settings
import pandas as pd

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

    # 6. Result ko HTML page par bhejna
    return render(request, 'predictor/index.html', {'result': result})