from collections import defaultdict
import text_processor

class InvertedIndex:
    def __init__(self, collection=None):
        # [(url, text)]
        self.collection = collection
        self.index = defaultdict(list)
        self.text_processor = text_processor.TextProcessor()

    def create_index(self):
        if not self.collection:
            raise Exception('add collection first')
        for url, text in self.collection:
            words = set(self.get_words_from_text(text))
            for word in words:
                self.index[word].append(url)
        
    def get_words_from_text(self, text):
        words_unprocessed = text.split(' ')
        words = []
        for w in words_unprocessed:
            if self.text_processor.is_word(w):
                words.append(w.lower())
        return words