from flask import Flask, render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['SECRET_KEY'] = "!@#$%^&*"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'FDB'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        url = YouTube(session['link'])
        return render_template('see_video.html', url=url)
    return render_template('index.html')


@app.route('/see-video', methods=['GET', 'POST'])
def see_video():
    if request.method == 'POST':
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        filename = video.download()
        return send_file(filename, as_attachment=True)
    return redirect(url_for("index"))


@app.route('/feedback.html', methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        details = request.form
        your_name = details['name']
        email = details['email']
        comments = details['comments']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO fuser(your_name, email, comments) VALUES "
                    "(%s, %s, %s)", (your_name, email, comments))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('feedback'))
    return render_template("feedback.html")


if __name__ == '__main__':
    app.run(debug=True)
