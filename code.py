import pygame
import random
import string

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Define red color
FONT_SIZE = 50
FPS = 60

# Load word list from a file or define your own list of words here
WORD_LIST = {
    "vegatables": ["carrot", "tomato", "broccoli", "potato","onion","asparagus","cabage"],
    "fruits": ["apple", "banana", "orange", "grape","plum","date","banana","pear"],
    "food": ["pasta", "bread", "sushi", "burger","meat","noodles","pizza"],
    "animals": ["armadillo", "camel", "owl", "lion","cow","pigeon","fox"],
    "nature": ["sun", "moon", "star", "rain","cloud","snow","river"],
    "furniture": ["sofa", "desk", "shelf", "chair","oven","armchair"],
    "school_equipment": ["folder", "pencil", "scissors", "book","ruler","eraser","marker"],
    "school_subjects": ["math", "science", "english", "history","Literature","art","sport"],
    "instruments": ["violin", "guitar", "piano", "clarinet","flute","trumpet","drum","cello"],
    "clothes": ["shirt", "jeans", "coat", "scarf","dress","hat","shoes"],
    "countries": ["argentina", "russia", "italy", "egypt","japan","canada","israel"],
    "transport": ["funicular", "airplane", "truck", "motorcycle","bus","cab","train"],
    "computer": ["monitor", "games", "keyboard", "mouse","headphones","cable","processor"],
    "jobs": ["doctor", "farmer", "principal", "guard","singer","cashier","coach"],
    "colors": ["green", "blue", "yellow", "orange","black","white","red"],
    "body": ["liver", "hand", "intestines", "tongue","heart","knee","lap"],
    # Add more topics with their respective word lists here
    # ...
}

# Function to choose a random word from the selected topic
def get_random_word(topic):
    if topic in WORD_LIST:
        return random.choice(WORD_LIST[topic])
    else:
        return None  # Handle the case when the topic is not found

# Function to display the guessed word with underscores for unknown letters
def display_word(word, guessed_letters):
    displayed = []
    for letter in word:
        if letter in guessed_letters:
            displayed.append(letter.upper())
        else:
            displayed.append("_")
    return " ".join(displayed)

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")
clock = pygame.time.Clock()

# Load font
font = pygame.font.SysFont(None, FONT_SIZE)

# Create a simple Button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, callback=None, data=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.callback = callback
        self.data = data
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.image.fill(WHITE)
        self.render_text()

    def render_text(self):
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if self.is_clicked(pos):
                        if self.callback is not None:
                            self.callback(self.data)

# Function to display the "HOW TO PLAY" guide image
def show_guide(data):
    screen.blit(guide_bg, (0, 0))
    guide_image = pygame.image.load("guide.png")
    guide_rect = guide_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(guide_image, guide_rect)
    pygame.display.flip()
    pygame.time.delay(10000)  # Display the guide for 10 seconds (adjust as needed)

# Function to start the game with a random topic
def start_game(data=None):
    all_topics = list(WORD_LIST.keys())
    topic = random.choice(all_topics)
    word_to_guess = get_random_word(topic)
    guessed_letters = set()
    max_tries = 6
    game_screen(word_to_guess, topic, guessed_letters, max_tries)

# Load the hangman images into a list
hangman_images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

# Load the fireworks image
fireworks_image = pygame.image.load("fireworks.png")  # Replace "fireworks.png" with your image file name
fireworks_image = pygame.transform.scale(fireworks_image, (330, 330))  # Resize the image to 330x330 pixels

# Define a variable to keep track of previously guessed wrong letters
previously_guessed_wrong_letters = set()

# Add a variable for the delay timer
delay_timer = 0

