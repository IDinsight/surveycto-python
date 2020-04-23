import requests

class SurveyCTOObject(object):
    """

    """

    def __init__(self,
    			 server_name,
    			 username,
    			 password,
    			 keyfile=False):

    """
    Function to form the basic url

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



	def get_data_from_url(self,
						  url):

		"""
			Function to fetch data directly from a scto url
	        :param url: SurveyCTO URL
		"""
		try:
			if self.keyfile is False:
				response = requests.get(url, headers=self.default_headers, auth=self.auth_basic)
			else:
				files = {'private_key': open(self.keyfile, 'rb')}
				response = requests.post(url, files=files, headers=self,default_headers, auth=self.auth_basic)

			response.raise_for_status()
			
		except Exception as e:
			try:
				if self.keyfile is False:
					response = requests.get(url, headers=self.default_headers, auth=self.auth_disgest)	
				else:
					files = {'private_key': open(self.keyfile, 'rb')}
					response = requests.post(url, files=files, headers=self.default_headers, auth=self.auth_disgest)

				response.raise_for_status()

			except Exception as e:
				response = False
				raise ValueError(e)

		return response



	def get_form_data(self,
					  form_id,
					  long_format=0):	

		"""
			Function to get form data in csv format
			:param form_id: SurveyCTO's unique identifier for the form
			:param long_format: Set to 1 if data to be downloaded in long format, default is wide
		"""

		if (long_format == 0):
			url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/wide/csv/{form_id}'
			data = (get_data_from_url(self, url)).text
			return data
		else:
			# Get list of files and then get data for each file - Should the data be formatted as a dictionary
			print("to be written")



	def get_form_data_as_json(self,
					  	   	  form_id,
					  	      date=0):	

		"""
			Function to get form data in json format
			:param form_id: SurveyCTO's unique identifier for the form
			:param date: Date for which the data is to be downloaded, default 0 means all dates
		"""

		if (date != 0):
			# check date is correct
			print("to be written")
		
		url = f'https://{self.server_name}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={date}'
		data = (get_data_from_url(self, url)).json()
		return data



	def get_repeatgroup_data(self,
					  		 form_id,
					  		 repeat_group):			
		
		"""
			Function to get only single repeat group data
			:param form_id: SurveyCTO's unique identifier for the form
			:param repeat_group: Repeat group name
		"""

		url = f'https://{self.server_name}.surveycto.com/api/v1/forms/data/csv/{form_id}/{repeat_group}'
		data = (get_data_from_url(self, url)).text
		return data



	def get_dataset_data(self,
					  	 dataset_id):	
		
		"""
			Function to get server dataset data
			:param dataset_id: SurveyCTO's unique identifier for the dataset
		"""
		
		url = f'https://{self.server_name}.surveycto.com/api/v2/datasets/data/csv/{dataset_id}'
		data = (get_data_from_url(self, url)).text
		return data
