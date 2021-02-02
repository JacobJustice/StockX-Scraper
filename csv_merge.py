import os
import glob
import pandas as pd
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
    merge_csv("./data/sneakers/retro-jordans/air-jordan-1/"
                , output_name="air_jordan_1.csv")

if __name__ == "__main__":
    main()

