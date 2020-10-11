from Bio.Application import _Option, _Switch, _Argument, AbstractCommandline

class AAConCommandline(AbstractCommandline):
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
        #self.java_jar = "java -jar "
        self.program_name = cmd
        self.parameters = [
            # ***Inputs***
            _Option(
                ["-m", "m"],
                """comma separated list of method names
                EXAMPLE: 'KABAT,JORE,GERSTEIN'
                Optional, if no method is specified request for all is assumed.""",
                checker_function=lambda x: isinstance(x, str),
                equate=True,
                is_required=False
            ),
            _Option(
                ["-i", "i"],
                """full path to the input FASTA file, required""",
                checker_function=lambda x: isinstance(x, str),
                filename=True,
                is_required=True,
                equate=True
            ),
            _Option(
                ["-o", "o"],
                """full path to the output file, optional, if no output file is
                provided the program will output to the standard out.""",
                checker_function=lambda x: isinstance(x, str),
                filename=True,
                is_required=False,
                equate=True
            ),
            _Option(
                ["-t", "t"],
                """number of CPUs (CPU cores more precisely) to use. Optional,
                defaults to all processors available on the machine.""",
                checker_function=lambda x: isinstance(x, int),
                filename=False,
                is_required=False,
                equate=True
            ),
            _Option(
                ["-f", "f"],
                """format  of the results in the output file
                two different formats are possible:
                RESULT_WITH_ALIGNMENT
                RESULT_NO_ALIGNMENT
                Optional, if not specified RESULT_NO_ALIGNMENT is assumed""",
                checker_function=lambda x: isinstance(x, str),
                filename=False,
                is_required=False,
                equate=True
            ),
            _Option(
                ["-d", "d"],
                """full path to a file where program execution details are to be
                listed. Optional, if not provided, no execution statistics is produced.""",
                checker_function=lambda x: isinstance(x, str),
                filename=False,
                is_required=False,
                equate=True
            ),
            _Option(
                ["-g", "g"],
                """comma separated list of gap characters provided by the user, if
                you're using an unusual gap character (not a -,., ,*,X) you have to
                provide it. If you you provide this list you have to list all the gaps
                accepted. Including those that were previously treated as a default.
                Optional.""",
                checker_function=lambda x: isinstance(x, str),
                filename=False,
                is_required=False,
                equate=True
            ),
            _Switch(
                ["-n", "n"],
                """using this key causes the results to be normalized.
                    Normalized results have values between 0 and 1. Please note however, that
                    some results cannot be normalized. In such a case, the system returns not
                    normalized value, and log the issue to the standard error stream.
                    The following formula is used for normalization
                                    n = (d - dmin)/(dmax - dmin)
                    Negative results first converted to positive by adding an absolute value of
                    the most negative result. Optional."""
            ),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)