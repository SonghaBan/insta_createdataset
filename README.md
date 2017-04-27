# Instagram ML Project Module: Data Preprocessor

## Installation
Clone or unzip into a folder and install dependencies with pip3.

```
$ pip install -r requirements.txt
```

## Run
Put profiles crawled using [instagram crawler](https://github.com/simonseo/instacrawler-privateapi) into a folder (by default `profiles/` folder).

Run by typing in `python create_dataset.py`.


## Detailed usage
```
$ python create_dataset.py -h
usage: create_dataset.py [-h] [-s IMG_SIZE] [--overwrite] [--stage STAGE]

This script preprocesses data collected from crawling instagram

optional arguments:
  -h, --help            show this help message and exit
  -s IMG_SIZE, --imgsize IMG_SIZE
                        Image resize dimension. Default value is 100.
  --overwrite           overwrite existing files in download or resize folders
  --stage STAGE         int values denoting which stage of the script to start from.
                        (empty): If it's your first run
                        1: Reprocess the JSON (not recommended to use alone)
                        2: Download all photos. See also: --overwrite
                        3: Resize photos. See also: -s, --overwrite
                        4: Process photos in resize directory and save as CSV.
                        5: If you want to clean up erroneous files and records detected during resize
                        6: Save labels (currently supports label = ratio of #likes/#followers). Must use 5 beforehand
```
