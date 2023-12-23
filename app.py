from flask import Flask,request,render_template
import numpy as np
import pickle

# importing model
model = pickle.load(open('model.pkl','rb'))
sc = pickle.load(open('standscaler.pkl','rb'))
ms = pickle.load(open('minmaxscaler.pkl','rb'))

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
    N = int(request.form['Nitrogen1'])
    P = int(request.form['Phosporus1'])
    K = int(request.form['Potassium1'])
    temp = float(request.form['Temperature1'])
    humidity = float(request.form['Humidity1'])
    ph = float(request.form['Ph1'])
    rainfall = float(request.form['Rainfall1'])

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
        result = "{} is the best crop to be cultivated right there".format(crop)
        if (N<0 or P<0 or K<0 or humidity<0 or ph<0 or rainfall<0):
            result="Values can't be negative , please enter values again"
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
                result=result+", ph value is too low."
            if(ph>9.25):
                result=result+", ph value is too high."
            result=result+" Sorry, we could not determine the best crop to be cultivated with the provided data."
    
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    return render_template('index.html',result = result)




# python main
if __name__ == "__main__":
    app.run(debug=True)