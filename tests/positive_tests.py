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


def test1(scto):

    data = scto.get_form_data("phone_surveys_pilot_4")
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def test2(scto):

    data = scto.get_form_data("phone_surveys_pilot_4", format="json")
    data_df = convert_json_to_df(data)
    print(data_df.head(1))


def test3(scto):

    date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
    data = scto.get_form_data(
        "phone_surveys_pilot_4", format="json", oldest_completion_date=date_input
    )
    data_df = convert_json_to_df(data)
    print(data_df.head(1))


def test4(scto):

    data = scto.get_repeatgroup("d2d_survey_rapid", repeat_group_name="family_details")
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def test5(scto):

    data = scto.get_server_dataset("test_dataset")
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))


def test6(scto):

    data = scto.get_form_data("d2d_survey_rapid", shape="long")
    print(data.keys())


def test7(scto):

    url = "https://dod.surveycto.com/view/submission-attachment/AA_586934af-a194-4567-b059-2504deb19055_hh_reached.m4a?blobKey=1419845"
    data = scto.get_attachment(url)
    f = open("test.mp4", "wb")
    f.write(data)
    f.close()


def test8(scto):

    key_data = open(
        "/Users/jeenuthomas/Documents/IDinsight/Projects/DOD/Docs/Uganda_UCT_PRIVATEDONOTSHARE.pem",
        "rb",
    )
    data = scto.get_form_data("gd_uct_endline", format="json", key=key_data)
    data_df = convert_json_to_df(data)
    print(data_df.columns)


def test9(scto):

    data = scto.get_form_definition("phone_surveys_pilot_4")
    print(data.keys())
    create_form_def_file(data)


def create_form_def_file(json_data):

    questions_df = pd.DataFrame(
        json_data["fieldsRowsAndColumns"][1:],
        columns=json_data["fieldsRowsAndColumns"][0],
    )
    choices_df = pd.DataFrame(
        json_data["choicesRowsAndColumns"][1:],
        columns=json_data["choicesRowsAndColumns"][0],
    )
    settings_df = pd.DataFrame(
        json_data["settingsRowsAndColumns"][1:],
        columns=json_data["settingsRowsAndColumns"][0],
    )

    writer = pd.ExcelWriter("form_def.xlsx", engine="openpyxl")
    questions_df.to_excel(writer, sheet_name="survey", index=False)
    choices_df.to_excel(writer, sheet_name="choices", index=False)
    settings_df.to_excel(writer, sheet_name="settings", index=False)
    writer.save()


if __name__ == "__main__":
    v_config = configparser.ConfigParser()
    v_config.read("./config.cfg")
    v_scto_config = v_config["surveycto-dod"]

    scto = pysurveycto.SurveyCTOObject(
        v_scto_config["servername"],
        v_scto_config["username"],
        v_scto_config["password"],
    )

    test9(scto)
