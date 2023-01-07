#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/06 19:00:46
# @Author: wd-2711
'''

import os
import base64
import pandas as pd
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

from configLoader import getYamlData

class infoExtracter:
    def __init__(self):
        config = getYamlData('config.yaml')
        self.in_path = config['TableImagePath']
        self.op_path = config['ExcelPath']
        self.data_path = config['InfoPath']
        self.secret_id = config['SecretId']
        self.secret_key = config['SecretKey']
        
    def run(self):
        """
            InfoExtracter runner
        """
        print("[+] Start extracter.")
        if len(os.listdir(self.op_path)) == 0:
            for ind, f in enumerate(os.listdir(self.in_path)):
                print("[+] Recognize picture {} ...".format(ind))
                assert self.__ocrRecognize(f)
        else:
            print("[+] Have recognized before.")
        print("[+] Excel processing and save.")
        self.__saver(self.__getExcelData())
        print("[+] Done.")
        return self.__getExcelData()

    def __ocrRecognize(self, p):
        """
            Extract data from every image and save data in excel.
        """
        # only for jpg
        op_path = os.path.join(self.op_path, p.replace('jpg', 'xlsx'))
        in_path = os.path.join(self.in_path, p)

        cred = credential.Credential(
            self.secret_id,
            self.secret_key
        )
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        clientProfile.signMethod = "TC3-HMAC-SHA256"

        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)
        req = models.GeneralFastOCRRequest()

        with open(in_path, 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding = 'utf-8')

        req.ImageBase64 = image_base64
        resp = client.RecognizeTableOCR(req)
        data = base64.b64decode(resp.Data)
        with open(op_path, 'wb') as f:
            f.write(data)
        return True

    def __getExcelData(self):
        """
            Name and phone
        """
        allData = pd.DataFrame(columns=['name', 'phone'])
        for f in os.listdir(self.op_path):
            f = os.path.join(self.op_path, f)
            frame = pd.read_excel(f, 'Sheet1', header = None)
            phone = frame.iloc[:, -1][frame.iloc[:, -1].astype(str).str.match(r"^\d{11}$")]
            name = frame.iloc[:, -3][frame.iloc[:, -3].astype(str).str.match(r"^[\u4E00-\u9FA5]{2,4}$")]
            d = pd.concat([name, phone], axis = 1)
            d.columns = ['name', 'phone']
            allData = pd.concat([allData, d], axis = 0, ignore_index = True)
        return allData.to_dict(orient = "records")

    def __saver(self, data):
        """
            Save data
        """
        with open(self.data_path, 'w', encoding = 'utf-8') as f:
            for d in data:
                f.write(str(d) + '\n')

if __name__ == "__main__":
    model = infoExtracter()
    data = model.run()
    print(data)


