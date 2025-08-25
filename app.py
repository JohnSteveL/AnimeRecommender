from flask import Flask,render_template,request
from pipeline.prediction_pipeline import hybrid_recommendation

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    recommendations = []
    submitted = False
    user_id = ""

    if request.method =='POST':
        submitted = True
        try:
            user_id = int(request.form["UserID"])

            recommendations = hybrid_recommendation(user_id)
        except Exception as e:
            print(f"Error occured: {e}")
        
    return render_template('index.html' , recommendations=recommendations, submitted=submitted, user_id=user_id)


if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)