# pysurveycto

Python library to use the SurveyCTO API to download data


# Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Use Cases](#usecases)
* [License](#license)
* [SCTO API Options](#apioptions)


<a name="installation"></a>
# Installation

## Prerequisites

- Python version 2.6, 2.7, 3.4, 3.5 or 3.6

## Install Package
```bash
pip install pysurveycto
```


<a name="usage"></a>
# Usage

```python
SurveyCTOObject(server_name, username, password, keyfile=False)
```
Initialize SCTO Object
Parameters:
- server_name (str): SurveyCTO server name
- username (str): SurveyCTO login username
- password (str): SurveyCTO login password
- keyfile (str, optional)

```python
get_form_data(form_id, format=’csv’, shape=’wide’, date=None, review_status='approved', repeat_groups=None, line_breaks=None)
```
Fetch SurveyCTO form data in json or csv formats
Parameters
- form_id (str): The form_id of the SurveyCTO form.
- format (str, optional): The format of the returned data. Allowed values are: json, csv(default).
- shape (str, optional): The shape of the returned data. Allowed values are: wide, long. shape=’long’ can only be specified when returning data in csv format.
- date (str, optional): Return only the form submissions where CompletionDate is greater than the given date (in UTC). Can only be specified when returning data in json format.
- review_status (str, optional): Return only the form submissions with given review status. Allowed values are: approved(default), rejected, pending and more than one value concatenated with | or with commas.
- repeat_groups (bool, optional): Return a dictionary object containing the main form data along with the repeat groups. Can only be specified when returning long data, in which case it will default to true.
- line_breaks (str, optional): Replace linebreaks in the csv data with some other character.

```python
get_repeatgroup(form_id, repeat_group_name, review_status='approved', line_breaks=None)
```
Fetch SurveyCTO form's repeatgroup data
Parameters
- form_id (str): The form_id of the SurveyCTO form.
- repeat_group_name (str): Form's repeat group name.
- review_status (str, optional): Return only the form submissions with given review status. Allowed values are: approved(default), rejected, pending and more than one value concatenated with | or with commas.
- line_breaks (str, optional): Replace linebreaks in the csv data with some other character.

```python
get_server_dataset(dataset_id, line_breaks=None)
```
Fetch SurveyCTO server dataset data
Parameters
- dataset_id (str): The server dataset id of the SurveyCTO dataset
- line_breaks (str, optional): Replace linebreaks in the csv data with some other character.

```python
get_attachment(url)
```
Fetch form's file attachments like media/audio/images from SurveyCTO
Parameters
- url (str): The URL to fetch the attached file


<a name="usecases"></a>
# Use Cases

- Get a wide csv
```python
get_form_data(form_id)
```

- Get a wide json
```python
get_form_data(form_id, format=’json’)
```

- Get a long csv with repeat groups
```python
get_form_data(form_id, shape=’long’)
```

- Get a long csv without repeat groups
```python
get_form_data(form_id, shape=’long’, repeat_groups=false)
```

- Get a wide json starting after a given CompletionDate
```python
get_form_data(form_id, format=’json’, date=my_datetime)
```


<a name="license"></a>
# License
[The MIT License (MIT)](LICENSE.md)


<a name="apioptions"></a>
# SCTO API Options

[SCTO API Documentation](https://support.surveycto.com/hc/en-us/articles/360033156894?flash_digest=0a6eded7694409181788cc46a7026897850d65b5&flash_digest=d76dde7c3ffc40f4a7f0ebd87596d32f3a52304f)

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

