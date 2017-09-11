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
                        help='number of sample to remove from the end, optimizes plot, defaults to zero', required=False)
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
    rec = wfdb.rdsamp(filename, channels=[0], sampto=sample_count-args.tail_samples_removed)

    # Does an annotation file exist?
    if os.path.isfile(filename + '.prf') is True:
        an_file = wfdb.rdann(filename, annotator='prf', sampto=sample_count-args.tail_samples_removed)
    else:
        an_file = None

    # Construct a title
    plot_title = filename + ', Sample count:  ' + str(sample_count) + ', Pace count: ' + str(len(an_file.annsamp))

    wfdb.plotrec(rec, title=plot_title, timeunits='seconds', figsize=(10, 10), annotation=an_file, ecggrids='all')


###############################################################################
if __name__ == '__main__':
    rv = main()
    exit(rv)
