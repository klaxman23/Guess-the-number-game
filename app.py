from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    if request.method == 'POST':
        session['secret_number'] = random.randint(1, 100)
        session['attempts'] = 0
        return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'secret_number' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            guess = int(request.form['guess'])
            session['attempts'] += 1

            if guess == session['secret_number']:
                result = f"Congratulations! You guessed the number {session['secret_number']} correctly in {session['attempts']} attempts."
                session.pop('secret_number')  # Clear session variables after the game
                session.pop('attempts')
                return render_template('result.html', result=result)
            elif guess < session['secret_number']:
                message = "Too low! Try again."
            else:
                message = "Too high! Try again."
        except ValueError:
            message = "Invalid input. Please enter a valid number."
        
        return render_template('game.html', message=message)

    return render_template('game.html', message=None)

if __name__ == '__main__':
    app.run(debug=True)
