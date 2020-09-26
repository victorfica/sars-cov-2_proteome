from Bio.Application import _Option, _Switch, _Argument, AbstractCommandline

class Bowtie2Commandline(AbstractCommandline):
    """
    Method names, input file paths are required. Application will not run until these 2 arguments are provided.
    If you want results printed, both format an input file path have to be provided


    AA Conservation version 1.1 (19 April 2017)

    This program allows calculation of conservation of amino acids in
    multiple sequence alignments.
    It implements 17 different conservation scores as described by Valdar in
    his paper (Scoring Residue Conservation, PROTEINS: Structure, Function
    and  Bioinformatics 48:227-241 (2002)) and SMERFS scoring algorithm as described
    by Manning, Jefferson and Barton (The contrasting properties of conservation
    and correlated phylogeny in protein functional residue prediction,
    BMC Bioinformatics (2008)).

    The conservation algorithms supported are:

    KABAT, JORES, SCHNEIDER, SHENKIN, GERSTEIN, TAYLOR_GAPS, TAYLOR_NO_GAPS,
    ZVELIBIL, KARLIN, ARMON, THOMPSON, NOT_LANCET, MIRNY, WILLIAMSON,
    LANDGRAF, SANDER, VALDAR, SMERFS

    Input format is either a FASTA formatted file containing aligned sequences with
    gaps or a Clustal alignment. The valid gap characters are *, -, space character,
    X and . (a dot). By default program prints the results to the command window.
    If the output file is provided the results are printed to the file in two
    possible formats with or without an alignment.
    If format is not specified, the program outputs conservation scores without
    alignment. The scores are not normalized by default but they can be (see below).
    SMERFS default parameters are window width of 7, column score is set to
    the middle column (MID_SCORE), gap% cutoff of 0.1. Different parameters for SMERFS
    can be provided (see below). Details of the program execution can be recorded to
    a separate file if an appropriate file path is provided.

    EXAMPLE HOW TO RUN THE PROGRAM:
    java -jar <jar name> -m=KABAT,SMERFS -i=prot1 -o=prot1_results -n

    As a result of the execution KABAT and SMERFS scores will be calculated.
    Input comes form prot1 file and an output without an alignment is recorded to
    prot1_results file.

    Authors: Peter Troshin, Agnieszka Golicz, David Martin, Fábio Madeira and Geoff J. Barton.
    Please visit http://www.compbio.dundee.ac.uk/aacon for further information.
    """

    def __init__(self, cmd="compbio-conservation-1.1.jar", **kwargs):
        """Initialize the class."""
        self.java_jar = "java -jar "
        self.program_name = self.java_jar + cmd
        self.parameters = [
            # ***Inputs***
            _Option(
                ["-m", "m"],
                """precedes a comma separated list of method names
                EXAMPLE: 'KABAT,JORE,GERSTEIN'
                Optional, if no method is specified request for all is assumed.""",
                checker_function=lambda x: isinstance(x, str),
                equate=True
            ),
            _Option(
                ["-i", "i"],
                """precedes a comma separated list of method names
                EXAMPLE: 'KABAT,JORE,GERSTEIN'
                Optional, if no method is specified request for all is assumed.""",
                checker_function=lambda x: isinstance(x, str),
                filename=True,
                required=True,
                equate=True
            ),
            _Switch(
                ["-q", "q"],
                "query input files are FASTQ .fq/.fastq (default)."
            ),
            _Switch(
                ["--tab5", "tab5"],
                "query input files are TAB5 .tab5."
            ),
            _Switch(
                ["--tab6", "tab6"],
                "query input files are TAB6 .tab6."
            ),
            _Switch(
                ["--qseq", "qseq"],
                "query input files are in Illumina's qseq format."
            ),
            _Switch(
                ["-f", "f"],
                "query input files are (multi-)FASTA .fa/.mfa."
            ),
            _Switch(
                ["-r", "r"],
                "query input files are raw one-sequence-per-line."
            ),
            _Option(
                ["-F", "F"],
                """query input files are continuous FASTA where reads are substrings (k-mers) extracted from 
                a FASTA file <s> and aligned at offsets 1, 1+i, 1+2i ... end of reference.""",
                checker_function=lambda x: isinstance(x, str),
                equate=False
            ),
            _Switch(
                ["-c", "c"],
                "<m1>, <m2>, <r> are sequences themselves, not files."
            ),
            _Option(
                ["-s", "--skip", "skip"],
                "skip the first <int> reads/pairs in the input (none)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["-u", "--upto", "upto"],
                "stop after first <int> reads/pairs (no limit)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["-5", "--trim5", "trim5"],
                "trim <int> bases from 5'/left end of reads (0)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["-3", "--trim3", "trim3"],
                "trim <int> bases from 3'/right end of reads (0)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["--trim-to", "trim_to"],
                """trim reads exceeding <int> bases from either 3' or 5' end
                If the read end is not specified then it defaults to 3 (0)""",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Switch(
                ["--phred33", "phred33"],
                "qualities are Phred+33 (default)"
            ),
            _Switch(
                ["--phred64", "phred64"],
                "qualities are Phred+64"
            ),
            _Switch(
                ["--int-quals", "int_quals"],
                "qualities encoded as space-delimited integers"
            ),
            # ***Presets***
            # For end-to-end
            _Switch(
                ["--very-fast", "very_fast"],
                "Same as: -D 5 -R 1 -N 0 -L 22 -i S,0,2.50"
            ),
            _Switch(
                ["--fast", "fast"],
                "Same as: -D 10 -R 2 -N 0 -L 22 -i S,0,2.50"
            ),
            _Switch(
                ["--sensitive", "sensitive"],
                "Same as: -D 15 -R 2 -N 0 -L 22 -i S,1,1.15 (default)"
            ),
            _Switch(
                ["--very-sensitive", "very_sensitive"],
                "Same as: -D 20 -R 3 -N 0 -L 20 -i S,1,0.50"
            ),
            # For local
            _Switch(
                ["--very-fast-local", "very_fast_local"],
                "Same as: -D 5 -R 1 -N 0 -L 25 -i S,1,2.00"
            ),
            _Switch(
                ["--fast-local", "fast_local"],
                "Same as: -D 10 -R 2 -N 0 -L 22 -i S,1,1.75"
            ),
            _Switch(
                ["--sensitive-local", "sensitive_local"],
                "Same as: -D 15 -R 2 -N 0 -L 20 -i S,1,0.75 (default)"
            ),
            _Switch(
                ["--very-sensitive-local", "very_sensitive_local"],
                "Same as: -D 20 -R 3 -N 0 -L 20 -i S,1,0.50"
            ),
            # ***Alingment***
            _Option(
                ["-N", "N"],
                "max # mismatches in seed alignment; can be 0 or 1 (0)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["-L", "L"],
                "length of seed substrings; must be >3, <32 (22)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["-i", "i"],
                "interval between seed substrings w/r/t read len (S,1,1.15)",
                checker_function=lambda x: isinstance(x, str),
                equate=False,
            ),
            _Option(
                ["--n-ceil", "n_ceil"],
                "func for max # non-A/C/G/Ts permitted in aln (L,0,0.15)",
                checker_function=lambda x: isinstance(x, str),
                equate=False,
            ),
            _Option(
                ["--dpad", "dpad"],
                "include <int> extra ref chars on sides of DP table (15)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["--gbar", "gbar"],
                "disallow gaps within <int> nucs of read extremes (4)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Switch(
                ["--ignore-quals", "ignore_equals"],
                "treat all quality values as 30 on Phred scale (off)",
            ),
            _Switch(
                ["--nofw", "nofw"],
                "do not align forward (original) version of read (off)"
            ),
            _Switch(
                ["--norc", "norc"],
                "do not align reverse-complement version of read (off)",
            ),
            _Switch(
                ["--no-1mm-upfront", "no_1mm_upfront"],
                """do not allow 1 mismatch alignments before attempting to
                 scan for the optimal seeded alignments""",
            ),
            _Switch(
                ["--end-to-end", "end_to_end"],
                "entire read must align; no clipping (on)",
            ),
            _Switch(
                ["--loca", "local"],
                "local alignment; ends might be soft clipped (off)",
            ),
            # ***Scoring***
            _Option(
                ["--ma", "ma"],
                "match bonus (0 for --end-to-end, 2 for --local)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["--mp", "mp"],
                "max penalty for mismatch; lower qual = lower penalty (6)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["--np", "np"],
                "penalty for non-A/C/G/Ts in read/ref (1)",
                checker_function=lambda x: isinstance(x, int),
                equate=False,
            ),
            _Option(
                ["--rdg", "rdg"],
                "read gap open, extend penalties (5,3) eg '5,3' ",
                checker_function=lambda x: isinstance(x, str),
                equate=False,
            )
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)