import itertools as it


def split_records(records, n_max=20_000):
    """
    Split fasta records into equal number of n_max seqs.
    Returns an iterator.
    **Max numbers of seq in GISAID dataset ~107.000
    """
    max_n_mafft = 20_000
    n_start = 0
    for i, l in enumerate(it.tee(records, 6)):
        l_slice = it.islice(l, n_start, max_n_mafft)
        n_start += n_max
        max_n_mafft += n_max

        yield l_slice


def batch_iterator(iterator, batch_size):
    """Returns lists of length batch_size.

    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.

    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.next()
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch