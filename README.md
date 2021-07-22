# pysurveycto

Python library to download data collected on SurveyCTO data collection app using SurveyCTO REST API.

# Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Use Cases](#usecases)
* [License](#license)
* [SCTO API Options](#apioptions)


<a name="installation"></a>
# Installation

## Prerequisites

- Python version >= 3

## Install Package
```bash
pip install pysurveycto
```


<a name="usage"></a>
# Usage

## Initialize SCTO Object
```python
SurveyCTOObject(server_name, 
                username, 
                password)
```
  *Parameters:*
  - **server_name** *(str)*: SurveyCTO server name
  - **username** *(str)*: SurveyCTO login username
  - **password** *(str)*: SurveyCTO login password


## Methods:

* 
  ```python
  get_form_data(form_id, 
                format='csv', 
                shape='wide', 
                oldest_completion_date=None, 
                review_status=None, 
                repeat_groups=None, 
                line_breaks=None, 
                key=False)
  ```
  <p>Fetch SurveyCTO form data in json or csv formats.

    *Parameters:*
    - **form_id** *(str)*: The form_id of the SurveyCTO form.
    - **format** *(str, optional)*: The format of the returned data. Allowed values are: json, csv(default).
    - **shape** *(str, optional)*: The shape of the returned data. Allowed values are: wide(default), long. shape=’long’ can only be specified when returning data in csv format.
    - **oldest_completion_date** *(datetime.date or datetime.datetime object, optional)*: Return only the form submissions where CompletionDate is greater than or equal to the given date (in UTC). Can only be specified when returning data in json format.
    - **review_status** *(list, optional)*: Return only the form submissions with given review status. Allowed values in the list are: approved(default), rejected, pending. This option is only applicable for forms using the “Review and Corrections” workflow on the SurveyCTO web console.
    - **repeat_groups** *(bool, optional)*: Return a dictionary object containing the main form data along with the repeat groups. Can only be specified when returning long data, in which case it will default to true.
    - **line_breaks** *(str, optional)*: Replace line breaks in the csv data with some other character.
    - **key** *(str, optional)*: The private key to decrypt form data in binary/string. This can be used only for json extracts without a review_status parameter.

    *Returns:* Form data in json or csv (wide or long) format depending on the parameters
  </p>


*
  ```python
  get_repeatgroup(form_id, 
                  repeat_group_name, 
                  review_status=None, 
                  line_breaks=None)
  ```
  <p>Fetch SurveyCTO form's repeat group data.

    *Parameters:*
    - **form_id** *(str)*: The form_id of the SurveyCTO form.
    - **repeat_group_name** *(str)*: Form's repeat group name.
    - **review_status** *(list, optional)*: Return only the form submissions with given review status. Allowed values in the list are: approved(default), rejected, pending. This option is only applicable for forms using the “Review and Corrections” workflow on the SurveyCTO web console.
    - **line_breaks** *(str, optional)*: Replace line breaks in the csv data with some other character.
  
    *Returns:* Repeat group data in csv format
  </p>

      
*
  ```python
  get_server_dataset(dataset_id, 
                     line_breaks=None)
  ```
  <p>Fetch SurveyCTO server dataset data.

    *Parameters:*
    - **dataset_id** *(str)*: The server dataset id of the SurveyCTO dataset.
    - **line_breaks** *(str, optional)*: Replace line breaks in the csv data with some other character.

    *Returns:* Server dataset data in csv format
  </p>

      
*
  ```python
  get_attachment(url,
                 key=False)
  ```
  <p>Fetch form's file attachments like media/audio/images from SurveyCTO.

    *Parameters:*
    - **url** *(str)*: The URL to the attached file. 
    - **key** *(str, optional)*: The private key to decrypt an encrypted attachment in binary/string. 

    *Returns:* The url content
  </p>    

      
*
  ```python
  get_form_definition(form_id)
  ```
  <p>Fetch form's definition from SurveyCTO

    *Parameters:*
    - **form_id** *(str)*: The form_id of the SurveyCTO form.

    *Returns:* The form definition in JSON format
  </p>    
    

<a name="usecases"></a>
# Use Cases

```python
import pysurveycto
scto = pysurveycto.SurveyCTOObject(server_name, username, password)
```

- Get a wide csv
  ```python
  scto.get_form_data(form_id)
  ```

- Get a long csv with all repeat groups (Returns a dictionary with repeat group names as keys and csv data for the repeat groups as values)
  ```python
  scto.get_form_data(form_id, shape='long')
  ```

- Get a long csv without repeat groups
  ```python
  scto.get_form_data(form_id, shape='long', repeat_groups=false)
  ```

- Get a wide csv with line breaks replaced with space with only pending-review submissions
  ```python
  scto.get_form_data(form_id, line_breaks=' ', review_status=['pending'])
  ```

- Get a wide json
  ```python
  scto.get_form_data(form_id, format='json')
  ```

- Get a wide json with forms completed after a given CompletionDate (inclusive)
  ```python
  date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
  scto.get_form_data(form_id, format='json', oldest_completion_date=date_input)
  ```

- Get a wide json for encrypted form starting after a given CompletionDate (inclusive)
  ```python
  key_data = open('<path to keyfile>', 'rb')
  scto.get_form_data(form_id, format='json', oldest_completion_date=my_datetime, key=key_data)
  ```

- Get a server dataset with line breaks replaced with space
  ```python
  scto.get_form_data(dataset_id, line_breaks=' ')
  ```

- Get a media file attachment and save to file
  ```python
  data = scto.get_attachment(url)
  f = open(file_name, 'wb')
  f.write(data)
  f.close()
  ```

- Get form definition and save to excel file
  ```python
  data = scto.get_form_definition(form_id)
  questions_df = pd.DataFrame(
      data["fieldsRowsAndColumns"][1:],
      columns=data["fieldsRowsAndColumns"][0],
  )
  choices_df = pd.DataFrame(
      data["choicesRowsAndColumns"][1:],
      columns=data["choicesRowsAndColumns"][0],
  )
  settings_df = pd.DataFrame(
      data["settingsRowsAndColumns"][1:],
      columns=data["settingsRowsAndColumns"][0],
  )

  writer = pd.ExcelWriter(file_name, engine="openpyxl")
  questions_df.to_excel(writer, sheet_name="survey", index=False)
  choices_df.to_excel(writer, sheet_name="choices", index=False)
  settings_df.to_excel(writer, sheet_name="settings", index=False)
  writer.save()
  ```


<a name="license"></a>
# License
[The MIT License (MIT)](LICENSE.md)


<a name="apioptions"></a>
# SCTO API Options

[SCTO API Documentation](https://support.surveycto.com/hc/en-us/articles/360033156894?flash_digest=0a6eded7694409181788cc46a7026897850d65b5&flash_digest=d76dde7c3ffc40f4a7f0ebd87596d32f3a52304f)
