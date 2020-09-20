import argparse, os

# create an argument parser so that the user can pass command line arguments
parser = argparse.ArgumentParser(description = 'Censors the words on an image')
parser.add_argument('--input-file', '-i', type = str, help = 'Input file path', required = True)
parser.add_argument('--output-file', '-o', type = str, help = 'Output file path', required = True)
parser.add_argument('--phrase', '-p', type = str, help = 'Phrase to censor', required = True)

# parse the command line args
arguments = parser.parse_args()

# check that the input file exists, and if it doesnt then exit with an error
if (not os.path.exists(arguments.input_file)):
    print('Input file does not exist.')
    exit(1)