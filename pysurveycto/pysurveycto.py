"""
This library allows downloading survey data collected on SurveyCTO data collection app using SurveyCTO REST API.

For more information on this library, see the README on GitHub:
    https://github.com/IDinsight/surveycto-python/blob/master/README.md

For more information on the SurveyCTO REST API, see:
    https://support.surveycto.com/hc/en-us/articles/360033156894?flash_digest=fd857681db6696b02b2de090c51ceb4e14ea65e1

"""

import requests
import datetime
import warnings
from urllib.parse import quote


class IllegalArgumentError(ValueError):
    """
    Class created to handle invalid parameter errors
    """

    pass


class NotImplementedError(ValueError):
    """
    Class created to handle requests that are not yet implemented
    """

    pass


class SurveyCTOObject(object):
    """
    Object to initialize and interact with a SurveyCTO server
    """

    def __init__(self, server_name, username, password):
        """
        Initialize SCTO Object
        :param server_name (str): SurveyCTO server name
        :param username (str): SurveyCTO login username
        :param password (str): SurveyCTO login password

        """

        self.server_name = server_name

        # Defining both to be compatible with all SurveyCTO versions
        self.auth_basic = requests.auth.HTTPBasicAuth(username, password)
        self.auth_digest = requests.auth.HTTPDigestAuth(username, password)
        self.default_headers = {
            "X-OpenRosa-Version": "1.0",
        }

        if not hasattr(type(self), "_sesh"):
            self.__session_make()

    def __print_user_response(self, err):
        """
        Private function to print specific responses based on the HTTP response code

        """

        if err.response.status_code == 417:
            v_error_json = err.response.json()
            print(f"""Error message: {v_error_json["error"]["message"]}""")

    @classmethod
    def __session_make(cls):
        """
        Create a session if it does not exist. Allows for session sharing
        Requests automatically refreshes session if connection closes

        """
        cls._sesh = requests.session()

    def __auth(self):
        """
        Establish CSRF token and login

        """

        url = f"https://{self.server_name}.surveycto.com"

        try:
            response = self._sesh.head(url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise e

        headers = {"X-csrf-token": response.headers["X-csrf-token"]}

        auth = self._sesh.post(
            url + "/login",
            cookies=self._sesh.cookies,
            headers=headers,
            auth=self.auth_basic,
        )
        headers["X-csrf-token"] = auth.headers["X-csrf-token"]

        return headers

    def get_url_data(self, url, line_breaks=None, key=False):
        """
        Function to fetch data directly from a SurveyCTO url
        :param url: SurveyCTO URL
        :line_breaks: Replace default linebreaks ('\n') in the csv data with this character
        :key: The private key to decrypt form data
        """

        # Change line break settings as per user parameter
        if line_breaks is not None:
            v_url_encoded_line_break = quote(line_breaks)
            v_settings = f"""https://{self.server_name}.surveycto.com/api/v1/forms/settings/csv/linebreak?v={v_url_encoded_line_break}"""

            try:
                response = requests.post(
                    v_settings, headers=self.default_headers, auth=self.auth_basic
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                try:
                    response = requests.post(
                        v_settings, headers=self.default_headers, auth=self.auth_digest
                    )
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    response = False
                    raise e
        else:
            # restore default
            v_settings = f"""https://{self.server_name}.surveycto.com/api/v1/forms/settings/csv/linebreak"""

            try:
                response = requests.delete(
                    v_settings, headers=self.default_headers, auth=self.auth_basic
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                try:
                    response = requests.delete(
                        v_settings, headers=self.default_headers, auth=self.auth_digest
                    )
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    response = False
                    raise e

        # Extract using basic authentication as per SurveyCTO 2.70 update
        try:
            if key is False:
                response = requests.get(
                    url, headers=self.default_headers, auth=self.auth_basic
                )
            else:
                files = {"private_key": key}
                response = requests.post(
                    url, files=files, headers=self.default_headers, auth=self.auth_basic
                )

            response.raise_for_status()

        # except Exception as e:
        except requests.exceptions.HTTPError as e:

            if e.response.status_code == 401:
                # Try digest authentication which works for old SurveyCTO versions
                try:
                    if key is False:
                        response = requests.get(
                            url, headers=self.default_headers, auth=self.auth_digest
                        )
                    else:
                        files = {"private_key": key}
                        response = requests.post(
                            url,
                            files=files,
                            headers=self.default_headers,
                            auth=self.auth_digest,
                        )

                    response.raise_for_status()

                except requests.exceptions.HTTPError as e:

                    response = False
                    self.__print_user_response(e)
                    raise e

            else:
                response = False
                self.__print_user_response(e)
                # raise SystemExit(e)
                raise e

        return response

    def __check_review_status_and_raise(self, review_status):
        """
        Private function to check the review status param and raise error

        """

        # review_status is of list type
        if not isinstance(review_status, list):
            raise TypeError("'review_status' parameter is expected to be a list.")

        for status in review_status:
            # review_status allowed values are approved(default), rejected, pending
            if status not in ["approved", "pending", "rejected"]:
                raise IllegalArgumentError(
                    "Wrong value passed in 'review_status'. Allowed values are 'approved', 'rejected' and 'pending'."
                )

    def __check_review_status_with_date_and_raise(self, review_status):
        """
        Private function to check if review status is specified with date filter and raise warning

        """
        if review_status is not None:
            warnings.warn(
                "Review status can only be specified when returning data without a date filter. Returning data for 'approved' review status."
            )

    def __check_key_and_raise(self, key):
        """
        Private function to check key parameter and raise error

        """
        if key is not False:
            raise IllegalArgumentError(
                "Encrypted data extraction is only supported when returning data in json format without review status filter."
            )

    def __check_date_and_raise(self, oldest_completion_date, format):
        """
        Private function to check date parameter and raise warning/error

        """
        if (format == "csv") & (oldest_completion_date is not None):
            warnings.warn(
                "'oldest_completion_date' can only be specified when returning data in json format. Returning data for all dates."
            )
        elif format == "json":
            if not (
                isinstance(oldest_completion_date, datetime.date)
                or isinstance(oldest_completion_date, datetime.datetime)
            ):
                # Check params - oldest_completion_date is of datetime.date or datetime.datetime object type
                raise TypeError(
                    "'oldest_completion_date' argument is expected to be a datetime.date or datetime.datetime object"
                )

    def __get_url_date(self, oldest_completion_date):
        """
        Private function to return date for in required url format

        """
        # Note a datetime.datetime is also a datetime.date but a datetime.date is not a datetime.datetime
        if not isinstance(oldest_completion_date, datetime.datetime):
            # convert oldest_completion_date to required format
            oldest_completion_date = datetime.datetime.combine(
                oldest_completion_date, datetime.datetime.min.time()
            )

        url_date = quote(oldest_completion_date.strftime("%b %-d, %Y %-I:%M:%S %p"))

        return url_date

    def __check_shape_and_raise(self, format, shape):
        """
        Private function to check the shape parameter and raise warning/error

        """

        # Shape allowed values are 'wide' and 'long'
        if shape not in ["long", "wide"]:
            raise IllegalArgumentError(
                "Wrong value passed in 'shape'. Allowed values are 'long' and 'wide'."
            )

        # Check params - shape not allowed in json format
        if (format == "json") & (shape != "wide"):
            warnings.warn(
                "Shape can only be specified when returning data in csv format. Returning data in 'wide' format."
            )

    def __check_repeat_groups_and_raise(self, repeat_groups, shape):
        """
        Private function to check the repeat groups parameter and raise warning

        """

        if shape == "wide":
            # repeat_groups not alowed in wide csv format
            if repeat_groups is not None:
                warnings.warn(
                    "Repeat groups can only be specified when returning data in csv long format. Returning data for all repeat groups."
                )

    def __check_line_breaks_and_raise(self, line_breaks):
        """
        Private function to check the line break parameter and raise warning

        """

        # line_breaks not allowed in json format
        if line_breaks is not None:
            warnings.warn(
                "Line breaks can only be specified when returning data in csv format."
            )

    def __check_csv_extraction_params(
        self, shape, oldest_completion_date, review_status, repeat_groups, key
    ):
        """
        Check parameters passed for csv extraction

        """

        # Shape allowed values are 'wide' and 'long'
        self.__check_shape_and_raise("csv", shape)

        # oldest_completion_date not allowed in csv format
        self.__check_date_and_raise(oldest_completion_date, "csv")

        # review_status should be a list of allowed values
        self.__check_review_status_and_raise(review_status)

        # repeat_groups not alowed in wide csv format
        self.__check_repeat_groups_and_raise(repeat_groups, shape)

        # key not allowed in csv format
        self.__check_key_and_raise(key)

    def __check_json_extraction_params(
        self, shape, oldest_completion_date, review_status, repeat_groups, line_breaks, key
    ):
        """
        Check parameters passed for json extraction

        """

        # Check params - shape not allowed in json format
        self.__check_shape_and_raise("json", shape)
        shape = "wide"

        # Check params - repeat_groups not allowed in json format
        self.__check_repeat_groups_and_raise(repeat_groups, shape)

        # Check params - line_breaks not allowed in json format
        self.__check_line_breaks_and_raise(line_breaks)

        if (oldest_completion_date == 0) or (oldest_completion_date is None):
            if review_status is not None:

                # Check params - review status
                self.__check_review_status_and_raise(review_status)

                # Check params - key not allowed in json formats with review status
                self.__check_key_and_raise(key)

        else:
            # Check params - review_status not allowed in json formats with date filter
            self.__check_review_status_with_date_and_raise(review_status)

            # Check params - oldest_completion_date
            self.__check_date_and_raise(oldest_completion_date, "json")

    def __get_repeat_groups(self, form_id):
        """
        Private function to get the dictionary with repeat group {name: url} pairs

        """

        files_url = f"""https://{self.server_name}.surveycto.com/api/v1/forms/files/csv/{form_id}"""
        url_list = (self.get_url_data(files_url, None, key=False)).text
        repeat_groups_dict = {}
        for url_count, url in enumerate(url_list.splitlines()):
            if url_count == 0:
                base_url = url
                repeat_group_name = "Main"
            else:
                repeat_group_name = url.replace(base_url + "/", "")

            repeat_groups_dict[repeat_group_name] = url

        return repeat_groups_dict

    def __get_form_data_in_csv_format(
        self,
        form_id,
        shape,
        oldest_completion_date,
        review_status,
        repeat_groups,
        line_breaks,
        key,
    ):
        """
        Private function to extract form data in csv format

        """
        url_review_status = ",".join(review_status)

        # oldest_completion_date not allowed in csv format
        oldest_completion_date = None

        if shape == "wide":

            # repeat_groups not alowed in wide csv format
            repeat_groups = None

            url = f"""https://{self.server_name}.surveycto.com/api/v1/forms/data/{shape}/csv/{form_id}?r={url_review_status}"""
            data = (self.get_url_data(url, line_breaks, key=key)).text
            return data

        else:

            if repeat_groups == False:

                url = f"""https://{self.server_name}.surveycto.com/api/v1/forms/data/csv/{form_id}?r={url_review_status}"""
                data = (self.get_url_data(url, line_breaks, key=key)).text
                return data

            else:

                # Default to returning all repeat groups in a dictionary
                repeat_groups_dict = self.__get_repeat_groups(form_id)

                data_dict = {}
                for dict_key, dict_value in repeat_groups_dict.items():

                    url = dict_value + "?r=" + url_review_status
                    data = (self.get_url_data(url, line_breaks, key=key)).text
                    data_dict[dict_key] = data

                return data_dict

    def __get_form_data_in_json_format(
        self,
        form_id,
        shape,
        oldest_completion_date,
        review_status,
        repeat_groups,
        line_breaks,
        key,
    ):
        """
        Private function to extract form data in json formats

        """
        # shape is 'wide' in json format always
        shape = "wide"

        # repeat_groups and line_breaks not allowed in json format
        repeat_groups = None
        line_breaks = None

        if (oldest_completion_date == 0) or (oldest_completion_date is None):
            # Default to fetching data for all dates
            url_date = 0

            # check params
            if review_status is not None:

                url_review_status = ",".join(review_status)

                # If review status is specified, use V1 API with review status
                url = f"""https://{self.server_name}.surveycto.com/api/v1/forms/data/{shape}/json/{form_id}?r={url_review_status}"""

            else:
                # If no review status specified, use V2 API with oldest_completion_date param
                url = f"""https://{self.server_name}.surveycto.com/api/v2/forms/data/{shape}/json/{form_id}?date={url_date}"""

        else:

            # review_status not allowed in json formats with date filter
            review_status = None

            url_date = self.__get_url_date(oldest_completion_date)

            url = f"""https://{self.server_name}.surveycto.com/api/v2/forms/data/{shape}/json/{form_id}?date={url_date}"""

        data = (self.get_url_data(url, key=key)).json()
        return data

    def get_form_data(
        self,
        form_id,
        format="csv",
        shape="wide",
        oldest_completion_date=None,
        review_status=None,
        repeat_groups=None,
        line_breaks=None,
        key=False,
    ):
        """
        Fetch SurveyCTO form data in json or csv formats.
        :param form_id (str): The form_id of the SurveyCTO form.
        :param format (str, optional): The format of the returned data. Allowed values are: json, csv(default).
        :param shape (str, optional): The shape of the returned data. Allowed values are: wide(default), long.
               shape=’long’ can only be specified when returning data in csv format.
        :param oldest_completion_date (datetime.date or datetime.datetime object, optional): Return only the form submissions where
                    CompletionDate is greater than the given date (in UTC). Can only be specified when returning data
                    in json format.
        :param review_status (list, optional): Return only the form submissions with given review status. Allowed
                    values in the list are: approved(default), rejected, pending. This option is only applicable for
                    forms using the “Review and Corrections” workflow on the SurveyCTO web console.
        :param repeat_groups (bool, optional): Return a dictionary object containing the main form data along
                    with the repeat groups. Can only be specified when returning long data, in which case it will
                    default to true.
        :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
        :param key(str, optional): The private key to decrypt form data in binary/string format. This can only be
                specified when returning data in json format without review_status parameter.
        """

        if format == "csv":

            if review_status is None:
                review_status = ["approved"]

            # Check params
            self.__check_csv_extraction_params(
                shape, oldest_completion_date, review_status, repeat_groups, key
            )

            data = self.__get_form_data_in_csv_format(
                form_id,
                shape,
                oldest_completion_date,
                review_status,
                repeat_groups,
                line_breaks,
                key,
            )
            return data

        elif format == "json":

            # Check params
            self.__check_json_extraction_params(
                shape, oldest_completion_date, review_status, repeat_groups, line_breaks, key
            )

            data = self.__get_form_data_in_json_format(
                form_id,
                shape,
                oldest_completion_date,
                review_status,
                repeat_groups,
                line_breaks,
                key,
            )
            return data

        else:

            raise NotImplementedError(
                "Support for downloading data in '"
                + format
                + "' format is currently not available. Allowed values are: 'json' and 'csv'."
            )

    def get_repeatgroup(
        self, form_id, repeat_group_name, review_status=None, line_breaks=None
    ):
        """
        Fetch SurveyCTO form's repeatgroup data.
        :param form_id (str): The form_id of the SurveyCTO form.
        :param repeat_group_name (str): Form's repeat group name.
        :param review_status (list, optional):Return only the form submissions with given review status. Allowed
                values in the list are: approved(default), rejected, pending. This option is only applicable for
                forms using the “Review and Corrections” workflow on the SurveyCTO web console.
        :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
        """

        if review_status is None:
            review_status = ["approved"]

        # Check params - review_status
        self.__check_review_status_and_raise(review_status)
        url_review_status = ",".join(review_status)

        repeat_groups_dict = self.__get_repeat_groups(form_id)
        del repeat_groups_dict["Main"]

        if len(repeat_groups_dict.keys()) == 0:
            raise IllegalArgumentError(
                "No repeat groups found in the specified SurveyCTO form."
            )

        if repeat_group_name not in repeat_groups_dict.keys():
            raise IllegalArgumentError(
                "Wrong repeat group name passed in arguments. Available repeat groups are: "
                + ", ".join(repeat_groups_dict.keys())
            )

        url = f"""https://{self.server_name}.surveycto.com/api/v1/forms/data/csv/{form_id}/{repeat_group_name}?r={url_review_status}"""

        data = (self.get_url_data(url, line_breaks)).text

        return data

    def get_server_dataset(self, dataset_id, line_breaks=None):
        """
        Fetch SurveyCTO server dataset data.
        :param dataset_id (str): The server dataset id of the SurveyCTO dataset.
        :param line_breaks (str, optional): Replace linebreaks in the csv data with some other character.
        """

        url = f"""https://{self.server_name}.surveycto.com/api/v2/datasets/data/csv/{dataset_id}"""

        data = (self.get_url_data(url, line_breaks)).text

        return data

    def get_attachment(self, url, key=False):
        """
        Fetch form's file attachments like media/audio/images from SurveyCTO
        :param url (str): The URL to fetch the attached file
        :param key(str, optional): The private key to decrypt form data in binary/string format.
        """

        data = (self.get_url_data(url, key=key)).content

        return data

    def get_form_definition(self, form_id):

        """
        Fetch form definition from SurveyCTO
        :param form_id (str): The form_id of the SurveyCTO form.

        """

        headers = self.__auth()
        url = f"https://{self.server_name}.surveycto.com/forms/{form_id}/design"

        try:
            response = self._sesh.get(
                url,
                cookies=self._sesh.cookies,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            response = False
            raise e

        return response.json()
