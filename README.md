# pysurveycto

Python library to use the SurveyCTO API to download data

## API Options

* JSON format: https://servername.surveycto.com/api/v2/forms/data/wide/json/formid?date=
  - servername
  - form_id
  - date (0 for all and 3 different formats)
  - review status

* Encrypted forms
  - servername
  - form_id
  - date (0 for all and 3 different formats)
  - private key
  - review status

* CSV format: https://servername.surveycto.com/api/v1/forms/data/csv/formid
  - servername
  - form_id
  - long or wide
  - long - files and repeatgroup
  - set value for linebreak using POST before fetching data
  - review status

* Server Dataset
  - servername
  - datasetid

* Downloading attachments?
  - media files, pictures etc.

