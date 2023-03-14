import datetime
import requests

def get_cutoff_time(param: int):
    """
    If the length is 4, the function extracts the first two characters as the hour
    and the last two characters as the minute of the cutoff time. 
    It then creates a datetime.time object with these values and returns it.
    If the length of the string is not 4, the function returns an empty string
    """
    if isinstance(param, int):
        str_time = str(param)
        if len(str_time) == 4:
            cutoff_time_hour = int(str_time[:2])
            cutoff_time_min = int(str_time[2:])
            cut_off_time = datetime.time(cutoff_time_hour, cutoff_time_min)
        else:
            cut_off_time = ''
    else:
        cut_off_time = ''
    return cut_off_time


def convert_date_format(param_date: str):
    """
    This Python function converts a date string in ISO format to a date object in UTC timezone.
    """
    return datetime.datetime.fromisoformat(param_date[:-1] + '+00:00').date()


def get_status_flag(param1, param2):
    """
    If "param1" is found in "param2", the function returns True. Otherwise, it returns False.
    """
    return True if param1 in param2.lower() else False



def get_response_from_api(url : str):
    """
    This method is to fetch the response from KFin API using GET method
    """
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        #print(json_response)
        return json_response
    else:
        return response.status_code