import configparser
import pysurveycto
    
def test1(scto):

    data = scto.get_form_data('phone_surveys_pilot_4')
    print(data)



def test2(scto):

    data = scto.get_form_data('phone_surveys_pilot_4', 
                              format='json')
    print(data)



def test3(scto):

    date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
    data = scto.get_form_data('phone_surveys_pilot_4', 
                              format='json', 
                              oldest_completion_date=date_input)
    print(data)



def test4(scto):

    data = scto.get_repeatgroup('d2d_survey_rapid', 
                                repeat_group_name='family_details')
    print(data)



def test5(scto):

    data = scto.get_server_dataset('D2D_CV')
    print(data)



if __name__ == '__main__':
    v_config = configparser.ConfigParser()
    v_config.read('./config.cfg')
    v_scto_config = v_config['surveycto-dod']
    #v_scto_config = v_config['surveycto-eg']
    
    scto = pysurveycto.SurveyCTOObject(v_scto_config['servername'], 
                                       v_scto_config['username'], 
                                       v_scto_config['password'])

    test1(scto)