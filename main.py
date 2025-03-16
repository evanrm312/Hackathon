import pynput, random, nltk , keyboard, antonym
from nltk.corpus import wordnet
from pynput import keyboard as kb

rl = 0 # current word length
current_word = []
typing = False

def generate_badchar(char):
    i = ord(char)
    j = -1
    while j == i or j < 97 or j > 122:
        j = random.randint(97, 122)
    return chr(j)

def generate_antonym(word):
    if word in antonym.most_common_words:
        index = antonym.most_common_words.index(word)
        if (antonym.antonyms[index] != "--"):
            return antonym.antonyms[index]

def change_word(word):
    new_word = ""
    new_word = generate_antonym("".join(word))
    if (new_word != ""):
        for _ in range(len(word)):
            keyboard.press_and_release('backspace')
        keyboard.write(new_word)
        current_word.clear()

def on_release(key):
    if key == kb.KeyCode.from_char('0') and keyboard.is_pressed('alt'):
        return False  # Stops the listener
    
def on_press(key):
    global current_word, typing
    try:
        if hasattr(key, 'char') and key.char is not None:
            current_word.append(key.char)
            typing = True
            if random.random() < 0.1:
                keyboard.press_and_release('backspace')
                wrong_char = generate_badchar(key.char)
                keyboard.write(wrong_char)
    except AttributeError:
        pass
    if typing and key in {kb.Key.space, kb.Key.tab, kb.Key.enter}:
            change_word(current_word)
        
with kb.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()