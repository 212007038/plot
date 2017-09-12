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
                        help='name of MIT waveform to plot with annotations (if present)', required=True)
    parser.add_argument('-s', dest='tail_samples_removed', type=int, default=0,
                        help='number of sample to remove from the end, optimizes plot, defaults to zero',
                        required=False)
    parser.add_argument('--version', action='version', help='Print version.',
                        version='%(prog)s Version {version}'.format(version=__version__))

    # Parse the command line arguments
    args = parser.parse_args(arg_list)

    ###############################################################################
    # Test for existence of the file.
    if os.path.isfile(args.input_file) is False:
        print('ERROR, ' + args.input_file + ' does not exist')
        print('\n\n')
        parser.print_help()
        return -1

    # endregion

    filename, file_extension = os.path.splitext(args.input_file)

    # Get the signal length by reading the header.
    hea = wfdb.rdheader(filename)
    sample_count = hea.siglen

    # Read the user given record.  Only get the first channels.
    rec = wfdb.rdsamp(filename, channels=[0], sampto=sample_count-args.tail_samples_removed)

    # Does an annotation file exist?
    an_file = None
    if os.path.isfile(filename + '.prf') is True:
        an_file = wfdb.rdann(filename, annotator='prf', sampto=sample_count-args.tail_samples_removed)

    # Construct a title
    plot_title = '{0:s}, Sample count: {1:d}, Pace count: {2:d}'.format(os.path.basename(args.input_file), sample_count,
                                                                        len(an_file.annsamp))

    # Plot...
    wfdb.plotrec(rec, title=plot_title, timeunits='seconds', figsize=(10, 5), annotation=an_file, ecggrids='all')


###############################################################################
if __name__ == '__main__':
    rv = main()
    exit(rv)
