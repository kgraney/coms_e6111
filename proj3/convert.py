import argparse
import data

parser = argparse.ArgumentParser()
parser.add_argument('in_file', type=str, help='Input CSV file from nyc.gov (gzipped)')
parser.add_argument('out_file', type=str, help='Output file (gzipped csv)')

def main():
    args = parser.parse_args()
    item_list = data.ParseFile(args.in_file)
    data.WriteIntegratedDataset(args.out_file, item_list)

if __name__ == '__main__':
    main()
