from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-random-key'

# Configuration
PIN = '1510'  # the pin (15 Oct -> 1510)
USERNAME = 'Duncan'


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        pin = request.form.get('pin', '').strip()
        if pin == PIN:
            session['signed_in'] = True
            session['name'] = USERNAME
            return redirect(url_for('birthday'))
        else:
            error = 'Wrong pin — try again :)'
    return render_template('index.html', error=error)


@app.route('/birthday')
def birthday():
    if not session.get('signed_in'):
        return redirect(url_for('index'))
    name = session.get('name', USERNAME)
    return render_template('birthday.html', name=name)


@app.route('/message')
def message():
    if not session.get('signed_in'):
        return redirect(url_for('index'))
    name = session.get('name', USERNAME)
    return render_template('message.html', name=name)


@app.route("/memories")
def memories():
    image_folder = os.path.join(app.static_folder, "images")
    images = [img for img in os.listdir(image_folder)
              if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    return render_template("memories.html", images=images)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
