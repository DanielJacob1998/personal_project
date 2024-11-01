import random
from wonderwords import RandomWord

class WordGame:
    def __init__(self):
        self.difficulty_level = 1
        self.used_words = set()  # Track used words
        self.word_generator = RandomWord()

    def get_random_words(self):
        # Generate words based on the difficulty level
        available_words = set()
        
        while len(available_words) < 5:
            # Generate a word with varying lengths based on difficulty level
            word = self.word_generator.word(length=self.get_word_length())
            if word not in self.used_words:
                available_words.add(word)

            # If we've generated too many and still have fewer than 5, increase difficulty
            if len(available_words) >= 5:
                break
        else:
            # If we cannot get enough unique words, reset used words or increase difficulty
            self.used_words.clear()
            self.increase_difficulty()
            return self.get_random_words()  # Try again

        self.used_words.update(available_words)
        return list(available_words)

    def get_word_length(self):
        # Determine the length of words based on the difficulty level
        if self.difficulty_level == 1:
            return random.randint(3, 4)  # Short words
        elif self.difficulty_level == 2:
            return random.randint(5, 6)  # Medium words
        elif self.difficulty_level == 3:
            return random.randint(7, 10)  # Longer words
        return 3  # Default fallback

    def increase_difficulty(self):
        # Increase difficulty to the next level, reset if at max level
        if self.difficulty_level < 3:  # Assuming you want only 3 levels
            self.difficulty_level += 1
        else:
            self.difficulty_level = 1  # Optionally loop back to the start

    def play_round(self):
        words = self.get_random_words()
        print("Remember these words:", words)
        
        # Add player input and scoring logic here

# Example usage
game = WordGame()
game.play_round()
game.increase_difficulty()
game.play_round()
