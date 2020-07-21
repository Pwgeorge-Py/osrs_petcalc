from flask import Flask, render_template, url_for, redirect, request, session, jsonify
import util.testscraper


application=Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/PetCalc', methods=['GET', 'POST'])
def login():
    error = None
    overall_probs = {}
    if request.method == 'POST':
        if request.form['btn'] == 'Login':
            if request.form['username'] == '':
                error = 'Please enter a username to autofill data'
            else:
                try:
                    user = request.form['username']
                    xpdic, kcdic = util.testscraper.fetch_data(user)
                    return render_template('PetCalc.html', error=error, username=user, overall_probs=overall_probs, **xpdic, **kcdic)
                except Exception as e:
                    error = 'Error fetching data'

        elif request.form['btn'] == 'Calc':
            all_pet_chances, overall_probs = util.testscraper.handle_calc(request.form)
            return render_template('PetCalc.html', error=error, overall_probs=overall_probs, **all_pet_chances, **request.form)

    return render_template('PetCalc.html', error=error, overall_probs=overall_probs)

@application.route('/Info')
def info():
    return render_template('info.html')


if __name__ == "__main__":
    application.run(debug=True)
