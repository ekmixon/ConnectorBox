#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup
import re

"""
Reference: https://www.cvedetails.com/
Connector Version: 1.0.0
API Version: 1.0.0
API Type: REST
"""

class CVEConnector(object):
    def __init__(self,
                 **kwargs):
        api_version = 'v1'
        self.base_url = "https://www.cvedetails.com/"
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
            url = "{0}".format(self.base_url) #https://cvedetails.com
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

    def action_get_details(self, cve_id, **kwargs):
        '''
        This action is to query and get back information regarding a CVE_ID
        cve_id: Enter the CVE ID we want to search for
        '''
        endpoint = f'cve/{cve_id}'
        return self.request_handler('GET',endpoint)

    def check_if_valid(self, data, **kwargs):
        '''
        This function is to check if the entered CVE ID is check_if_valid
        '''
        return """Unknown CVE ID""" not in data

    def get_required_data(self, data, **kwargs):
        '''
        This function is to query information from the raw html data
        '''
        soup = BeautifulSoup(data, 'html.parser')
        summary = soup.find('div', {'class':'cvedetailssummary'})
        print(f"Summary of the vulnerability is: {summary.text.strip()}")
        score = soup.find('div', {"class": "cvssbox"})
        print(f"Vulnerability score is: {score.text.strip()}")
        confidentiality_impact=soup.find('span',{'class':'cvssdesc'})
        print(f"Confidentiality impact is: {confidentiality_impact.text.strip()}")


x=CVEConnector()
id = str(input("Enter CVE ID: "))
x1=x.action_get_details(cve_id=id)
status=x.check_if_valid(x1)
if(status==True):
    a=x.get_required_data(x1)
else:
    print("CVE-ID NOT VALID")
