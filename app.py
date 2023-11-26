from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta

# Initialize Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Score model
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    score = db.Column(db.String(10))
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

# Route for submitting scores
@app.route('/submit', methods=['POST'])
def submit_score():
    data = request.json
    new_score = Score(name=data['name'], score=data['score'])
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"message": "Score submitted successfully"}), 201

# Route for getting leaderboards (daily, weekly, monthly)
@app.route('/leaderboard/<string:period>', methods=['GET'])
def get_leaderboard(period):
    base_query = Score.query.with_entities(
        Score.name,
        func.count(Score.id).label('games_played'),
        func.sum(Score.score.cast(db.Integer)).label('total_score')
    )

    if period == 'daily':
        base_query = base_query.filter(Score.date >= datetime.utcnow().date())
    elif period == 'weekly':
        base_query = base_query.filter(Score.date >= datetime.utcnow() - timedelta(days=7))
    elif period == 'monthly':
        base_query = base_query.filter(Score.date >= datetime.utcnow() - timedelta(days=30))

    leaderboard = base_query.group_by(Score.name).all()

    # Calculate the average score
    formatted_leaderboard = []
    for entry in leaderboard:
        avg_score = entry.total_score / entry.games_played if entry.games_played > 0 else 0
        formatted_leaderboard.append({
            'name': entry.name,
            'total_score': entry.total_score,
            'games_played': entry.games_played,
            'average_score': avg_score
        })

    return jsonify(formatted_leaderboard)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Create database tables within the app context
    app.run(debug=True)
