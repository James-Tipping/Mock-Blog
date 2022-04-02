from flask import Flask, render_template, request
import requests
import smtplib

URL = "https://api.npoint.io/1a35f570e5e64163c7e3"
outlook_email = "****@outlook.com"
outlook_password = "****"

app = Flask(__name__)

posts = requests.get(URL).json()
for post in posts:
    print(post)


@app.route("/")
def go_home():
    return render_template("index.html", posts=posts)


@app.route("/about")
def go_about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def go_contact():
    if request.method == "GET":
        return render_template("contact.html", msg_sent=False)

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        print(name, email, phone, message)

        with smtplib.SMTP("smtp-mail.outlook.com") as connection:
            connection.starttls()
            connection.login(user=outlook_email, password=outlook_password)
            connection.sendmail(
                from_addr=outlook_email,
                to_addrs="****@gmail.com",
                msg="Subject: Form Completion\n\n"
                    f"{name}, {email}, {phone}, {message}"
            )

        return render_template("contact.html", msg_sent=True)


@app.route("/form-entry", methods=["POST"])
def complete_form():
    name = request.form["name"]

    print(name)
    return f"<h1>{name}</h1>"


@app.route("/post/<int:index>")
def go_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)