import configparser
import datetime
import pysurveycto
import pandas as pd
import json
from io import StringIO

#exec(open("../pysurveycto/pysurveycto.py").read())

def convert_csv_to_df(csv_data):

    v_df = pd.read_csv(StringIO(csv_data))
    return v_df


def convert_json_to_df(json_data):

    v_df = pd.read_json(json.dumps(json_data))
    return v_df


def review_status_test_1(scto):
    """
    Expected: Type Error("'review_status' parameter is expected to be a list.")

    """

    data = scto.get_form_data("phone_surveys_pilot_4", review_status="approved")
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def review_status_test_2(scto):
    """
    Expected: IllegalArgumentError(
      "Wrong value passed in 'review_status'. Allowed values are 'approved', 'rejected' and 'pending'.")

    """

    data = scto.get_form_data(
        "phone_surveys_pilot_4", review_status=["approved", "WrongValue"]
    )
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def review_status_test_3(scto):
    """
    Expected: warnings.warn(
      "Review status can only be specified when returning data without a date filter. Returning data for 'approved' review status.")

    """

    date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
    data = scto.get_form_data(
        "phone_surveys_pilot_4",
        format="json",
        oldest_completion_date=date_input,
        review_status=["approved"],
    )
    data_df = convert_json_to_df(data)
    print(data_df.head(1))


def key_test_1(scto):
    """
    Expected: IllegalArgumentError(
      "Encrypted data extraction is only supported in returning data json format without review status filter.")

    """

    data = scto.get_form_data("phone_surveys_pilot_4", key="dfghj")
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def date_test_1(scto):
    """
    Expected: warnings.warn(
      "'oldest_completion_date' can only be specified when returning data in json format. Returning data for all dates.")

    """

    date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
    data = scto.get_form_data(
        "phone_surveys_pilot_4", oldest_completion_date=date_input
    )
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def date_test_2(scto):
    """
    Expected: raise TypeError(
      "'oldest_completion_date' argument is expected to be a datetime.date or datetime.datetime object")
    """

    data = scto.get_form_data(
        "phone_surveys_pilot_4", format="json", oldest_completion_date="2020-03-31"
    )
    data_df = convert_json_to_df(data)
    print(data_df.head(1))


def shape_test_1(scto):
    """
    Expected: IllegalArgumentError(
      "Wrong value passed in 'shape'. Allowed values are 'long' and 'wide'.")
    """

    data = scto.get_form_data("phone_surveys_pilot_4", shape="wde")
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def shape_test_2(scto):
    """
    Expected: warnings.warn(
      "Shape can only be specified when returning data in csv format. Returning data in 'wide' format.")

    """

    data = scto.get_form_data("phone_surveys_pilot_4", format="json", shape="long")
    data_df = convert_json_to_df(data)
    print(data_df.head(1))


def repeat_groups_test_1(scto):
    """
    Expected: warnings.warn(
      "Repeat groups can only be specified when returning data in csv long format. Returning data for all repeat groups.")
    """

    data = scto.get_form_data(
        "phone_surveys_pilot_4", format="json", repeat_groups=False
    )
    data_df = convert_json_to_df(data)
    print(data_df.head(1))


def repeat_groups_test_2(scto):
    """
    Expected: IllegalArgumentError(
        "Wrong repeat group name passed in arguments. Available repeat groups are: " + ', '.join(repeat_groups_dict.keys()))

    """

    data = scto.get_repeatgroup("phone_surveys_pilot_4", repeat_group_name="Testing")
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def line_breaks_test_1(scto):
    """
    Expected: warnings.warn(
              "Line breaks can only be specified when returning data in csv format.")
    """

    data = scto.get_form_data("phone_surveys_pilot_4", format="json", line_breaks=" ")
    data_df = convert_json_to_df(data)
    print(data_df.head(1))


def wrong_form_id_qdef(scto):
    """
    requests.exceptions.HTTPError: 500 Server Error

    """

    data = scto.get_questionnaire_definition("phone_surveys_pilo_4")
    print(data.keys())


if __name__ == "__main__":
    v_config = configparser.ConfigParser()
    v_config.read("./config.cfg")
    v_scto_config = v_config["surveycto-dod"]

    scto = pysurveycto.SurveyCTOObject(
        v_scto_config["servername"],
        v_scto_config["username"],
        v_scto_config["password"],
    )

    # review_status_test_1(scto)
    # review_status_test_2(scto)
    # review_status_test_3(scto)
    # key_test_1(scto)
    # date_test_1(scto)
    # date_test_2(scto)
    # shape_test_1(scto)
    # shape_test_2(scto)
    # repeat_groups_test_1(scto)
    # repeat_groups_test_2(scto)
    # line_breaks_test_1(scto)
    # wrong_form_id_qdef(scto)