def game_screen(word_to_guess, topic, guessed_letters, max_tries):
    global delay_timer  # Use the global delay_timer variable

    revealed = set()  # Store the indices of revealed letters
    wrong_letters = set()  # Store wrong letters
    correct_guesses = set()  # Store correct guesses
    running = True
    won = False  # Add a variable to track if the user has won
    hangman_stage = 0  # Initialize the hangman stage

    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in range(97, 123):  # Check if the key pressed is a lowercase letter
                    letter = chr(event.key)
                    if letter in word_to_guess:
                        # Replace all occurrences of the guessed letter in lines
                        for i, char in enumerate(word_to_guess):
                            if char == letter:
                                revealed.add(i)
                                correct_guesses.add(letter)  # Add correct guesses here
                    else:
                        if letter not in previously_guessed_wrong_letters:
                            previously_guessed_wrong_letters.add(letter)  # Add the letter to the set
                            wrong_letters.add(letter)
                            hangman_stage += 1  # Increase hangman stage for wrong guess

        # Calculate the remaining max tries based on the incorrect guesses
        tries = len(wrong_letters)

        # Clear the screen
        screen.fill(WHITE)

        # Display the hangman image only if a new wrong letter is guessed
        if hangman_stage >= 0:
            hangman_rect = hangman_images[hangman_stage].get_rect(bottomright=(WIDTH - 20, HEIGHT - FONT_SIZE * 1))
            screen.blit(hangman_images[hangman_stage], hangman_rect)

        # Display the topic as the title
        title_text = font.render(topic.upper(), True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, FONT_SIZE // 2))
        screen.blit(title_text, title_rect)

        # Create lines for each letter in the chosen word
        word = word_to_guess.upper()
        line_height = FONT_SIZE
        line_spacing = 10

        total_width = len(word) * (line_height + line_spacing)
        start_x = (WIDTH - total_width) // 7
        start_y = HEIGHT // 2

        for i, letter in enumerate(word):
            line_text = font.render("_", True, BLACK)
            if i in revealed:
                line_text = font.render(letter, True, BLACK)  # Display revealed letters
            line_rect = line_text.get_rect(midleft=(start_x, start_y))
            screen.blit(line_text, line_rect)
            start_x += line_height + line_spacing

        if all(letter in correct_guesses for letter in word_to_guess) and tries < max_tries:
            # Display the "YOU WON!" screen
            screen.fill(WHITE)
            won_text = font.render("YOU WON!", True, BLACK)
            won_rect = won_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            screen.blit(won_text, won_rect)

            word_text = font.render("the word was: " + word_to_guess, True, BLACK)
            word_rect = word_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(word_text, word_rect)

            # Display the fireworks image in the bottom left
            fireworks_rect = fireworks_image.get_rect(topleft=(10, HEIGHT - 300))
            screen.blit(fireworks_image, fireworks_rect)

            # Add code to display the "GOOD JOB" image in the bottom right
            goodjob_image = pygame.image.load("goodjob.png")  # Replace with your image file name
            goodjob_image = pygame.transform.scale(goodjob_image, (400, 200))  # Resize the image
            goodjob_rect = goodjob_image.get_rect(bottomright=(WIDTH - 20, HEIGHT - FONT_SIZE * 1))
            screen.blit(goodjob_image, goodjob_rect)

            pygame.display.flip()
            pygame.time.delay(5000)  # Display the "YOU WON!" screen for 5 seconds
            running = False
            won = True

        if tries >= max_tries:
            # Check if the delay timer has not reached 1.5 seconds yet
            if delay_timer < FPS * 1.5:
                delay_timer += 1
            else:
                # Display the "YOU LOST!" screen
                screen.fill(WHITE)
                lost_text = font.render("YOU LOST!", True, BLACK)
                lost_rect = lost_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
                screen.blit(lost_text, lost_rect)

                word_text = font.render("the word was: " + word_to_guess, True, BLACK)
                word_rect = word_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(word_text, word_rect)

                pygame.display.flip()
                pygame.time.delay(5000)  # Display the "YOU LOST!" screen for 5 seconds
                running = False

        # Display the "WRONG LETTERS" title above the wrong letters
        wrong_title_text = font.render("WRONG LETTERS", True, BLACK)
        wrong_title_rect = wrong_title_text.get_rect(topleft=(20, HEIGHT - FONT_SIZE * 2))
        screen.blit(wrong_title_text, wrong_title_rect)

        # Display the wrong letters at the bottom left in red
        wrong_text = font.render(" ".join(wrong_letters), True, RED)  # Use RED color
        wrong_rect = wrong_text.get_rect(topleft=(20, HEIGHT - FONT_SIZE * 1))
        screen.blit(wrong_text, wrong_rect)

        pygame.display.flip()
        clock.tick(FPS)

    if won:
        # Add code here for what to do after winning
        pass

# Load "HOW TO PLAY" guide background image
guide_bg = pygame.image.load("guide_bg.jpg")
guide_bg = pygame.transform.scale(guide_bg, (WIDTH, HEIGHT))

# Create buttons
how_to_play_button = Button(WIDTH // 2 - WIDTH // 5, HEIGHT // 2, WIDTH // 5 * 2, FONT_SIZE * 2, "HOW TO PLAY", show_guide)
play_button = Button(WIDTH // 2 - WIDTH // 8, HEIGHT // 2 - FONT_SIZE - 10, WIDTH // 4, FONT_SIZE, "PLAY", start_game)

buttons_group = pygame.sprite.Group(how_to_play_button, play_button)

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    buttons_group.update(event_list)
    buttons_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
