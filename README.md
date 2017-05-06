# Instagram ML Project Module: Data Preprocessor

## Installation
Clone or unzip into a folder and install dependencies with pip3.

```
$ pip install -r requirements.txt
```

## Run
Put profiles crawled using [Instagram Crawler](https://github.com/simonseo/instacrawler-privateapi) into a folder (by default `profiles/` folder). The JSON format must follow that defined in the above repository.

Run by typing in `python create_dataset.py`.


## Detailed usage

This script is divided into 6 parts.

1. Process profile JSON files and save them as a CSV for easier scripting
1. Download all photos in each Instagram post
1. Resize photos into a uniform square format
1. Retrieve RGB values from the resized photos and save them in the following order:

    ```
    R,R,R,R
    G,G,G,G
    B,B,B,B
    R,R,R,R
    G,G,G,G
    B,B,B,B
    ...
    ```

1. Clean up erroneous files and records that were created due to users deleting posts between the time of crawling profiles and processing them.
1. Save labels. Currently, `label := # of likes / # of followers`

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
                        6: Save labels (currently supports label = ratio of #likes/#followers*100). Must use 5 beforehand
```
