import pynput, random, nltk, keyboard
from nltk.corpus import wordnet as wn
from pynput import keyboard as kb


rl = 0  
current_word = [] 

import time

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
                return lemma.antonyms()[0].name()
    return word 
def change_word():
    global current_word, rl
    if not current_word:
        return
    keyboard.hook(lambda e: None)
    new_word = get_antonym("".join(current_word))
    if new_word != "".join(current_word):

        for _ in range(rl + 2):
            keyboard.press_and_release('backspace')

        keyboard.press_and_release('space')
        keyboard.write(new_word)
        keyboard.press_and_release('space')
        print (f"{current_word} -> {new_word}")

        rl = len(new_word)
    
    keyboard.unhook_all()
    current_word.clear()
    time.sleep(0.1)


def on_release(key):
    if key == kb.KeyCode.from_char('0') and keyboard.is_pressed('alt'):
        return False

def on_press(key):

    global current_word, rl
    try:
        if hasattr(key, 'char') and key.char is not None:
            current_word.append(key.char)
            rl += 1  

            if random.random() < 0.02:
                keyboard.press_and_release('backspace')
                wrong_char = generate_badchar(key.char)
                keyboard.write(wrong_char)
                rl += 1  


            if random.random() < 0.4:
                keyboard.press_and_release('capslock')

    except AttributeError:
        pass  
   
    if key in {kb.Key.space, kb.Key.tab, kb.Key.enter}:
        if current_word:

            if random.random() < 1: 
                change_word()
            else:
                keyboard.write("um.. ")
                rl += 4  
        rl = 0
        current_word.clear()

    elif key == kb.Key.backspace:
        if current_word:
            current_word.pop() 
            rl = max(0, rl - 1)  

with kb.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()