import pynput, random, nltk , keyboard
from nltk.corpus import wordnet
from pynput import keyboard as kb

rl = 0 # current word length
current_word = []
typing = False

def generate_badchar(char):
    i = ord(char)
    j = -1
    while j == i or j < 97 or j > 123:
        j = random.randint(97, 123)
    return chr(j)

def generate_antonym(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    if antonyms:
        return antonyms[0]
    else:
        return word 

def change_word():
    generate_antonym()

def on_release(key):
    return not keyboard.is_pressed('alt+0')
    
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
        if typing and (kb.Key.space == key or kb.Key.tab == key or kb.Key.enter == key):
            change_word()
        
with kb.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()