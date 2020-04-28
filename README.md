# pysurveycto

Python library to use the SurveyCTO API to download data

# Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Use Cases](#usecases)
* [License](#license)
* [SCTO API Options](#apioptions)

<br>

<a name="installation"></a>
# Installation

## Prerequisites

- Python version 2.6, 2.7, 3.4, 3.5 or 3.6

## Install Package
```bash
pip install pysurveycto
```

<br>

<a name="usage"></a>
# Usage

## Initialize SCTO Object
```python
SurveyCTOObject(server_name, username, password)
```
  *Parameters:*
  - server_name (str): SurveyCTO server name
  - username (str): SurveyCTO login username
  - password (str): SurveyCTO login password


## Methods:

* 
  ```python
  get_form_data(form_id, format=’csv’, shape=’wide’, date=None, review_status=None, repeat_groups=None, line_breaks=None, keyfile=False)
  ```
  <p>Fetch SurveyCTO form data in json or csv formats.

    *Parameters:*
    - **form_id** (str): The form_id of the SurveyCTO form.
    - **format** (str, optional): The format of the returned data. Allowed values are: json, csv(default).
    - **shape** (str, optional): The shape of the returned data. Allowed values are: wide(default), long. shape=’long’ can only be specified when returning data in csv format.
    - **date** (datetime.date or datetime.datetime object, optional): Return only the form submissions where CompletionDate is greater than the given date (in UTC). Can only be specified when returning data in json format.
    - **review_status** (list, optional): Return only the form submissions with given review status. Allowed values in the list are: approved(default), rejected, pending. This option is only applicable for forms using the “Review and Corrections” workflow on the SurveyCTO web console.
    - **repeat_groups** (bool, optional): Return a dictionary object containing the main form data along with the repeat groups. Can only be specified when returning long data, in which case it will default to true.
    - **line_breaks** (str, optional): Replace linebreaks in the csv data with some other character.
    - **keyfile**(str, optional): The private key to decrypt form data. This can be used only for json extracts without a review_status parameter.
  </p>
<br>

*
  ```python
  get_repeatgroup(form_id, repeat_group_name, review_status=None, line_breaks=None)
  ```
  <p>Fetch SurveyCTO form's repeatgroup data.

    *Parameters:*
    - **form_id** (str): The form_id of the SurveyCTO form.
    - **repeat_group_name** (str): Form's repeat group name.
    - **review_status** (list, optional): Return only the form submissions with given review status. Allowed values in the list are: approved(default), rejected, pending. This option is only applicable for forms using the “Review and Corrections” workflow on the SurveyCTO web console.
    - **line_breaks** (str, optional): Replace linebreaks in the csv data with some other character.
  </p>
<br>
      
*
  ```python
  get_server_dataset(dataset_id, line_breaks=None)
  ```
  <p>Fetch SurveyCTO server dataset data.

    *Parameters:*
    - **dataset_id** (str): The server dataset id of the SurveyCTO dataset.
    - **line_breaks** (str, optional): Replace linebreaks in the csv data with some other character.
  </p>
<br>
      
*
  ```python
  get_attachment(url)
  ```
  <p>Fetch form's file attachments like media/audio/images from SurveyCTO.

    *Parameters:*
    - **url** (str): The URL to the attached file.   
  </p>    
  
<br>

<a name="usecases"></a>
# Use Cases

```python
scto = SurveyCTOObject(server_name, username, password)
```

- Get a wide csv
  ```python
  scto.get_form_data(form_id)
  ```

- Get a long csv with repeat groups
  ```python
  scto.get_form_data(form_id, shape=’long’)
  ```

- Get a long csv without repeat groups
  ```python
  scto.get_form_data(form_id, shape=’long’, repeat_groups=false)
  ```

- Get a wide csv with linebreaks replaced with space with only pending-review submissions
  ```python
  scto.get_form_data(form_id, line_breaks=' ', review_status=['pending'])
  ```

- Get a wide json
  ```python
  scto.get_form_data(form_id, format=’json’)
  ```

- Get a wide json for encrypted form starting after a given CompletionDate
  ```python
  scto.get_form_data(form_id, format=’json’, date=my_datetime, keyfile='<path to keyfile>')
  ```

- Get a server dataset with linebreaks replaced with space
  ```python
  scto.get_form_data(dataset_id, line_breaks=' ')
  ```

<br>

<a name="license"></a>
# License
[The MIT License (MIT)](LICENSE.md)

<br>

<a name="apioptions"></a>
# SCTO API Options

[SCTO API Documentation](https://support.surveycto.com/hc/en-us/articles/360033156894?flash_digest=0a6eded7694409181788cc46a7026897850d65b5&flash_digest=d76dde7c3ffc40f4a7f0ebd87596d32f3a52304f)
