from flask import Flask, render_template, request, redirect, url_for, session
import random
from wonderwords import RandomWord

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

class WordGame:
    def __init__(self):
        self.difficulty_level = 1
        self.used_words = set()
        self.word_generator = RandomWord()
        self.total_score = 0  # Initialize total score

    def update_score(self, score):
        self.total_score += score  # Add score from the round

    def increase_difficulty(self):
        if self.difficulty_level < 15:
            self.difficulty_level += 1  # Increment the difficulty level

    def get_word_length(self):
        # Set word length based on difficulty level
        if self.difficulty_level <= 5:
            return random.randint(3, 4)  # Short words for levels 1-5
        elif self.difficulty_level <= 10:
            return random.randint(5, 6)  # Medium words for levels 6-10
        else:
            return random.randint(7, 10)  # Longer words for levels 11-15

    def get_random_words(self):
        word_count = self.get_word_count()  # Determine how many words to generate
        word_length = self.get_word_length()  # Determine word length based on level
        available_words = set()

        while len(available_words) < word_count:
            word = self.word_generator.word()  # Generate a word without specifying length
            if len(word) == word_length and word not in self.used_words:
                available_words.add(word)

        self.used_words.update(available_words)
        return list(available_words)

    def get_word_count(self):
        # Adjust the number of words to memorize based on levels
        if self.difficulty_level <= 5:
            return random.randint(1, 2)  # 1-2 words for levels 1-5
        elif self.difficulty_level <= 10:
            return random.randint(3, 4)  # 3-4 words for levels 6-10
        else:
            return random.randint(5, 6)  # 5-6 words for levels 11-15

    def to_dict(self):
        return {
            'difficulty_level': self.difficulty_level,
            'used_words': list(self.used_words),
            'total_score': self.total_score
        }

@app.route('/')
def index():
    # Initialize game parameters in the session
    session['difficulty_level'] = 1
    session['used_words'] = []
    session['game'] = WordGame().to_dict()  # Initialize the game state in the session
    return render_template('index.html')

@app.route('/play')
def play():
    game_data = session.get('game')
    if game_data:
        game = WordGame()
        game.difficulty_level = game_data['difficulty_level']
        game.used_words = set(game_data['used_words'])
        game.total_score = game_data['total_score']
    else:
        game = WordGame()  # Create a new game if none exists

    words = game.get_random_words()
    session['words'] = words  # Store the words in the session

    # Determine timer duration based on difficulty level
    if game.difficulty_level <= 5:
        timer_duration = 3  # Beginning levels
    elif game.difficulty_level <= 10:
        timer_duration = 5  # Middle levels
    else:
        timer_duration = 10  # Higher levels

    session['game'] = game.to_dict()  # Store the updated game state in the session
    return render_template('play.html', words=words, timer_duration=timer_duration)

@app.route('/check_answers', methods=['POST'])
def check_answers():
    # Retrieve the expected words from the session
    words = session.get('words', [])
    expected_word_count = len(words)

    # Get recalled words using list comprehension
    recalled_words = [request.form.get(f'word{i}', '') for i in range(1, expected_word_count + 1)]

    # Calculate correct and missed words
    correct_words = set(words) & set(recalled_words)
    missed_words = set(words) - correct_words
    score = len(correct_words)

    # Recreate the game state from session data
    game_data = session.get('game')
    game = WordGame()
    if game_data:
        game.difficulty_level = game_data['difficulty_level']
        game.used_words = set(game_data['used_words'])
        game.total_score = game_data['total_score']
    else:
        game = WordGame()

    # Update the game score
    game.update_score(score)

    # Check if all words are recalled correctly
    if score == expected_word_count:
        # Progress to next level and redirect to /play
        game.increase_difficulty()
        session['game'] = game.to_dict()
        return redirect(url_for('play'))
    else:
        # If any word is missed, store game state and show results
        session['game'] = game.to_dict()
        message = "Some words were missed. Try Again!"
        return render_template('results.html', score=score, total_score=game.total_score,
                               correct_words=correct_words, missed_words=missed_words,
                               words=words, message=message)

if __name__ == "__main__":
    app.run(debug=True)
