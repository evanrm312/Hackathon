import pynput, random, nltk, keyboard
from nltk.corpus import wordnet as wn
from pynput import keyboard as kb
import time

# Initialize variables
rl = 0  # current word length
current_word = []
typing = True  # Typing flag set to True at the start

# Generate a random "bad" character for the word
def generate_badchar(char):
    i = ord(char)
    j = -1
    while j == i or j < 97 or j > 122:
        j = random.randint(97, 122)
    return chr(j)

# Get antonyms from WordNet
def get_antonym(word):
    synsets = wn.synsets(word)
    for syn in synsets:
        for lemma in syn.lemmas():
            if lemma.antonyms():
                return random.choice(lemma.antonyms()).name()
    return word  # Return original if no antonym found

# Replace the current word with an antonym
def change_word(word):
    global typing, current_word
    new_word = get_antonym("".join(word))
    if new_word != "":
        # Clear the current word by backspacing
        for _ in range(len(word) + 1):
            keyboard.press_and_release('backspace')
            time.sleep(0.05)  # Slight delay to simulate human-like backspacing

        # Write the new word (antonym)
        keyboard.write(new_word)
        # Clear current_word list and reset typing flag
        current_word.clear()
        typing = True  # Set typing flag to True to continue typing the next word

# Listener for keyboard events
def on_release(key):
    if key == kb.KeyCode.from_char('0') and keyboard.is_pressed('alt'):
        return False  # Stop the listener when Alt + 0 is pressed

def on_press(key):
    global current_word, typing
    try:
        if typing and hasattr(key, 'char') and key.char is not None:
            # If it's a valid character, append to current_word
            current_word.append(key.char)

            # Introduce a small error randomly
            if random.random() < 0.19:  # Random chance to simulate a wrong character
                keyboard.press_and_release('backspace')
                wrong_char = generate_badchar(key.char)
                keyboard.write(wrong_char)
                
    except AttributeError:
        pass

    # If space, tab, or enter is pressed, process the word and replace it with an antonym
    if typing and key in {kb.Key.space, kb.Key.tab, kb.Key.enter}:
        # Only change word if current_word is not empty
        if current_word:
            change_word(current_word)
        typing = True  # Ensure typing flag is reset after processing a word

# Start the listener
with kb.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
