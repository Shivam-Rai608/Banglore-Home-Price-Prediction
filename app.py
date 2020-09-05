# importing the necessary dependencies
from flask import Flask, render_template, request
import pickle
import os
import numpy as np



app = Flask(__name__) # initializing a flask app
@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("base.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            location = str(request.form['crim'])
            area = float(request.form['zn'])
            bathrooms = int(request.form['indus'])
            bhk= int(request.form['chas'])
            h = ["total_sqft", "bath", "bhk", "1st Block Jayanagar", "1st Phase JP Nagar", "2nd Phase Judicial Layout",
                 "2nd Stage Nagarbhavi", "5th Block Hbr Layout", "5th Phase JP Nagar", "6th Phase JP Nagar",
                 "7th Phase JP Nagar", "8th Phase JP Nagar", "9th Phase JP Nagar", "AECS Layout", "Abbigere",
                 "Akshaya Nagar", "Ambalipura", "Ambedkar Nagar", "Amruthahalli", "Anandapura", "Ananth Nagar",
                 "Anekal", "Anjanapura", "Ardendale", "Arekere", "Attibele", "BEML Layout", "BTM 2nd Stage",
                 "BTM Layout", "Babusapalaya", "Badavala Nagar", "Balagere", "Banashankari", "Banashankari Stage II",
                 "Banashankari Stage III", "Banashankari Stage V", "Banashankari Stage VI", "Banaswadi",
                 "Banjara Layout", "Bannerghatta", "Bannerghatta Road", "Basavangudi", "Basaveshwara Nagar",
                 "Battarahalli", "Begur", "Begur Road", "Bellandur", "Benson Town", "Bharathi Nagar", "Bhoganhalli",
                 "Billekahalli", "Binny Pete", "Bisuvanahalli", "Bommanahalli", "Bommasandra",
                 "Bommasandra Industrial Area", "Bommenahalli", "Brookefield", "Budigere", "CV Raman Nagar",
                 "Chamrajpet", "Chandapura", "Channasandra", "Chikka Tirupathi", "Chikkabanavar", "Chikkalasandra",
                 "Choodasandra", "Cooke Town", "Cox Town", "Cunningham Road", "Dasanapura", "Dasarahalli",
                 "Devanahalli", "Devarachikkanahalli", "Dodda Nekkundi", "Doddaballapur", "Doddakallasandra",
                 "Doddathoguru", "Domlur", "Dommasandra", "EPIP Zone", "Electronic City", "Electronic City Phase II",
                 "Electronics City Phase 1", "Frazer Town", "GM Palaya", "Garudachar Palya", "Giri Nagar",
                 "Gollarapalya Hosahalli", "Gottigere", "Green Glen Layout", "Gubbalala", "Gunjur", "HAL 2nd Stage",
                 "HBR Layout", "HRBR Layout", "HSR Layout", "Haralur Road", "Harlur", "Hebbal", "Hebbal Kempapura",
                 "Hegde Nagar", "Hennur", "Hennur Road", "Hoodi", "Horamavu Agara", "Horamavu Banaswadi", "Hormavu",
                 "Hosa Road", "Hosakerehalli", "Hoskote", "Hosur Road", "Hulimavu", "ISRO Layout", "ITPL",
                 "Iblur Village", "Indira Nagar", "JP Nagar", "Jakkur", "Jalahalli", "Jalahalli East", "Jigani",
                 "Judicial Layout", "KR Puram", "Kadubeesanahalli", "Kadugodi", "Kaggadasapura", "Kaggalipura",
                 "Kaikondrahalli", "Kalena Agrahara", "Kalyan nagar", "Kambipura", "Kammanahalli", "Kammasandra",
                 "Kanakapura", "Kanakpura Road", "Kannamangala", "Karuna Nagar", "Kasavanhalli", "Kasturi Nagar",
                 "Kathriguppe", "Kaval Byrasandra", "Kenchenahalli", "Kengeri", "Kengeri Satellite Town",
                 "Kereguddadahalli", "Kodichikkanahalli", "Kodigehaali", "Kodigehalli", "Kodihalli", "Kogilu",
                 "Konanakunte", "Koramangala", "Kothannur", "Kothanur", "Kudlu", "Kudlu Gate", "Kumaraswami Layout",
                 "Kundalahalli", "LB Shastri Nagar", "Laggere", "Lakshminarayana Pura", "Lingadheeranahalli",
                 "Magadi Road", "Mahadevpura", "Mahalakshmi Layout", "Mallasandra", "Malleshpalya", "Malleshwaram",
                 "Marathahalli", "Margondanahalli", "Marsur", "Mico Layout", "Munnekollal", "Murugeshpalya",
                 "Mysore Road", "NGR Layout", "NRI Layout", "Nagarbhavi", "Nagasandra", "Nagavara", "Nagavarapalya",
                 "Narayanapura", "Neeladri Nagar", "Nehru Nagar", "OMBR Layout", "Old Airport Road", "Old Madras Road",
                 "Padmanabhanagar", "Pai Layout", "Panathur", "Parappana Agrahara", "Pattandur Agrahara",
                 "Poorna Pragna Layout", "Prithvi Layout", "R.T. Nagar", "Rachenahalli", "Raja Rajeshwari Nagar",
                 "Rajaji Nagar", "Rajiv Nagar", "Ramagondanahalli", "Ramamurthy Nagar", "Rayasandra", "Sahakara Nagar",
                 "Sanjay nagar", "Sarakki Nagar", "Sarjapur", "Sarjapur Road", "Sarjapura - Attibele Road",
                 "Sector 2 HSR Layout", "Sector 7 HSR Layout", "Seegehalli", "Shampura", "Shivaji Nagar", "Singasandra",
                 "Somasundara Palya", "Sompura", "Sonnenahalli", "Subramanyapura", "Sultan Palaya", "TC Palaya",
                 "Talaghattapura", "Thanisandra", "Thigalarapalya", "Thubarahalli", "Thyagaraja Nagar", "Tindlu",
                 "Tumkur Road", "Ulsoor", "Uttarahalli", "Varthur", "Varthur Road", "Vasanthapura", "Vidyaranyapura",
                 "Vijayanagar", "Vishveshwarya Layout", "Vishwapriya Layout", "Vittasandra", "Whitefield",
                 "Yelachenahalli", "Yelahanka", "Yelahanka New Town", "Yelenahalli", "Yeshwanthpur"]
            loc_index = h.index(location)

            X = np.zeros(244)
            X[0] = area
            X[1] = bathrooms
            X[2] = bhk
            if loc_index >= 0:
                X[loc_index] = 1

            filename = 'House_price_prediction.pickle'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction = loaded_model.predict([X])
            # showing the prediction results in a UI
            return render_template('prediction.html', value=round(prediction[0]))

        except:
            return ('Something Went Wrong')
    else:
        return render_template('base.html')


if __name__ == "__main__":
    app.run()