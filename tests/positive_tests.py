import configparser
import datetime
import pysurveycto
import pandas as pd
import json
from io import StringIO

#exec(open('../pysurveycto/pysurveycto.py').read())

def convert_csv_to_df(csv_data):

    v_df = pd.read_csv(StringIO(csv_data))
    return v_df


def convert_json_to_df(json_data):

    v_df = pd.read_json(json.dumps(json_data))
    return v_df



def test1(scto):

    data = scto.get_form_data('phone_surveys_pilot_4')
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))



def test2(scto):

    data = scto.get_form_data('phone_surveys_pilot_4', 
                              format='json')
    data_df = convert_json_to_df(data)
    print(data_df.head(1))



def test3(scto):

    date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
    data = scto.get_form_data('phone_surveys_pilot_4', 
                              format='json', 
                              oldest_completion_date=date_input)
    data_df = convert_json_to_df(data)
    print(data_df.head(1))



def test4(scto):

    data = scto.get_repeatgroup('d2d_survey_rapid', 
                                repeat_group_name='family_details')
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))



def test5(scto):

    data = scto.get_server_dataset('test_dataset')
    data_df = convert_csv_to_df(data)
    print(data_df.head(1))



if __name__ == '__main__':
    v_config = configparser.ConfigParser()
    v_config.read('./config.cfg')
    #v_scto_config = v_config['surveycto-dod']
    v_scto_config = v_config['surveycto-eg']
    
    scto = pysurveycto.SurveyCTOObject(v_scto_config['servername'], 
                                       v_scto_config['username'], 
                                       v_scto_config['password'])

    test1(scto)