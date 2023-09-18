#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Iterator
from .posting import Posting


class PostingsMerger:
    """
    Utility class for merging posting lists.

    It is currently left unspecified what to do with the term frequency field
    in the returned postings when document identifiers overlap. Different
    approaches are possible, e.g., an arbitrary one of the two postings could
    be returned, or the posting having the smallest/largest term frequency, or
    a new one that produces an averaged value, or something else.
    """

    @staticmethod
    def intersection(p1: Iterator[Posting], p2: Iterator[Posting]) -> Iterator[Posting]:
        """
        A generator that yields a simple AND of two posting lists, given
        iterators over these.

        The posting lists are assumed sorted in increasing order according
        to the document identifiers.
        """
        #raise NotImplementedError("You need to implement this as part of the assignment.")
        
        res = Iterator()
        
        # while p1 is not None and p2 is not None:
        while not current_p1 == None and not current_p2 == None:
            if current_p1.document_id() == current_p2.document_id():
                yield current_p1.document_id
                current_p1 = next(p1, None)
                current_p2 = next(p2, None)
            elif p1() < p2():
                current_p1 = next(p1, None)
            else:
                current_p2 = next(p2, None)

        return res


    @staticmethod
    def union(p1: Iterator[Posting], p2: Iterator[Posting]) -> Iterator[Posting]:
        """
        A generator that yields a simple OR of two posting lists, given
        iterators over these.

        The posting lists are assumed sorted in increasing order according
        to the document identifiers.
        """
        #raise NotImplementedError("You need to implement this as part of the assignment.")

        res = Iterator()
        current_p1 = next(p1, None)
        current_p2 = next(p2, None)
        
        while current_p1 is not None and current_p2 is not None:
            if current_p1.document_id() == current_p2.document_id():
                yield current_p1.document_id
                current_p1 = next(p1, None)
                current_p2 = next(p2, None)
            elif current_p1.document_id() < current_p2.document_id():
                yield current_p1.document_id
                current_p1 = next(p1, None)
            else:
                yield current_p2.document_id
                current_p2 = next(p2, None)

        return res
