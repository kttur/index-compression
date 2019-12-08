import encoding
import os

from id_service import IDService

class IndexCompressor:
    def __init__(self, index):
        self.index = index
        self.postings_ids = IDService.get_document_ids()
        self.word_ids = IDService.get_word_ids()

    def build(self, compression_algorithm):
        if not self.index:
            raise Exception('add index to this object first')        
        if not os.path.isdir('./compressed_index'):
            os.mkdir('./compressed_index')

        postings_reference = 0
        with open('./compressed_index/index.bin', mode='wb') as index_f, \
             open('./compressed_index/postings.bin', mode='wb+') as postings_f:
            for word in self.index:
                postings_gamma_codes_chain = ''
                for posting_url in self.index[word]:
                    posting_id = int(self.postings_ids[posting_url])
                    postings_gamma_codes_chain = postings_gamma_codes_chain + compression_algorithm(posting_id)
                chain_with_leading_zeros = encoding.add_leading_zeros(postings_gamma_codes_chain)
                bytes_to_write = bytes([int(x, 2) for x in encoding.split_code_to_8_bits(chain_with_leading_zeros)])
                postings_f.write(bytes_to_write)
                index_f.write(bytes(postings_reference.to_bytes(4, byteorder='big')))
                postings_reference += len(bytes_to_write)

    def build_gamma(self):
        self.build(encoding.elias_gamma)
    
    def build_delta(self):
        self.build(encoding.elias_delta)

    
            