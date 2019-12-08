import os
import pickle

from inverted_index import InvertedIndex
from id_service import IDService
from db_service import DBService
from index_to_bytes import IndexToByteConverter
from compress_index import IndexCompressor

def main():
    # if uncompressed index not exists
    if not os.path.exists('./uncompressed_index'):
        db_service = DBService("msuspider.db")

        inverted_index = InvertedIndex(db_service.get_texts())
        inverted_index.create_index()

        with open('index.pickle', 'wb') as f:
            pickle.dump(inverted_index.index, f)

        id_service = IDService(inverted_index.index)
        id_service.create_postings_ids()
        id_service.create_word_ids()

        converter = IndexToByteConverter(inverted_index.index)
        converter.build()

    # if in-memory index doesnt exist
    if not os.path.exists('./index.pickle'):
        db_service = DBService("msuspider.db")
        inverted_index = InvertedIndex(db_service.get_texts())
        inverted_index.create_index()
        with open('index.pickle', 'wb') as f:
            pickle.dump(inverted_index.index, f)
        inv_index = inverted_index.index
    else:
        with open('index.pickle', 'rb') as f:
            inv_index = pickle.load(f)

    # if compressed index deosnt exist
    if not os.path.exists('./compressed_index'):
        index_compressor = IndexCompressor(inv_index)
        index_compressor.build_delta()        

    converter = IndexToByteConverter()
    print(converter.get_word_postings('ректор')[1])
    print(inv_index['ректор'][1])

    



if __name__ == "__main__":
    main()