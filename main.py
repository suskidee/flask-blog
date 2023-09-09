from flask import Flask, render_template, request
from flask_mailman import EmailMessage
from flask_mailman import Mail
import requests
import smtplib
email = "suskidee@gmail.com"
password = "szkpptbsaahmarjx"
api_key = "18af70187215750c3be01446d2ec8c8a"

posts = requests.get("https://api.npoint.io/9d85d7ace620756a9eb1").json()
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        from_email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        connection.ehlo()
        connection.login(email, password)
        connection.sendmail(
            from_addr=email,
            to_addrs=email,
            msg=f"subject:New message from {name}\n\nPhone no: {phone}\nEmail: {from_email}\n\n\n{message}"
        )
        return render_template("contact.html", message_sent=True)
    else:
        return render_template("contact.html", message_sent=False)


@app.route("/me")
def me():
    return render_template("me.html")


@app.route("/post/<int:index>")
def post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
