#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup
import re

"""
Reference: https://www.github.com/
Connector Version: 1.0.0
API Version: 1.0.0
API Type: REST
"""

class GithubConnector(object):
    def __init__(self,
                 **kwargs):
        api_version = 'v1'
        self.base_url = "https://www.github.com"
        self.headers = {"Accept": "*"}
        self.SUCCESS = "SUCCESS"
        self.ERROR = "ERROR"
        self.execution_status = "execution_status"
        self.result = "result"

    def test_connection(self, **kwargs):
        """
        Test Connection
        Used for checking the connectivity of the base url.
        :return: boolean (True/False)
        """
        try:
            url = "{0}".format(self.base_url)
            response = requests.request("GET", url)
            return response.status_code < 500
        except KeyError:
            return False

    def request_handler(self, method, endpoint,
                        **kwargs):
        try:
            base_url = "{0}/{1}".format(self.base_url, endpoint)
            base_url = base_url
            if method != "GET":
                return {self.result: 'Invalid Method {}\
                         Requested!'.format(method),
                        self.execution_status: self.ERROR}

            response = requests.get(base_url)
            return response.text if response.status_code == 200 else False
        except Exception as e:
            response_data = {'response': str(e)}
            execution_status = self.ERROR
        return {self.result: response_data,
                self.execution_status: execution_status}

    def search_repo_according_to_stars(self, search, **kwargs):
        '''
        This action is to query and get back information regarding a topic on github
        seach: Enter the search we want to search for
        '''
        endpoint = f'search?o=desc&q={search}&s=stars&type=Repositories'
        return self.request_handler('GET',endpoint)

    def search_repo_accoring_to_relavance(self, search, **kwargs):
        '''
        This action is to query and get back information regarding a topic on github based on search_repo_accoring_to_relavance
        search: Enter the search term we want to search for
        '''
        endpoint = f'search?q={search}'
        return self.request_handler('GET', endpoint)

    def get_required_data(self, data, **kwargs):
        '''
        This function is to query information from the raw html data
        '''
        if data:

            soup = BeautifulSoup(data, 'html.parser')
            data = soup.find_all('a', {'class':'v-align-middle'})

            return [item.text for item in data]


    def format_search(self, search, **kwargs):
        '''
        This function is used to format a normal search string into a github search
        '''

        search=search.replace(" ","+")
        return search

x=GithubConnector()
search = str(input("Enter search string: "))
search=x.format_search(search=search)
if x1 := x.search_repo_according_to_stars(search=search):
    a=x.get_required_data(str(x1))
    print(a)
else:
    print("We couldn't find any repositories matching ")
