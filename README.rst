===========
pysurveycto
===========

Python library to download data collected on SurveyCTO data collection
app using SurveyCTO REST API.

Table of Contents
=================

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Use Cases <#use-cases>`__
-  `License <#license>`__
-  `SCTO API Options <#scto-api-options>`__


Installation
============

Prerequisites
-------------

-  Python version >= 3

Install Package
---------------

.. code:: bash

   pip install pysurveycto


Usage
=====

Initialize SCTO Object
----------------------

.. code:: python

   SurveyCTOObject(server_name, 
                   username, 
                   password)

*Parameters:*

-  **server\_name** *(str)*: SurveyCTO server name 
-  **username** *(str)*: SurveyCTO login username 
-  **password** *(str)*: SurveyCTO login password

Methods:
--------

-  
  .. code:: python
   
   get_form_data(form_id,
                 format='csv',
                 shape='wide',
                 oldest_completion_date=None,
                 review_status=None,
                 repeat_groups=None,
                 line_breaks=None,
                 key=False)

  Fetch SurveyCTO form data in json or csv formats.
  
  *Parameters:*

  -  **form\_id** *(str)*: The form\_id of the SurveyCTO form.
  -  **format** *(str, optional)*: The format of the returned data. Allowed values are: json, csv(default).
  -  **shape** *(str, optional)*: The shape of the returned data. Allowed values are: wide(default), long. shape=’long’ can only be specified when returning data in csv format.
  -  **oldest_completion_date** *(datetime.date or datetime.datetime object, optional)*: Return only the form submissions where CompletionDate is greater than or equal to the given date (in UTC). Can only be specified when returning data in json format.
  -  **review\_status** *(list, optional)*: Return only the form submissions with given review status. Allowed values in the list are: approved(default), rejected, pending. This option is only applicable for forms using the “Review and Corrections” workflow on the SurveyCTO web console.
  -  **repeat\_groups** *(bool, optional)*: Return a dictionary object containing the main form data along with the repeat groups. Can only be specified when returning long data, in which case it will default to true.
  -  **line\_breaks** *(str, optional)*: Replace line breaks in the csv data with some other character.
  -  **key** *(str, optional)*: The private key to decrypt form data in binary/string. This can be used only for json extracts without a review\_status parameter.

  *Returns:* Form data in json or csv (wide or long) format depending on the parameters


-  
  .. code:: python

   get_repeatgroup(form_id, 
                   repeat_group_name, 
                   review_status=None,                    
                   line_breaks=None) 

  Fetch SurveyCTO form's repeat group data.

  *Parameters:*

  -  **form\_id** *(str)*: The form\_id of the SurveyCTO form.
  -  **repeat\_group\_name** *(str)*: Form's repeat group name.
  -  **review\_status** *(list, optional)*: Return only the form submissions with given review status. Allowed values in the list are: approved(default), rejected, pending. This option is only applicable for forms using the “Review and Corrections” workflow on the SurveyCTO web console.
  -  **line\_breaks** *(str, optional)*: Replace line breaks in the csv data with some other character.

  *Returns:* Repeat group data in csv format


-  
  .. code:: python

   get_server_dataset(dataset_id,
                      line_breaks=None)

  Fetch SurveyCTO server dataset data.

  *Parameters:*

  -  **dataset\_id** *(str)*: The server dataset id of the SurveyCTO dataset.
  -  **line\_breaks** *(str, optional)*: Replace line breaks in the csv data with some other character.

  *Returns:* Server dataset data in csv format


-  
  .. code:: python

   get_attachment(url,
                  key=False)

  Fetch form's file attachments like media/audio/images from SurveyCTO.

  *Parameters:*

  -  **url** *(str)*: The URL to the attached file.
  -  **key** *(str, optional)*: The private key to decrypt an encrypted attachment in binary/string.

  *Returns:* The url content


-  
  .. code:: python

   get_form_definition(form_id)

  Fetch form's definition from SurveyCTO

  *Parameters:*

  -  **form\_id** *(str)*: The form\_id of the SurveyCTO form.

  *Returns:* The form definition in JSON format


Use Cases
=========

-  
  .. code:: python

   import pysurveycto
   scto = pysurveycto.SurveyCTOObject(server_name, username, password)

-  Get a wide csv:
    .. code:: python
    
     scto.get_form_data(form_id)


-  Get a long csv with all repeat groups (Returns a dictionary with repeat group names as keys and csv data for the repeat groups as values)
    .. code:: python
    
     scto.get_form_data(form_id, shape='long')

-  Get a long csv without repeat groups
    .. code:: python
    
     scto.get_form_data(form_id, shape='long', repeat_groups=false)

-  Get a wide csv with line breaks replaced with space with only pending-review submissions
    .. code:: python
    
     scto.get_form_data(form_id, line_breaks=' ', review_status=['pending'])

-  Get a wide json
    .. code:: python
    
     scto.get_form_data(form_id, format='json')

-  Get a wide json with forms completed after a given date (exclusive)
    .. code:: python
    
     date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
     scto.get_form_data(form_id, format='json', oldest_completion_date=date_input)

-  Get a wide json for encrypted form starting after a given CompletionDate
    .. code:: python
    
     key_data = open('<path to keyfile>', 'rb')
     scto.get_form_data(form_id, format='json', oldest_completion_date=my_datetime, key=key_data)

-  Get a server dataset with line breaks replaced with space
    .. code:: python
    
     scto.get_form_data(dataset_id, line_breaks=' ')

-  Get a media file attachment and save to file
     .. code:: python
    
      data = scto.get_attachment(url)
      f = open(file_name, 'wb')   
      f.write(data)   
      f.close()

-  Get form definition and save to excel file
     .. code:: python
    
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

License 
=======

`The MIT License (MIT)`_


SCTO API Options
================

`SCTO API Documentation`_


.. _The MIT License (MIT): https://github.com/IDinsight/surveycto-python/blob/master/LICENSE.md
.. _SCTO API Documentation: https://support.surveycto.com/hc/en-us/articles/360033156894?flash_digest=0a6eded7694409181788cc46a7026897850d65b5&flash_digest=d76dde7c3ffc40f4a7f0ebd87596d32f3a52304f