import requests
import urllib
import datetime


class IllegalArgumentError(ValueError):
    pass


class SurveyCTOObject(object):
    """

    """

    def __init__(self,
                 server_name,
                 username,
                 password,
                 keyfile=False):
        """
                Initialize SCTO Object
                :param server_name (str): SurveyCTO server name
                :param username (str): SurveyCTO login username
                :param password (str): SurveyCTO login password
                :param keyfile (str, optional)

        """

        self.server_name = server_name

        # Defining both to be compatible with all SCTO versions
        self.auth_basic = requests.auth.HTTPBasicAuth(username,
                                                      password)
        self.auth_disgest = requests.auth.HTTPDigestAuth(username,
                                                         password)

        self.keyfile = keyfile

        # Only header we are using -- Check if any more should be provided as options
        self.default_headers = {
            'X-OpenRosa-Version': '1.0',
        }



    def get_url_data(self,
                     url,
                     line_breaks=None):
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

        try:
            if self.keyfile is False:
                response = requests.get(
                    url, headers=self.default_headers, auth=self.auth_basic)
            else:
                files = {'private_key': open(self.keyfile, 'rb')}
                response = requests.post(
                    url, files=files, headers=self.default_headers, auth=self.auth_basic)

            response.raise_for_status()

        except Exception as e:
            try:
                if self.keyfile is False:
                    response = requests.get(
                        url, headers=self.default_headers, auth=self.auth_disgest)
                else:
                    files = {'private_key': open(self.keyfile, 'rb')}
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
                      review_status='approved',
                      repeat_groups=None,
                      line_breaks=None):
        """
                Fetch SurveyCTO form data in json or csv formats.
                :param form_id (str): The form_id of the SurveyCTO form.
                :param format (str, optional): The format of the returned data. Allowed values are: json, csv(default).
                :param shape (str, optional): The shape of the returned data. Allowed values are: wide, long. 
                	   shape=’long’ can only be specified when returning data in csv format.
                :param date (datetime.date or datetime.datetime object, optional): Return only the form submissions where 
                		CompletionDate is greater than the given date (in UTC). Can only be specified when returning data 
                		in json format.
                :param review_status (str, optional): Return only the form submissions with given review status. Allowed 
                		values are: approved(default), rejected, pending and more than one value concatenated with | or 
                		with commas.
                :param repeat_groups (bool, optional): Return a dictionary object containing the main form data along 
                		with the repeat groups. Can only be specified when returning long data, in which case it will 
                		default to true.
                :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
        """

        review_status_arr = review_status.replace('|', ',').split(',')

        for status in review_status_arr:
            if (review_status not in ['approved', 'pending', 'rejected']):
                raise IllegalArgumentError(
                    "Wrong value passed in review_status. Allowed values are approved, rejected and pending.")
            else:
                url_review_status = review_status

        if (format == 'csv'):

            # check params
            if (date is not None):
                raise IllegalArgumentError(
                    "Date can only be specified when extracting data in json format")

            if (shape not in ['long', 'wide']):
                raise IllegalArgumentError(
                    "Wrong value passed in shape. Allowed values are long and wide")

            if (shape == 'wide'):

                if (repeat_groups is not None):
                    raise IllegalArgumentError(
                        "Repeat groups can only be specified when extracting data in csv long format")

                url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/wide/csv/{form_id}?r={url_review_status}'
                data = (self.get_url_data(url, line_breaks)).text
                return data
            else:

                if (repeat_groups == False):

                    url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/csv/{form_id}?r={url_review_status}'
                    data = (self.get_url_data(url, line_breaks)).text
                    return data

                else:

                    # Default to returning all repeat groups in a distionary
                    files_url = f'https://{self.server_name}.surveycto.com/api/v1/forms/files/csv/{form_id}'
                    url_list = (self.get_url_data(files_url, line_breaks)).text
                    data_dict = {}
                    url_count = 0
                    for url in url_list.splitlines():
                        url = url + f'?r={url_review_status}'
                        data = (self.get_url_data(url, line_breaks)).text
                        data_dict[url_count] = data
                        url_count = url_count + 1

                    return data_dict

        else:

            if (shape != 'wide'):
                raise IllegalArgumentError(
                    "Shape can only be specified when extracting data in csv format")

            if (repeat_groups is not None):
                raise IllegalArgumentError(
                    "Repeat groups can only be specified when extracting data in csv long format")

            if (line_breaks is not None):
                raise IllegalArgumentError(
                    "Line breaks can only be specified when extracting data in csv format")

            if ((date == 0) or (date is None)):
                # Default to fecthing data for all dates
                url_date = 0
            else:
                if (isinstance(date, datetime.date) or isinstance(date, datetime.datetime)):

                    if (isinstance(date, datetime.date)):
                        # convert date to required format
                        date = datetime.datetime.combine(
                            date, datetime.datetime.min.time())

                    url_date = urllib.parse.quote(
                        date.strftime("%b %-d, %Y %-I:%M:%S %p"))

                else:
                    raise TypeError(
                        'Date arg must be a datetime.date or datetime.datetime object')

            url = f'https://{self.server_name}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={url_date}?r={url_review_status}'
            data = (self.get_url_data(url)).json()
            return data



    def get_repeatgroup(self,
                        form_id,
                        repeat_group_name,
                        review_status='approved'):
        """
                Fetch SurveyCTO form's repeatgroup data.
                :param form_id (str): The form_id of the SurveyCTO form.
                :param repeat_group_name (str): Form's repeat group name.
                :param review_status (str, optional): Return only the form submissions with given review status. 
                		Allowed values are: approved(default), rejected, pending and more than one value concatenated 
                		with | or with commas.
                :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
        """

        review_status_arr = review_status.replace('|', ',').split(',')

        for status in review_status_arr:
            if (review_status not in ['approved', 'pending', 'rejected']):
                raise IllegalArgumentError(
                    "Wrong value passed in review_status. Allowed values are approved, rejected and pending.")
            else:
                url_review_status = review_status

        url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/csv/{form_id}/{repeat_group_name}?r={url_review_status}'
        data = (self.get_url_data(url)).text
        return data



    def get_server_dataset(self,
                           dataset_id):
        """
                Fetch SurveyCTO server dataset data.
                :param dataset_id (str): The server dataset id of the SurveyCTO dataset.
                :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
        """

        url = f'https://{self.server_name}.surveycto.com/api/v2/datasets/data/csv/{dataset_id}'
        data = (self.get_url_data(url)).text
        return data



    def get_attachment(self,
                       url):
        """
                Fetch form's file attachments like media/audio/images from SurveyCTO
                :param url (str): The URL to fetch the attached file
        """

        data = (self.get_url_data(url)).content
        return data


