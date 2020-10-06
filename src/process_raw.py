import fire
from Bio import SeqIO
from concurrent.futures import ThreadPoolExecutor

from .conf import DATA_INTERIM
from .conf import protein_names, reference_seq


def parse_records(rawfile, others):
    # Parse `rawfile` and separate proteins as reference vs others. This take aprox 1-2 minutes
    records = SeqIO.parse(rawfile, "fasta")

    ref_seqs = dict()
    other_seqs = dict()
    for i, r in enumerate(records, 1):
        head = r.description
        head_sections = head.split("|")
        # relevant header sections
        prot_name = head_sections[0]
        sample_id = head_sections[3]
        country = head_sections[-1]

        if reference_seq == sample_id:
            ref_seqs[prot_name+"|"+head_sections[1]+'|'+country] = str(r.seq)
        else:
            if others:
                other_seqs[prot_name+"|"+head_sections[1]+'|'+country] = str(r.seq)

    return ref_seqs, other_seqs


def write_others(others_dict, outfolder, njobs):
    """
    Write SARS-CoV-2 Non-Reference Sample proteins to Fasta Files.
    """

    def _proteins(d, protein):
        """
        Select specific protein from `others_dict` dictionary
        and write to respective Fasta.
        """

        selected = filter(lambda items: items[0].split('|')[0] == protein, d.items())
        with open(outfolder / 'sars2_others_{}.fasta'.format(protein), 'w') as f:
            for h, seq in selected:
                f.write('>{}\n'.format(h))
                f.write('{}\n'.format(seq))

    def _helper(protein):
        """ Helper function for running multiprocessing """
        return _proteins(others_dict, protein)

    with ThreadPoolExecutor(max_workers=njobs) as executor:
        for i, result in enumerate(executor.map(_helper, [p for p in protein_names])):
            print(f"Processed {protein_names[i]}...")

def write_reference(ref_dict, outfolder):
    """
    Write SARS-CoV-2 Reference Sample proteins to Fasta Files.
    """

    for k, v in ref_dict.items():
        name = k.split("|")[0]
        with open(outfolder / 'sars2_refWuhan_{}.fasta'.format(name), 'w') as f:
            f.write('>{}\n'.format(k))
            f.write('{}\n'.format(v))


class ProcessRaw(object):
    """
    CLI to process SARS-CoV-2 proteins Fasta File from GISAID.

    Parameters
    ----------
    others : bool, optional
        Process or not Non-reference samples proteins. (default: True)
    outdir : str, optional
        Specify folder to write files. (default: `sars2_proteins`)
    """

    def __init__(self, outdir='sars2_proteins', others=True, njobs=4):

        self._sars2protein_folder = None
        self.njobs = njobs
        self.outdir = outdir
        self.others = others


    def _config(self):

        print('Setting up SARS-CoV-2 proteome folder')
        self._sars2protein_folder = DATA_INTERIM / self.outdir
        if not self._sars2protein_folder.is_dir():
            self._sars2protein_folder.mkdir()
        print(f'Folder : {self.outdir}')
        print(f'Process Non-reference Proteins: {self.others}')

    def process(self, rawfile):
        """
        Process SARS-CoV-2 Samples proteins and write out to respective Fasta Files.

        Parameters
        ----------
        rawfile : str
            GISAID Fasta File with all SARS-CoV-2 proteins.
        """

        # Setting up Folder
        self._config()
        # Parsing File
        print(f'Parsing {rawfile} ...')
        ref_seqs, others_seqs = parse_records(rawfile, others=self.others)

        # Write references proteins
        print('Writing SARS-CoV-2 Reference Sample proteins...')
        write_reference(ref_seqs, self._sars2protein_folder)
        if self.others:
            print('Writing SARS-CoV-2 Non-Reference Sample proteins...')
            write_others(others_seqs, self._sars2protein_folder, njobs=self.njobs)

def main():
  fire.Fire(ProcessRaw)