from flask import Flask, render_template, url_for
import datetime

app = Flask(__name__)

@app.route("/")
def hello():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {
		'title' : 'HELLO!',
		'time' : timeString,
		'route1' : "https://stackoverflow.com/questions/45528007/flask-href-link-to-html-not-working"
		}
	return render_template('main.html', **templateData)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
