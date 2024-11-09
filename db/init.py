import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="prempred_db",
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY,'
                                 'username varchar (150) NOT NULL UNIQUE,'
                                 'acknowledge_ai boolean)'
                                 )

cur.execute('CREATE TABLE IF NOT EXISTS teams (id serial PRIMARY KEY,'
                                'full_name text NOT NULL UNIQUE,'
                                'short_name text NOT NULL,'
                                'acronym varchar(3),'
                                'color varchar(15))'
            )

cur.execute('CREATE TABLE IF NOT EXISTS gameweeks (id serial PRIMARY KEY, '
                                'number int NOT NULL UNIQUE,'
                                'end_date TIMESTAMPTZ NOT NULL)'
            )

cur.execute('CREATE TABLE IF NOT EXISTS games (id serial PRIMARY KEY,'
                                'scores JSONB NOT NULL,'
                                'started_at TIMESTAMPTZ NOT NULL,'
                                'home_team_id INT NOT NULL,'
                                'away_team_id INT NOT NULL,'
                                'gameweek_id INT NOT NULL,'
                                'CONSTRAINT fk_home_team FOREIGN KEY(home_team_id) REFERENCES teams(id),'
                                'CONSTRAINT fk_away_team FOREIGN KEY(away_team_id) REFERENCES teams(id),'
                                'CONSTRAINT fk_gameweek FOREIGN KEY(gameweek_id) REFERENCES gameweeks(id))'
            )

cur.execute('CREATE TABLE IF NOT EXISTS user_gameweek_scores (id serial PRIMARY kEY,'
                                'gameweek_id INT NOT NULL,'
                                'user_id INT NOT NULL,'
                                'score INT DEFAULT 0,'
                                'CONSTRAINT fk_gameweek FOREIGN KEY(gameweek_id) REFERENCES gameweeks(id),'
                                'CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id))'
            )

cur.execute('CREATE TABLE IF NOT EXISTS predictions (id serial PRIMARY kEY,'
                                'name text NOT NULL UNIQUE)'
            )

cur.execute('CREATE TABLE IF NOT EXISTS user_predictions (id serial PRIMARY kEY,'
                                'game_id INT NOT NULL,'
                                'prediction_id INT NOT NULL,'
                                'user_id INT NOT NULL,'
                                'ai_suggested boolean DEFAULT false,'
                                'CONSTRAINT fk_game FOREIGN KEY(game_id) REFERENCES games(id),'
                                'CONSTRAINT fk_prediction FOREIGN KEY(prediction_id) REFERENCES predictions(id),'
                                'CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id))'
            )

cur.execute('CREATE TABLE IF NOT EXISTS ai_predictions (id serial PRIMARY kEY,'
                                'game_id INT NOT NULL,'
                                'prediction_id INT NOT NULL,'
                                'user_id INT NOT NULL,'
                                'CONSTRAINT fk_game FOREIGN KEY(game_id) REFERENCES games(id),'
                                'CONSTRAINT fk_prediction FOREIGN KEY(prediction_id) REFERENCES predictions(id),'
                                'CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id))'
            )

conn.commit()

cur.close()
conn.close()