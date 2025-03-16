import pynput, random, nltk, keyboard
from nltk.corpus import wordnet as wn
from pynput import keyboard as kb
import time
import threading

# Initialize variables
current_word = []
typing_lock = threading.Lock()  # Thread lock for synchronization
is_computer_typing = False  # Flag to track when computer is typing
word_length = 0  # Track word length

# Create keyboard controller for programmatic typing
keyboard_controller = kb.Controller()

def block_input(block):
    """Block or unblock keyboard input using pynput"""
    global is_computer_typing
    is_computer_typing = block
    # We'll use this flag in the on_press handler

def generate_badchar(char):
    """Generate a random incorrect character"""
    i = ord(char)
    j = -1
    while j == i or j < 97 or j > 122:
        j = random.randint(97, 122)
    print(f"Generated bad character: {chr(j)}")
    return chr(j)

def get_antonym(word):
    """Find antonym for a word if available"""
    print(f"Searching antonyms for '{word}'")
    try:
        synsets = wn.synsets(word)
        for syn in synsets:
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    return random.choice(lemma.antonyms()).name()
    except Exception as e:
        print(f"Error finding antonym: {e}")
    return word

def change_word(word):
    """Replace current word with its antonym or a modified version"""
    global current_word, word_length
    
    # Block keyboard input while we're typing
    block_input(True)
    
    try:
        # Convert word list to string
        original_word = "".join(word)
        print(f"Changing word: '{original_word}'")
        
        # Get antonym
        new_word = get_antonym(original_word)
        print(f"Result: '{new_word}'")
        
        if len(new_word) > 1 and new_word != original_word:
            # Delete the current word
            for _ in range(word_length):
                keyboard.press_and_release('backspace')
                time.sleep(0.01)  # Small delay to prevent issues
            
            # Type the new word
            keyboard.write(new_word)
            keyboard.press_and_release('space')
            print(f"Changed: '{original_word}' -> '{new_word}'")
        
        # Reset word tracking
        current_word.clear()
        word_length = 0
    
    except Exception as e:
        print(f"Error in change_word: {e}")
    
    finally:
        # Always unblock input when done
        block_input(False)

def on_release(key):
    """Handle key release events"""
    if key == kb.KeyCode.from_char('0') and keyboard.is_pressed('alt'):
        print("Exiting program")
        return False

def on_press(key):
    """Handle key press events"""
    global current_word, word_length
    
    # Skip processing if computer is typing
    if is_computer_typing:
        return False  # Block the key press
    
    try:
        # Handle regular character keys
        if hasattr(key, 'char') and key.char is not None:
            # Add to current word tracking
            current_word.append(key.char)
            word_length += 1
            
            # Random chance to make a typo (19%)
            if random.random() < 0.19:
                # Block input while making the typo
                block_input(True)
                try:
                    keyboard.press_and_release('backspace')
                    time.sleep(0.01)  # Small delay
                    wrong_char = generate_badchar(key.char)
                    keyboard.write(wrong_char)
                    # Update our tracking
                    if current_word:
                        current_word[-1] = wrong_char
                finally:
                    block_input(False)
            
            # Lower chance to toggle caps lock (5% instead of 30%)
            if random.random() < 0.05:
                keyboard.press_and_release("caps_lock")
                print("Toggled caps lock")
    
    except AttributeError:
        pass
    
    # Handle special keys
    if key in {kb.Key.space, kb.Key.tab, kb.Key.enter}:
        # End of word
        if current_word and random.random() < 0.50:
            change_word(current_word)
        else:
            current_word.clear()
            word_length = 0
    
    elif key == kb.Key.backspace and current_word:
        # Handle backspace
        current_word.pop() if current_word else None
        word_length = max(0, word_length - 1)  # Prevent negative count

print("Bad Grammar Helper started! Press Alt+0 to exit.")
print("Keyboard input will be blocked while the computer is typing.")

# Set up the listener with a non-blocking approach
listener = kb.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Keep the main thread alive
try:
    while listener.is_alive():
        time.sleep(0.1)
except KeyboardInterrupt:
    listener.stop()
    print("Program stopped by user")