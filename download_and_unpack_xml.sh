#!/bin/bash
set -e

# enwiki link on https://dumps.wikimedia.org/backup-index.html
# ex: https://dumps.wikimedia.org/enwiki/20221020/enwiki-20221020-pages-articles-multistream4.xml-p311330p558391.bz2
# latest dumps also at https://dumps.wikimedia.org/enwiki/latest/
# ex: https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2
DOWNLOAD_URL="https://dumps.wikimedia.org/enwiki/20221020/enwiki-20221020-pages-articles-multistream4.xml-p311330p558391.bz2"
FILE_NAME="wiki.xml"
ARCHIVE_OUTPUT_NAME="${FILE_NAME}.bz2"

if [ ! -f  "${FILE_NAME}" ]
then
  echo "Downloading dump from ${DOWNLOAD_URL}"
  curl $DOWNLOAD_URL -o $ARCHIVE_OUTPUT_NAME
  echo "Decompressing dump"
  bzip2 -d $ARCHIVE_OUTPUT_NAME
else
  echo "Decompressed dump found. Skipping download"
fi

echo "Extracting pages to json"
python parse_wikipedia_xml.py
