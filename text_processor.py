import re

class TextProcessor:
    def __init__(self, pattern='[A-Za-zА-Яа-я0-9_]+'):
        self.pattern_re = re.compile(pattern)
    
    def is_word(self, word: str) -> bool:
        return bool(self.pattern_re.fullmatch(word))
