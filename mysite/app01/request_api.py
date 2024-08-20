#-*- coding:utf-8 -*-
"""
Author: yuanchangtian
Data: 2024-07-05
Owner: Shanghai Dermatology Hospital
"""

import pyodbc  
import configparser
import sys
from openpyxl import Workbook
import requests
import certifi
import urllib3
urllib3.disable_warnings()
from app01.tools import get_sm4

class ShenKangRequest:
    def __init__(self, config):
        self.config = config
        self.base_url = self.config.get('ShenKang', 'base_url')
        #print (self.base_url)
    def request_token(self, ):
        """
        发送POST请求到指定的URL以获取token
        参数：
        grant_type: 授权类型，默认password
        client_id: 默认ddr-api
        client_secret: 默认secret
        scope: 授权作用域，默认ddr-api
        unername: 申康中心提供的账号对应的用户名
        password: 申康中心提供账号对应的密码
        返回：
        access_token：身份认证token或者令牌
        token_type：令牌类型
        expires_in：令牌有效时间，单位秒
        scope：授权作用域
        """
        url = self.base_url + self.config.get('ShenKang_Get_Token', 'api')
        headers = {
            'Content-Type':  self.config.get('ShenKang_Get_Token', 'content_type')
        }
        #print ('请求地址：', url, '\n', '请求头：', headers)
        data = {}
        params = self.config.items('ShenKang_Get_Token')
        #print (params)
        for param in params:
            if param[0] in ('grant_type', 'client_id', 'client_secret', 'scope', 'username', 'password'):
                data[param[0]] = param[1]
        #print ('请求参数：', data)
        try:
            response = requests.post(url, data=data, headers=headers, verify=False)
            print ('状态码：', response.text)
            response.raise_for_status() #如果响应状态码不是200，将抛出HTTPError异常          
            return response.json()
        except requests.RequestException as e:
            print (f"请求token失败：{e}")         
            return None
        
    def request_upload_value_domain_dict(self, token, path):
        """
        发送POST请求到指定的URL以上传值阈字典
        请求头：
        Authorization: 身份认证令牌token
        Content-Type: multipart/form-data
        参数：无
        返回：
        code：状态响应码，成功200
        message：响应消息
        data：响应数据
        """
        url = self.base_url + self.config.get('ShenKang_Upload_Value_Domain_Dict', 'api')
        headers = {
            'Content-Type':  self.config.get('ShenKang_Upload_Value_Domain_Dict', 'content_type'),
            'Authorization' : token
        }
        print (url, '\n', headers)
        files = {'file': open(path, 'rb')}
        try:
            
            response = requests.post(url, files=files, headers=headers, verify=False)
            response.raise_for_status() #如果响应状态码不是200，将抛出HTTPError异常
            return response.json()
        except requests.RequestException as e:
            print (f"上传值阈字典失败：{e}")
            return None
    def request_search_value_domain_dict(self, token_response):
        """
        发送POST请求到指定的URL以查询值阈字典
        请求头：
        Authorization : 身份认证令牌token
        Content-Type : application/json;charset=utf-8
        参数：无
        返回：
        code：状态响应码，成功200
        message：响应消息
        data：响应数据
        """
        url = self.base_url + self.config.get('ShenKang_Search_Value_Domain_Dict', 'api')
        access_token = token_response['access_token']
        token_type = token_response['token_type']
        headers = {
            'Content-Type':  self.config.get('ShenKang_Search_Value_Domain_Dict', 'content_type'),
            'Authorization' : f"{token_type} {access_token}"
        }
        #print ('请求地址：', url, '\n', '请求头：', headers)
        data = {}
        params = self.config.items('ShenKang_Search_Value_Domain_Dict')
        #print (params)
        for param in params:
            if param[0] in ('code'):
                data[param[0]] = param[1]
        print ('查询阈值字典请求参数：', data)
        try:            
            response = requests.post(url, data=data, headers=headers, verify=False)
            response.raise_for_status() #如果响应状态码不是200，将抛出HTTPError异常
            print (response.text)
            return response.json()
        except requests.RequestException as e:
            print (f"查询值阈字典失败：{e}")
            return None
        
    def request_upload_data(self, token_response):
        """
        发送POST请求到指定的URL以上传专病数据
        请求头：
        Authorization : 身份认证令牌token
        Content-Type : application/json;charset=utf-8
        """
        url = self.base_url + self.config.get("ShenKang_Upload_Data", "api")
        access_token = token_response["access_token"]
        token_type = token_response["token_type"]
        headers = {
            "Content-Type":  self.config.get("ShenKang_Upload_Data", "content_type"),
            "Authorization" : f"{token_type} {access_token}"
        }
        #print ('请求地址：', url, '\n', '请求头：', headers)
        data = {}
        modelInfo = {"code" : self.config.get('ShenKang_Upload_Data', 'model_code'),
                     "name" : self.config.get('ShenKang_Upload_Data', 'model_name')}
        hospital = {"name" : self.config.get('ShenKang_Upload_Data', 'hospital_name'),
                    "code" : self.config.get('ShenKang_Upload_Data', 'hospital_code'),
                    "centreType" : self.config.get('ShenKang_Upload_Data', 'hospital_centreType')}
        modelData = []
        modelData.append({"modelCode": "DP_Admission_Record",
                     "description" : "入院录",
                     "items" : [[]]})
    
        modelData[0]['items'][0].append({'PropertyCode' : 'patient_id', 'propertyValue' : '343046'})
        modelData[0]['items'][0].append({'PropertyCode' : 'YLJGDM', 'propertyValue' : '42500278100'})
        modelData[0]['items'][0].append({'PropertyCode' : 'SFZH', 'propertyValue' : get_sm4('342222199107116496', config.get('Database', 'sm4_key'))})
        modelData[0]['items'][0].append({'PropertyCode' : 'SJSCSJ', 'propertyValue' : '2023-03-17 00:00:00'})
        modelData[0]['items'][0].append({'PropertyCode' : 'JZLSH', 'propertyValue' : '48898'})
        modelData[0]['items'][0].append({'PropertyCode' : 'ccfbyy', 'propertyValue' : '无明显诱因'})
        modelData[0]['items'][0].append({'PropertyCode' : 'ccfbbw', 'propertyValue' : '下肢'})
        modelData[0]['items'][0].append({'PropertyCode' : 'xys', 'propertyValue' : '偶尔'})
        modelData[0]['items'][0].append({'PropertyCode' : 'yjs', 'propertyValue' : '偶尔'})
        modelData[0]['items'][0].append({'PropertyCode' : 'yxbjzs', 'propertyValue' : '无'})
        modelData[0]['items'][0].append({'PropertyCode' : 'bfjbs', 'propertyValue' : '体健'})
        modelData[0]['items'][0].append({'PropertyCode' : 'yxbbc', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'zjzz', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'gjtbs', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'gjtbc', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'ccfbsn', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'bcz_nps', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'ccnpsj', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'bcz_hps', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'cchpsj', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'bcz_gjtbs', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'bcz_gjtbx', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'jwzlqk', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'psqczcsj', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'xyns', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'xyl', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'jyns', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'yjns', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'jjns', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'hyzk', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'syzk', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'jzs_yjqs', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'jzs_ejqs', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'jzs_sjqs', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'psbw', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'psfb', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'psxt', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'lxzt', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'zjshzk', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'zjshbx', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'slszjs', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'slzzjs', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'zjshyzcd', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'xy_gjtqk', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'xy_gjtwz', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'xy_gjtsl', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'xy_gjztbx', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'pasi', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'bsa', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'mnapsi', 'propertyValue' : ''})
        modelData[0]['items'][0].append({'PropertyCode' : 'yxblx', 'propertyValue' : ''})
        

        
        data['modelInfo'] = modelInfo
        data['hospital'] = hospital
        data['modelData'] = modelData

        print ('请求头：', headers)
        print ('上传数据请求参数：', data)
        try:
            
            response = requests.post(url, json=data, headers=headers, verify=False)
            response.raise_for_status() #如果响应状态码不是200，将抛出HTTPError异常
            print (response.text)
            return response.json()
        except requests.RequestException as e:
            print (response.text)
            print (f"上传数据失败：{e}")
            return None
        
    def request_upload_log(self, token_response):
        """
        发送POST请求到指定的URL以上传专病数据日志
        请求头：
        Authorization : 身份认证令牌token
        Content-Type : application/json;charset=utf-8
        """
        url = self.base_url + self.config.get('ShenKang_Upload_Log', 'api')
        access_token = token_response['access_token']
        token_type = token_response['token_type']
        headers = {
            'Content-Type':  self.config.get('ShenKang_Upload_Log', 'content_type'),
            'Authorization' : f"{token_type} {access_token}"
        }
        print ('请求地址：', url, '\n', '请求头：', headers)
        data = {}
        data['DiseaseCode'] = self.config.get('ShenKang_Upload_Log', 'disease_code')
        print ('查询日志请求参数：', data)
        url = url + '?DiseaseCode=L40'
        print (url)
        try:
            
            response = requests.post(url, data=data, headers=headers, verify=False)
            response.raise_for_status() #如果响应状态码不是200，将抛出HTTPError异常
            print (response.text)
            return response.json()
        except requests.RequestException as e:
            print (response.text)
            print (f"查询日志失败：{e}")
            return response.json()
if __name__ == "__main__":  
    config = configparser.ConfigParser()
    config.read('./conf/config.ini', encoding='utf-8')
    sections = config.sections()
    options = config.options('ShenKang_Get_Token')
    items = config.items('ShenKang_Get_Token')
    #print (items)
    SKReq = ShenKangRequest(config)
    #token_response = SKReq.request_token()
    #if token_response:
    #    print ("Token响应:", token_request)
    #else:
    #    print ("未获取到Token")
    path = './data/test.xlsx'
    token_response = SKReq.request_token()
    #upload_data_response = SKReq.request_upload_data(token_response)
    upload_data_log = SKReq.request_upload_log(token_response)
    #if upload_value_domain_dict_response:
    #    print ("上传值阈字典成功:", token_request)
    #else:
    #    print ("上传值阈字典失败！！！")


