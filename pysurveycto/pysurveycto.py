import requests
import urllib
import datetime


class IllegalArgumentError(ValueError):
    pass


class SurveyCTOObject(object):
    """
        Object to initialize and interact with a SurveyCTO server
    """

    def __init__(self,
                 server_name,
                 username,
                 password):
        """
            Initialize SCTO Object
            :param server_name (str): SurveyCTO server name
            :param username (str): SurveyCTO login username
            :param password (str): SurveyCTO login password

        """

        self.server_name = server_name

        # Defining both to be compatible with all SCTO versions
        self.auth_basic = requests.auth.HTTPBasicAuth(username,
                                                      password)
        self.auth_disgest = requests.auth.HTTPDigestAuth(username,
                                                         password)

        # Only header we are using -- Check if any more should be provided as options
        self.default_headers = {
            'X-OpenRosa-Version': '1.0',
        }



    def get_url_data(self,
                     url,
                     line_breaks=None,
                     keyfile=False):
        """
            Function to fetch data directly from a scto url
            :param url: SurveyCTO URL
        """

        # Change line break settings as per user parameter
        if (line_breaks is not None):
            v_url_encoded_line_break = urllib.parse.quote(line_breaks)
            v_settings = f'''https://{self.server_name}.surveycto.com/api/v1/forms/settings/csv/linebreak?v={v_url_encoded_line_break}'''
            try:
                response = requests.post(
                    v_settings, headers=self.default_headers, auth=self.auth_basic)
                response.raise_for_status()
            except Exception as e:
                try:
                    response = requests.post(
                        v_settings, headers=self.default_headers, auth=self.auth_disgest)
                    response.raise_for_status()
                except Exception as e:
                    response = False
                    raise ValueError(e)
        else:
            # restore default
            v_settings = f'https://{self.server_name}.surveycto.com/api/v1/forms/settings/csv/linebreak'

            try:
                response = requests.delete(
                    v_settings, headers=self.default_headers, auth=self.auth_basic)
                response.raise_for_status()
            except Exception as e:
                try:
                    response = requests.delete(
                        v_settings, headers=self.default_headers, auth=self.auth_disgest)
                    response.raise_for_status()
                except Exception as e:
                    response = False
                    raise ValueError(e)

        # Extract using basic authentication as per SurveyCTO 2.70 update
        try:
            if keyfile is False:
                response = requests.get(
                    url, headers=self.default_headers, auth=self.auth_basic)
            else:
                files = {'private_key': open(keyfile, 'rb')}
                response = requests.post(
                    url, files=files, headers=self.default_headers, auth=self.auth_basic)

            response.raise_for_status()

        except Exception as e:
            # Try digest authentication which works for old SurveyCTO versions
            try:
                if keyfile is False:
                    response = requests.get(
                        url, headers=self.default_headers, auth=self.auth_disgest)
                else:
                    files = {'private_key': open(keyfile, 'rb')}
                    response = requests.post(
                        url, files=files, headers=self.default_headers, auth=self.auth_disgest)

                response.raise_for_status()

            except Exception as e:
                response = False
                raise ValueError(e)

        return response



    def get_form_data(self,
                      form_id,
                      format='csv',
                      shape='wide',
                      date=None,
                      review_status=None,
                      repeat_groups=None,
                      line_breaks=None,
                      keyfile=False):
        """
            Fetch SurveyCTO form data in json or csv formats.
            :param form_id (str): The form_id of the SurveyCTO form.
            :param format (str, optional): The format of the returned data. Allowed values are: json, csv(default).
            :param shape (str, optional): The shape of the returned data. Allowed values are: wide(default), long. 
            	   shape=’long’ can only be specified when returning data in csv format.
            :param date (datetime.date or datetime.datetime object, optional): Return only the form submissions where 
            		CompletionDate is greater than the given date (in UTC). Can only be specified when returning data 
            		in json format.
            :param review_status (list, optional): Return only the form submissions with given review status. Allowed 
            		values in the list are: approved(default), rejected, pending. This option is only applicable for 
                    forms using the “Review and Corrections” workflow on the SurveyCTO web console.
            :param repeat_groups (bool, optional): Return a dictionary object containing the main form data along 
            		with the repeat groups. Can only be specified when returning long data, in which case it will 
            		default to true.
            :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
            :param keyfile(str, optional): The private key to decrypt form data. This can only be specified when returning
                    data in json format without review_status parameter.
        """

        if (format == 'csv'):

            if review_status is None:
                review_status = ['approved']
            #review_status_arr = review_status.replace('|', ',').split(',')

            # Check params - review status is of list type
            if not isinstance(review_status, list):
                raise TypeError(
                        "review_status parameter is expected to be a list.")

            url_review_status = ""
            url_review_count = 0
            for status in review_status:
                # Check params - review_status allowed values are approved(default), rejected, pending
                if (status not in ['approved', 'pending', 'rejected']):
                    raise IllegalArgumentError(
                        "Wrong value passed in review_status. Allowed values are approved, rejected and pending.")
                else:
                    if (url_review_count == 0):
                        url_review_status = url_review_status + status
                    else:
                        url_review_status = url_review_status + "," + status
                    url_review_count+=1

            # Check params - date not allowed in csv formats
            if (date is not None):
                raise IllegalArgumentError(
                    "Date can only be specified when returning data in json format.")

            # Check params - keyfile not allowed in csv formats
            if keyfile is not False:
                raise IllegalArgumentError(
                    "Encrypted data extraction is only supported when returning data in json format.")

            # Check params - shape allowed values are wide(default) and long 
            if (shape not in ['long', 'wide']):
                raise IllegalArgumentError(
                    "Wrong value passed in shape. Allowed values are long and wide.")

            if (shape == 'wide'):

                # Check params - repeat_groups not alowed in wide csv format
                if (repeat_groups is not None):
                    raise IllegalArgumentError(
                        "Repeat groups can only be specified when returning data in csv long format.")

                url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/wide/csv/{form_id}?r={url_review_status}'
                data = (self.get_url_data(url, line_breaks, keyfile=keyfile)).text
                return data

            else:

                if (repeat_groups == False):

                    url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/csv/{form_id}?r={url_review_status}'
                    data = (self.get_url_data(url, line_breaks, keyfile=keyfile)).text
                    return data

                else:

                    # Default to returning all repeat groups in a dictionary
                    files_url = f'https://{self.server_name}.surveycto.com/api/v1/forms/files/csv/{form_id}'
                    url_list = (self.get_url_data(files_url, line_breaks, keyfile=keyfile)).text
                    data_dict = {}
                    url_count = 0
                    for url in url_list.splitlines():
                        url = url + f'?r={url_review_status}'
                        data = (self.get_url_data(url, line_breaks, keyfile=keyfile)).text
                        data_dict[url_count] = data
                        url_count = url_count + 1

                    return data_dict

        else:

            # Check params - shape not allowed in json format
            if (shape != 'wide'):
                raise IllegalArgumentError(
                    "Shape can only be specified when returning data in csv format.")

            # Check params - repeat_groups not allowed in json format
            if (repeat_groups is not None):
                raise IllegalArgumentError(
                    "Repeat groups can only be specified when returning data in csv format.")

            # Check params - line_breaks not allowed in json format
            if (line_breaks is not None):
                raise IllegalArgumentError(
                    "Line breaks can only be specified when returning data in csv format.")

            if ((date == 0) or (date is None)):
                # Default to fecthing data for all dates
                url_date = 0

                # check params
                if review_status is not None:
                    #review_status_arr = review_status.replace('|', ',').split(',')

                    # Check params - review status is of list type
                    if not isinstance(review_status, list):
                        raise TypeError(
                                "review_status parameter is expected to be a list.")

                    # Check params - keyfile not allowed in json formats with review status
                    if keyfile is not False:
                        raise IllegalArgumentError(
                            "Encrypted data extraction is only supported in returning data json format without review status filter.")

                    url_review_status = ""
                    url_review_count = 0
                    for status in review_status:
                        if (status not in ['approved', 'pending', 'rejected']):
                            # Check params - review_status allowed values are approved(default), rejected, pending
                            raise IllegalArgumentError(
                                "Wrong value passed in review_status. Allowed values are approved, rejected and pending.")
                        else:
                            if (url_review_count == 0):
                                url_review_status = url_review_status + status
                            else:
                                url_review_status = url_review_status + "," + status
                            url_review_count+=1

                    # If review status is specified, use V1 API with review status
                    url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/wide/json/{form_id}?r={url_review_status}'

                else:
                    # If no review status specified, use V2 API with date param
                    url = f'https://{self.server_name}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={url_date}'

            else:

                # Check params - review_status not allowed in json formats with date filter
                if review_status is not None:
                    raise IllegalArgumentError(
                                "Review status can only be specified when returning data without a date filter.")

                if (isinstance(date, datetime.date) or isinstance(date, datetime.datetime)):

                    if (isinstance(date, datetime.date)):
                        # convert date to required format
                        date = datetime.datetime.combine(
                            date, datetime.datetime.min.time())

                    url_date = urllib.parse.quote(
                        date.strftime("%b %-d, %Y %-I:%M:%S %p"))

                else:
                     # Check params - date is of datetime.date or datetime.datetime object type
                    raise TypeError(
                        'Date argument is expected to be a datetime.date or datetime.datetime object')

                url = f'https://{self.server_name}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={url_date}'

            data = (self.get_url_data(url, keyfile=keyfile)).json()
            return data



    def get_repeatgroup(self,
                        form_id,
                        repeat_group_name,
                        review_status=None,
                        line_breaks=None):
        """
            Fetch SurveyCTO form's repeatgroup data.
            :param form_id (str): The form_id of the SurveyCTO form.
            :param repeat_group_name (str): Form's repeat group name.
            :param review_status (list, optional):Return only the form submissions with given review status. Allowed 
                    values in the list are: approved(default), rejected, pending. This option is only applicable for 
                    forms using the “Review and Corrections” workflow on the SurveyCTO web console.
            :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
        """

        if not isinstance(review_status, list):
            raise TypeError(
                    "review_status parameter is expected to be a list.")

        url_review_status = ""
        url_review_count = 0
        for status in review_status:
            # Check params - review_status allowed values are approved(default), rejected, pending
            if (status not in ['approved', 'pending', 'rejected']):
                raise IllegalArgumentError(
                    "Wrong value passed in review_status. Allowed values are approved, rejected and pending.")
            else:
                if (url_review_count == 0):
                    url_review_status = url_review_status + status
                else:
                    url_review_status = url_review_status + "," + status
                url_review_count+=1

        url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/csv/{form_id}/{repeat_group_name}?r={url_review_status}'
        data = (self.get_url_data(url, line_breaks)).text
        return data



    def get_server_dataset(self,
                           dataset_id,
                           line_breaks=None):
        """
            Fetch SurveyCTO server dataset data.
            :param dataset_id (str): The server dataset id of the SurveyCTO dataset.
            :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
        """

        url = f'https://{self.server_name}.surveycto.com/api/v2/datasets/data/csv/{dataset_id}'
        data = (self.get_url_data(url, line_breaks)).text
        return data



    def get_attachment(self,
                       url):
        """
                Fetch form's file attachments like media/audio/images from SurveyCTO
                :param url (str): The URL to fetch the attached file
        """

        data = (self.get_url_data(url)).content
        return data

