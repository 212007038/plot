import wfdb
import os
import argparse  # command line parser

__version__ = '1.0'  # version of script


def main(arg_list=None):
    # region Command Line
    ###############################################################################
    # Get command line arguments.
    parser = argparse.ArgumentParser(description="Plot given MIT file")
    parser.add_argument('-i', dest='input_file',
                        help='name of MIT waveform to plot with annotations', required=True)
    parser.add_argument('--version', action='version', help='Print version.',
                        version='%(prog)s Version {version}'.format(version=__version__))

    # Parse the command line arguments
    args = parser.parse_args(arg_list)

    ###############################################################################
    # Test for existence of the directory.
    if os.path.isfile(args.input_file) is False:
        print('ERROR, ' + args.input_file + ' does not exist')
        print('\n\n')
        parser.print_help()
        return -1

    # endregion

    filename, file_extension = os.path.splitext(args.input_file)

    # Create record and annotation objects.
    # Only get the first 2 channels.
    rec = wfdb.rdsamp(filename, channels=[0])
    sample_count = rec.siglen
    rec = wfdb.rdsamp(filename, channels=[0], sampto=sample_count-10)

    # Does an annotation file exist?
    if os.path.isfile(filename + '.prf' ) is True:
        an_file = wfdb.rdann(filename, annotator='prf', sampto=sample_count-10)
    else:
        an_file = None

    wfdb.plotrec(rec, timeunits='seconds', figsize=(20, 20), annotation=an_file, ecggrids='all')

###############################################################################
if __name__ == '__main__':
    rv = main()
    exit(rv)
