from inverted_index import InvertedIndex as II
from collections import defaultdict as dd
import pytest


class TestGetWordsFromText:

    getw = II().get_words_from_text

    def test_single_word(self):
        assert self.getw('Test') == ['test']

    def test_two_words(self):
        assert self.getw('Test phrase') == ['test', 'phrase']

    def test_sentence(self):
        assert self.getw('This is a complete sentence with a repeating word') ==  [
                'this',
                'is',
                'a',
                'complete',
                'sentence',
                'with',
                'a',
                'repeating',
                'word'
        ]

    def test_empty_string(self):
        assert self.getw('') == []

    def test_empty_string_with_spaces(self):
        assert self.getw('    ') == []

    def test_empty_string_with_tabs(self):
        assert self.getw('      ') == []

    def test_word_with_symbols(self):
        assert self.getw('Test phr@se') == ['test']

    def test_word_with_number(self):
        assert self.getw('Test one1') == ['test', 'one1']

    def test_cyr_word(self):
        assert self.getw('Тест') == ['тест']

    def test_word_with_underscore(self):
        assert self.getw('Test_words') == ['test_words']


class TestCreateIndex:

    def test_empty_collection(self):
        with pytest.raises(Exception) as e:
            II().create_index()
        assert 'add collection first' in str(e.value)

    def test_single_element(self):
        c = [('http://test.net', 'Simple text')]
        ii = II(c)
        ii.create_index()
        d = dd(list)
        d['simple'] = ['http://test.net']
        d['text'] = ['http://test.net']
        assert d == ii.index

    def test_multiple_elements(self):
        c = [
                ('One', 'one Two three'),
                ('two', 'three'),
                ('three', 'two Three')
            ]
        d = dd(list)
        d['one'] = ['One']
        d['two'] = ['One', 'three']
        d['three'] = ['One', 'two', 'three']
        ii = II(c)
        ii.create_index()
        assert d == ii.index

