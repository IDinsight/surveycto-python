exec(open('../pysurveycto/pysurveycto.py').read())

import configparser
    
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
                              date=date_input)
    print(data)



def test4(scto):

    data = scto.get_repeatgroup('D2D_CV', 
                                repeat_group_name='Household')
    print(data)



def test4(scto):

    data = scto.get_server_dataset('D2D_CV')
    print(data)



if __name__ == '__main__':
    v_config = configparser.ConfigParser()
    v_config.read('./config.cfg')
    v_scto_config = v_config['surveycto']

    scto = SurveyCTOObject(v_scto_config['servername'], 
                           v_scto_config['username'], 
                           v_scto_config['password'])

    test1(scto)