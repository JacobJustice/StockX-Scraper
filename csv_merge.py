import os
import glob
import pandas as pd
import argparse
import sys

parser = argparse.ArgumentParser(description='Merge all csvs in a directory into one')
parser.add_argument('-d', '--directory', required=True, help='Directory containing .csv you wish to merge')
parser.add_argument('-o', '--output', default='output',help='Name of output file with no file ending')
args = parser.parse_args(sys.argv[1:])

"""
merge_csvs in directory

@param directory_path: path to directory containing csv files to be merged

"""
def merge_csv(directory_path, output_name="combined_csv.csv"):
    os.chdir(directory_path)
    print(directory_path, output_name)
    all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
    print(all_filenames)

    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

    combined_csv.to_csv( output_name
            , index=False
            , encoding='utf-8-sig'
            , mode='w')

def main():
    global args
    directory = args.directory
    outname = args.output
    merge_csv(directory, output_name= outname + ".csv")

if __name__ == "__main__":
    main()

