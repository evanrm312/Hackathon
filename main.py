import pynput, random, nltk, keyboard
from nltk.corpus import wordnet as wn
from pynput import keyboard as kb
import time


rl = 0  
current_word = []
typing = True  

def generate_badchar(char):
    i = ord(char)
    j = -1
    while j == i or j < 97 or j > 122:
        j = random.randint(97, 122)
    return chr(j)


def get_antonym(word):
    synsets = wn.synsets(word)
    for syn in synsets:
        for lemma in syn.lemmas():
            if lemma.antonyms():
                return random.choice(lemma.antonyms()).name()
    return word


def change_word(word):
    global typing, current_word, rl
    new_word = get_antonym("".join(word))
    print(new_word)
    if len(new_word) > 1:
        typing = False
        for _ in range(rl):
            keyboard.press_and_release('backspace') 
        keyboard.write(new_word)
        current_word.clear()
    new_word.clear()

def on_release(key):
    if key == kb.KeyCode.from_char('0') and keyboard.is_pressed('alt'):
        return False

def on_press(key):
    global current_word, typing, rl
    try:
        if typing and hasattr(key, 'char') and key.char is not None:
            
            current_word.append(key.char)
            rl += 1 
            if random.random() < 0.19:  
                keyboard.press_and_release('backspace')
                wrong_char = generate_badchar(key.char)
                keyboard.write(wrong_char)
            if random.random() < 0.3:
                keyboard.press("caps_lock")
                
    except AttributeError:
        pass

    if typing and key in {kb.Key.space, kb.Key.tab, kb.Key.enter}:
        
        if current_word:
            change_word(current_word)
        typing = True  
    elif key == kb.Key.backspace and len(current_word) > 0:
        del(current_word[-1])
        rl -= 1 

with kb.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
