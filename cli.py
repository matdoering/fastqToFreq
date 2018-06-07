"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mminvar` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``minvar.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``minvar.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import os
import sys

from pkg_resources import (get_distribution, DistributionNotFound, resource_exists)
# resource_filename)

try:
    __version__ = get_distribution('minvar').version
    HCV_references = resource_exists(__name__, 'db/HCV/subtype_references.fasta')

except DistributionNotFound:
    # package is not installed
    pass

files_to_remove = [
    'calls_1.vcf.gz', 'cnsref.amb', 'cnsref.ann', 'cnsref.bwt', 'hq_smp.fastq',
    'hq_smp.fasta', 'hq_2_cns_final.bam', 'hq_2_cns_final.bam.bai',
    'cnsref.pac', 'cnsref.sa', 'high_quality.fastq', 'loc_res.tsv',
    'outblast.xml', 'refcon_sorted.bam', 'refcon_sorted.bam.bai',
    'sample_hq.fasta', 'phased.csv']

# parse command line
parser = argparse.ArgumentParser()
# First define all option groups
group1 = parser.add_argument_group('Input files', 'Required input')
group1.add_argument("-f", "--fastq", default="", type=str, dest="f",
                    help="input reads in fastq format")
group1.add_argument("-r", "--recal", action="store_true",
                    help="turn on recalibration with GATK <default: %(default)s>", default=False)
group1.add_argument("-k", "--keep", action="store_true",
                    help="keep intermediate files <default: %(default)s>", default=False)
group1.add_argument('-v', '--version', action='version', version=__version__)

# exit so that log file is not written
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()


def main(args=None):
    """What the main does."""
    import logging
    import logging.handlers

    args = parser.parse_args(args=args)

    log_format = '%(levelname)s %(asctime)s %(filename)s: %(funcName)s() %(lineno)d: \t%(message)s'
    logging.basicConfig(filename='minvar.log', level=logging.INFO, format=log_format, datefmt='%Y/%m/%d %H:%M:%S')
    logging.info(' '.join(sys.argv))

    from minvar import prepare
    cns_file, prepared_bam, org_found = prepare.main(args.f)
    '''
    from minvar import callvar
    called_file, called_bam = callvar.main(ref_file=cns_file, bamfile=prepared_bam, caller='lofreq',
                                           recalibrate=args.recal)

    from minvar import annotate
    annotate.main(vcf_file=called_file, ref_file=cns_file, bam_file=called_bam, organism=org_found)

    from minvar import reportdrm
    reportdrm.main(org=org_found, subtype_file='subtype_evidence.csv', fastq=args.f, version=__version__)
    '''
    if not args.keep:
        for f in files_to_remove:
            try:
                os.remove(f)
            except FileNotFoundError:
                pass
