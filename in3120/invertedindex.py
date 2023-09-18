#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
from abc import ABC, abstractmethod
from collections import Counter
from typing import Iterable, Iterator, List
from .dictionary import InMemoryDictionary
from .normalizer import Normalizer
from .tokenizer import Tokenizer
from .corpus import Corpus
from .posting import Posting
from .postinglist import CompressedInMemoryPostingList, InMemoryPostingList, PostingList
#extra import?
import document


class InvertedIndex(ABC):
    """
    Abstract base class for a simple inverted index.
    """

    def __getitem__(self, term: str) -> Iterator[Posting]:
        return self.get_postings_iterator(term)

    def __contains__(self, term: str) -> bool:
        return self.get_document_frequency(term) > 0

    @abstractmethod
    def get_terms(self, buffer: str) -> Iterator[str]:
        """
        Processes the given text buffer and returns an iterator that yields normalized
        terms as they are indexed. Both query strings and documents need to be
        identically processed.
        """
        pass

    @abstractmethod
    def get_postings_iterator(self, term: str) -> Iterator[Posting]:
        """
        Returns an iterator that can be used to iterate over the term's associated
        posting list. For out-of-vocabulary terms we associate empty posting lists.
        """
        pass

    @abstractmethod
    def get_document_frequency(self, term: str) -> int:
        """
        Returns the number of documents in the indexed corpus that contains the given term.
        """
        pass


class InMemoryInvertedIndex(InvertedIndex):
    """
    A simple in-memory implementation of an inverted index, suitable for small corpora.

    In a serious application we'd have configuration to allow for field-specific NLP,
    scale beyond current memory constraints, have a positional index, and so on.

    If index compression is enabled, only the posting lists are compressed. Dictionary
    compression is currently not supported.
    """

    def __init__(
        self,
        corpus: Corpus,
        fields: Iterable[str],
        normalizer: Normalizer,
        tokenizer: Tokenizer,
        compressed: bool = False,
    ):
        self.__corpus = corpus
        self.__normalizer = normalizer
        self.__tokenizer = tokenizer
        self.__posting_lists: List[PostingList] = []
        self.__dictionary = InMemoryDictionary()
        self.__build_index(fields, compressed)

    def __repr__(self):
        return str({term: self.__posting_lists[term_id] for (term, term_id) in self.__dictionary})

    def __build_index(self, fields: Iterable[str], compressed: bool) -> None:
        # raise NotImplementedError("You need to implement this as part of the assignment.")
        docs = [document]
        for id in range(self.__corpus.size):
            docs.append(self.__corpus.get_document[id])
        
        for field in fields:
            freq = 0
            for doc in docs:
                while doc.get_field(field) is not None:
                    self.__dictionary.add_if_absent(field)
                    freq = freq + 1

            PostingList.append_posting(Posting(doc.get_document_id, freq))


    def get_terms(self, buffer: str) -> Iterator[str]:
        #raise NotImplementedError("You need to implement this as part of the assignment.")
        # res = Iterator()
        result_list = []
        tokens = self.__tokenizer.tokens(buffer)
        buffer = self.__tokenizer.join(tokens)
        for s in buffer:
            result_list.append(self.__normalizer.normalize(s))

        return result_list
    
    def get_postings_iterator(self, term: str) -> Iterator[Posting]:
        #raise NotImplementedError("You need to implement this as part of the assignment.")
        res = Iterator()[Posting]
        if self.__dictionary.__contains__(term):
            postings_list = self.__posting_lists[self.__dictionary.get_term_id(term)]
            res = Iterator[Posting](postings_list)
        
        return res


    def get_document_frequency(self, term: str) -> int:
        # raise NotImplementedError("You need to implement this as part of the assignment.")
        if self.__dictionary.__contains__(term):
            return len(self.__posting_lists[self.__dictionary.get_term_id(term)])
        else:
            return 0
        