from flask import Flask, redirect, url_for,render_template,request,jsonify,make_response
import Content_based_Recommendation

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/tv")
def TV():
    return render_template("TVSeries.html")


@app.route("/content")
def Content():
    return render_template("Contentbased.html")


@app.route("/similarity",methods=["POST"])
def similarity():
    movie = request.form['name']
    cbr = Content_based_Recommendation.Recommendation()
    recommended_movies=cbr.get_recommendation(movie)
    return ",".join(recommended_movies)


if __name__ == "__main__":
    app.run(debug=True)
