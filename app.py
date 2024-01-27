from flask import Flask,request,render_template
import numpy as np
import pickle

# app = Flask(__name__,template_folder=r'C:\Users\91970\Downloads\Project\Project')
# importing model
model = pickle.load(open('model.pkl','rb'))
sc = pickle.load(open('standscaler.pkl','rb'))
ms = pickle.load(open('minmaxscaler.pkl','rb'))

model1 = pickle.load(open('model1.pkl','rb'))
sc1 = pickle.load(open('standscaler1.pkl','rb'))
ms1 = pickle.load(open('minmaxscaler1.pkl','rb'))
# creating flask app
app = Flask(__name__,template_folder=r'C:\Users\91970\Downloads\Project\Project')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/index.html')
def index2():
    return render_template('index.html')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route("/predict",methods=['POST'])

def predict():
    water={"Rice":"The daily consumptive use of rice varies from 6-10 mm and total water is ranges from 1100 to 1250 mm","Maize":"Water requirement of Kharif maize is 400-550 mm while that of Rabi maize is 450-600 mm","Jute":"Jute requires about 50 cm water for its growth and development","Cotton":"Cotton is a water-intensive crop that requires 700–1300 mm of water to meet its water requirements. This is roughly 40,000 liters per day over a six-month life cycle."
,"Coconut":"water requirement of coconut ranges from 80–120 liters per tree per day, depending on the location. ","Papaya":"In case of young seedlings Water once or twice a week.In case of established plants  Water no more than once every three or four days if planted in loam.In areas with limited rainfall, growers may need to supply up to 10 gallons (38 liters) of water per tree daily during the fruit-bearing period.","Orange":"One-year-old orange trees need 9 liters of water per day, while four-year-old trees need 40 liters per day.Mature orange trees need 60–170 liters of water per day.","groundnuts":"groundnut cultivation requires an average of 420–820 millimeters of water for its entire growth period.","Muskmelon":"Muskmelons require one to two inches of water per week.","Watermelon":"watermelon needs 3400-4600m3 water per hectare.","Grapes":"Grapes cultivation requires an average of 800 millimeters of water for its entire growth period.","Banana":"Water requirement of banana has been worked out to be 1,800 – 2,000 mm per annum. In winter, irrigation is provided at an interval of 7-8 days while in summer it should be given at an interval of 4-5 days.","Pomegranate":"They estimated the age-wise water requirement (l/day/tree) of pomegranate that ranged from 1.33 to 3.40 in the 1st year, 5.13 to 12.13 in the 2nd year, 14.63 to 35.70 in the 3rd year, 20.90 to 51.00 in the 4th year and 27.14 to 66.30 in the 5th year.","Lentil":"Lentil cultivation requires an average of 450 millimeters of water for its entire growth period.","Blackgram":"Blackgram cultivation requires an average of 500 millimeters of water for its entire growth period.","Mungbean":"Mungbean cultivation requires an average of 500 millimeters of water for its entire growth period.","Mothbeans":"Mothbeans cultivation requires an average of 500 millimeters of water for its entire growth period.","Pigeonpeas":"Pigeonpeas cultivation requires an average of 600 millimeters of water for its entire growth period.","Kidneybeans":"Kidneybeans cultivation requires an average of 500 millimeters of water for its entire growth period.","Chickpeas":"Chickpeas cultivation requires an average of 440 millimeters of water for its entire growth period.","Coffee":"Coffee cultivation requires an average of 1500 millimeters of water for its entire growth period."}
    c=str(request.form['choice'])
    N = int(request.form['Nitrogen1'])
    P = int(request.form['Phosporus1'])
    K = int(request.form['Potassium1'])
    temp = float(request.form['Temperature1'])
    humidity = float(request.form['Humidity1'])
    ph = float(request.form['Ph1'])
    rainfall = float(request.form['Rainfall1'])
    if(c=='no' or c=='No' or c=="NO"):
        feature_list = [N, P, K, temp, humidity, ph]
        single_pred = np.array(feature_list).reshape(1, -1)
        scaled_features = ms1.transform(single_pred)
        final_features = sc1.transform(scaled_features)
        prediction = model1.predict(final_features)
    else:
        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)
        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange", 8: "groundnuts", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpeas", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        if(crop=='Mango'):
            req="The young mango plants require 9-12 litre/day/plant water for better growth. The plants of 3-6 years, 6-10 years, 9-12 years and full grown trees require approximately 30-35 litre, 50-60 litre, 80-90 litre and 120 litre/day/plant."
        else:
            req=water[crop]
        result = "{} is the best crop to be cultivated right there , {}".format(crop,req)
        if (N<0 or P<0 or K<0 or humidity<0 or ph<0 or rainfall<0):
            result="Values can't be negative , please enter values again."
        elif(N<10 and P<5 and K<5):
            result="Nitrogen,pottasium and phosporus values are very low."
            result=result+" Sorry, we could not determine the best crop to be cultivated with the provided data."
        elif(N>140):
            result="Nitrogen content is too high "
            if(K>205):
                result=result+", Pottasium content is too high"
            if(P>145):
                result=result+", Phosporus content is too high "
            if(ph<4.25):
                result=result+", ph value is too low "
            if(ph>9.25):
                result=result+", ph value is too high "
            result=result+" Sorry, we could not determine the best crop to be cultivated with the provided data."
        elif(K>200):
            result="Pottasium content is too high "
            if(P>145):
                result=result+", Phosporus content is too high."
            if(ph<4.25):
                result=result+", ph value is too low "
            if(ph>9.25):
                result=result+", ph value is too high "
            result=result+" Sorry, we could not determine the best crop to be cultivated with the provided data."
        elif(P>145):
            result="Phosporus content is too high "
            if(ph<4.25):
                result=result+", ph value is too low."
            elif(ph>9.25):
                result=result+", ph value is too high."
            else:
                result="Phosporus content is too high."
            result=result+" Sorry, we could not determine the best crop to be cultivated with the provided data."
        elif(ph<4.25 or ph>9.25):
            if(ph<4.25):
                result="ph value is too low."
            if(ph>9.25):
                result="ph value is too high."
            result=result+" Sorry, we could not determine the best crop to be cultivated with the provided data."
        elif(c=='Yes' or c=='yes' or c=='YES'):
            if(rainfall<30):
                result="Sorry expected rainfall is too low , we cannot suggest a crop"
        elif(c.lower()!='yes' and c.lower()!='no'):
            result="please enter either Yes or No"
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    return render_template('index.html',result = result)




# python main
if __name__ == "__main__":
    app.run(debug=True)