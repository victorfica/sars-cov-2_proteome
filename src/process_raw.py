import pandas as pd
import fire
from Bio import SeqIO
from concurrent.futures import ThreadPoolExecutor

from .conf import DATA_INTERIM, DATA_PROCESSED
from .conf import protein_names, reference_seq


def parse_raw(rawfile):
    # Parse rawfasta and separate proteins as reference vs others. This take aprox 1-2 minutes
    records = SeqIO.parse(rawfile, "fasta")

    ref_seqs = dict()
    other_seqs = dict()
    for i, r in enumerate(records, 1):
        head = r.description
        head_sections = head.split("|")
        # relevant header sections
        prot_name = head_sections[0]
        sample_id = head_sections[3]

        if reference_seq == sample_id:
            ref_seqs[prot_name + "|" + head_sections[1]] = str(r.seq)
        else:
            other_seqs[prot_name + "|" + head_sections[1]] = str(r.seq)

    return ref_seqs, other_seqs



class ProcessRaw:

    def __init__(self, rawfile, reference=True, others=True, outdir='sars2_proteins'):
        """

        Parameters
        ----------
        rawfile
        reference
        others
        outdir
        """

        self.rawfile = rawfile
        self.outdir = outdir
        self.reference = reference
        self.others = others
        self.ref_outfile = 'sars2_refWuhan_{}.fasta'
        self.other_outfile = 'sars2_others_{}.fasta'

        print('Setting up SARS-CoV-2 proteome folder')
        self.sars2protein_folder = DATA_INTERIM/'sars2_proteins'
        if not self.sars2protein_folder.is_dir():
            self.sars2protein_folder.mkdir()
        print('sars2_proteins folder made')
        # get dict of parsed records
        print('Parsing rawfile Fasta...')
        self.ref_seqs, self.others_seqs = parse_raw(self.rawfile)

    def ref_tofasta(self):
        """
        Write SARS-CoV-2 Reference Sample proteins to Fasta Files.

        """

        print('Writing SARS-CoV-2 Reference Sample proteins...')
        # write reference fastas
        for k, v in self.ref_seqs.items():
            name = k.split("|")[0]
            with open(self.sars2protein_folder / self.ref_outfile.format(name), 'w') as f:
                f.write('>{}\n'.format(k))
                f.write('{}\n'.format(v))


    def others_tofasta(self):
        """
        Write SARS-CoV-2 Non-Reference Sample proteins to Fasta Files.
        """
        print('Writing SARS-CoV-2 Non-Reference Sample proteins...')

        def write_proteins(d, protein):

            """
            Select specific protein from seqs dictionary
            and write to respective fasta.

            """

            selected = filter(lambda items: items[0].split('|')[0] == protein, d.items())
            with open(self.sars2protein_folder / 'sars2_others_{}.fasta'.format(protein), 'w') as f:
                for h, seq in selected:
                    f.write('>{}\n'.format(h))
                    f.write('{}\n'.format(seq))

        def _helper(protein):
            return write_proteins(self.others_seqs, protein)

        with ThreadPoolExecutor(max_workers=10) as executor:
            for i, result in enumerate(executor.map(_helper, [p for p in protein_names])):
                print(f"Processed {protein_names[i]}...")


    def run(self):

        if self.reference:
            self.ref_tofasta()
        if self.others:
            self.others_tofasta()


def main():
  fire.Fire(ProcessRaw)