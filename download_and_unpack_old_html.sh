#!/bin/bash
set -e

# https://dumps.wikimedia.org/other/static_html_dumps
DOWNLOAD_URL="https://dumps.wikimedia.org/other/static_html_dumps/2008-03/aa/wikipedia-aa-html.7z"
FOLDER_NAME="html_wiki"
ARCHIVE_OUTPUT_NAME="${FOLDER_NAME}.7z"

if [ ! -f  "${FOLDER_NAME}" ]
then
  echo "Downloading dump from ${DOWNLOAD_URL}"
  curl $DOWNLOAD_URL -o $ARCHIVE_OUTPUT_NAME
  echo "Decompressing dump"
  7za e $ARCHIVE_OUTPUT_NAME
else
  echo "Decompressed dump found. Skipping download"
fi

