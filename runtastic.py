"""
Usage:
  runtastic.py -h
  runtastic.py [--unix-timestamp] [-o <output_file>] <folder>

Options:
  -h --help                Print this menu
  --unix-timestamp         Keeps the Unix timestamp instead of UTC datetime.
  -o <output_file>         The file to write output to.
"""

import json
from docopt import docopt

def collate_data(folder_path, do_convert_to_utc):
    import glob
    from datetime import datetime

    all_json_files = glob.glob(folder_path + '/*.json')
    all_json_data = []

    for json_file in all_json_files:
      with open(json_file) as f:
        data = json.load(f)
        if do_convert_to_utc:
          # Divide by 1000 to convert from ms to seconds.
          data['created_at'] = datetime.utcfromtimestamp(data['created_at']/1000).strftime('%Y-%m-%d %H:%M:%S')
          data['start_time'] = datetime.utcfromtimestamp(data['start_time']/1000).strftime('%Y-%m-%d %H:%M:%S')
          data['tracked_at'] = datetime.utcfromtimestamp(data['tracked_at']/1000).strftime('%Y-%m-%d %H:%M:%S')
          data['updated_at'] = datetime.utcfromtimestamp(data['updated_at']/1000).strftime('%Y-%m-%d %H:%M:%S')
        all_json_data.append(data)

    all_json_data.sort(key=lambda json_obj: json_obj['start_time'])
    return all_json_data

def main():
    args = docopt(__doc__)
    print(args)
    if '<folder>' in args:
      collated_json_data = collate_data(args['<folder>'], do_convert_to_utc=not args['--unix-timestamp'])
      if '-o' in args:
        with open(args['-o'], 'w') as f:
          json.dump(collated_json_data, f, indent=4)
      else:
        print(json.dumps(collated_json_data, indent=4))

if __name__ == '__main__':
    main()
