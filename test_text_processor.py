from text_processor import TextProcessor

class TestIsWord:

    tp = TextProcessor()

    def test_one_word_latin(self):
        assert self.tp.is_word('Test')

    def test_one_word_cyr(self):
        assert self.tp.is_word('Тест')

    def test_two_words(self):
        assert not self.tp.is_word('Test test')

    def test_word_with_num(self):
        assert self.tp.is_word('Test1')

    def test_word_with_underscore(self):
        assert self.tp.is_word('Test_test')

    def test_words_devided_by_symbol(self):
        assert not self.tp.is_word('Test*test')
