import os
import mmap
import contextlib

from id_service import IDService

class IndexToByteConverter:
    '''
    Index:

    | postings_link |
    -----------------
    |    4 bytes    |
    -----------------

    Postings:

    | count_postings |    postings    |
    -----------------------------------
    |    2 bytes     |    (2 bytes)   |
    |                |        x       |
    |                | count_postings |
    -----------------------------------
    '''
    def __init__(self, index=None):
        self.index = index
        self.postings_ids = IDService.get_document_ids()
        self.word_ids = IDService.get_word_ids()

    def build(self):
        if not self.index:
            raise Exception('no index found to build')

        if not os.path.isdir('./uncompressed_index'):
            os.mkdir('./uncompressed_index')

        # word_bytes_count = 0
        # posting_bytes_count = 0
        postings_reference = 0
        with open('./uncompressed_index/index.bin', mode='wb') as index_f, \
             open('./uncompressed_index/postings.bin', mode='wb+') as postings_f:
            for word in self.index:
                index_f.write(postings_reference.to_bytes(4, byteorder='big'))
                word_freq = len(self.index[word])
                word_freq_as_bytes = word_freq.to_bytes(2, byteorder='big')
                postings_f.write(word_freq_as_bytes)
                for url in self.index[word]:
                    postings_f.write(int(self.postings_ids[url]).to_bytes(2, byteorder='big'))
                postings_reference += word_freq*2 + 2

    def get_word_postings(self, word):
        if word not in self.word_ids:
            raise Exception('there is no such word in the dictionary')
        word_id = int(self.word_ids[word])
        with open('uncompressed_index/index.bin', mode='r+b') as index_f, \
             open('uncompressed_index/postings.bin', mode='r+b') as postings_f:
            index_mm = mmap.mmap(index_f.fileno(), 0)
            postings_mm = mmap.mmap(postings_f.fileno(), 0)

            postings_file_byte_offset = int.from_bytes(index_mm[(word_id-1)*4:word_id*4], byteorder='big')

            # print(postings_file_byte_offset)

            count_bytes_for_postings = int.from_bytes(postings_mm[postings_file_byte_offset:postings_file_byte_offset + 2], byteorder='big')

            # print(count_bytes_for_postings)

            postings_ids = []
            for byte_number in range(count_bytes_for_postings):
                postings_id = int.from_bytes(postings_mm[postings_file_byte_offset + 2 + 2*byte_number: postings_file_byte_offset + 2 + 2*byte_number + 2], byteorder='big')
                postings_ids.append(postings_id)
            return postings_ids
            # print(self.postings_ids[postings_id])
            # print(count_bytes_for_postings)
   