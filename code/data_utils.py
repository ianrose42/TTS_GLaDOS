"""
Functions for downloading and formatting data to train a GLaDOS themed
text-to-speech model.
"""
import requests
from bs4 import BeautifulSoup as bs
import os
from os.path import join
import pandas as pd
from collections import OrderedDict
from time import sleep
from pathlib import Path
import inspect

def get_wav_url(s) -> dict:
    """
    Return dict with the url for a sound file, and the
    text corresponding to the speech in that sound file
    """
    try:
        key = s.find('i').text
    except:
        key = s.text
    value = set()
    for i in s.find_all('a', href=True):
        value.add(i['href'])
                  
    value = [i for i in value if i[-4::]=='.wav']
    return({key:value[0]})   

def download_wav_file(url, dir_path, use_sleep=True, wait_time = 15, **kwargs):
    """
    download a .wav file from a particular URL
    """
    file_name = url.split('/')[-1]
    file_path = os.path.join(dir_path, file_name)
    
    if not os.path.exists(file_path): 
        response = requests.get(url)
        f = open(file_path, 'wb')
        f.write(response.content)
        f.close()
    
        if use_sleep:
            sleep(wait_time)
            print('{} second sleep...'.format(wait_time))

def download_wav_file(url, dir_path, use_sleep=True, wait_time = 15, **kwargs):
    file_name = url.split('/')[-1]
    file_path = os.path.join(dir_path, file_name)
    
    if not os.path.exists(file_path):
        try:
            response = requests.get(url)
            f = open(file_path, 'wb')
            f.write(response.content)
            f.close()
        except: 
            if use_sleep:
                sleep(wait_time)
                response = requests.get(url)
                f = open(file_path, 'wb')
                f.write(response.content)
                f.close()
                print('{} second sleep...'.format(wait_time))

def make_soup(in_url: str,
            content_type='li',
            extension='.wav') -> OrderedDict:
    '''
    List urls for specified file type
    ''' 
    # get web page contents
    soup = bs(requests.get(in_url).content, 'html.parser')
    # find links in that page's contents
    links = soup.find_all('li')
    # get links for correct file type
    links = [i for i in links if extension in str(i)]
    out_links = OrderedDict()
    for i in links:
        out_links.update(get_wav_url(i))

    return out_links

def download_data(data_url: str,
                out_path: str,
                **kwargs):
    '''
    main function for downloading GLaDOS data
    '''
    # make meta data table
    soup_kwarge = 
    link_dict = make_soup()

# from:
# https://stackoverflow.com/questions/12627118/get-a-function-arguments-default-value
def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }

def add_kwargs(func, **kwargs):
    """
    Function to pass applicable kwargs given to parent function
    to appropriate child functions. 
    """
    applicable_kwargs = get_default_args(func)

    n_func_args = func.__code__.co_argcount
    all_func_vars = func.__code__.co_varnames
    func_args = all_func_vars[0:n_func_args]
    
    for a in [i for i in kwargs if i in func_args]:
        applicable_kwargs.update({a:kwargs[a]})

    return applicable_kwargs