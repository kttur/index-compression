import os
import csv
import operator

from collections import defaultdict

class IDService:
    def __init__(self, index):
        self.index = index

    def create_word_ids(self):        
        id = 1
        with open('word_ids.csv', 'w+', encoding='utf8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            for word in self.index:
                csv_writer.writerow([id, word])
                id += 1

    def create_postings_ids(self):
        # count df
        doc_freq = defaultdict(lambda: 0)        
        for word in self.index:
            for url in self.index[word]:
                doc_freq[url]+=1

        # sort by df
        sorted_docs = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
        print(f'Max df is: {sorted_docs[0][1]}')

        # write id based on df
        id = 1
        with open('document_ids.csv', 'w+', encoding='utf8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            for doc, _ in sorted_docs:
                csv_writer.writerow([id, doc])
                id += 1

    @staticmethod
    def get_document_ids():
        document_ids = dict()
        if not os.path.exists('./document_ids.csv'):
            raise Exception('run create_postings_ids() first')
        with open('document_ids.csv', encoding='utf8') as f:
            csv_file = csv.reader(f)
            for id, url in csv_file:
                document_ids[url] = id
        return document_ids

    @staticmethod
    def get_word_ids():
        word_ids = dict()
        if not os.path.exists('./word_ids.csv'):
            raise Exception('run create_word_ids() first')
        with open('word_ids.csv', encoding='utf8') as f:
            csv_file = csv.reader(f)
            for id, word in csv_file:
                word_ids[word] = id
        return word_ids