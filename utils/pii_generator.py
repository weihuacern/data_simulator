import random
import time
import uuid

import names
import pymssql
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from constants import PII_CATALOG
from utils import rand_x_digit_num

#ssn, name, gender, phone number, email, blood_type
class fakepiientry:
    def __init__(self):
        self.pii_catalog = PII_CATALOG
        self.gender = ["Male", "Female"]
        self.email_domain = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com"]
        self.blood_type = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]

    def __generate_uniform(self, target_list):
        return target_list[random.randint(0, len(target_list)-1)]

    def __generate_phonenumber(self):
        first = str(random.randint(100,999))
        second = str(random.randint(1,888)).zfill(3)
        last = (str(random.randint(1,9998)).zfill(4))
        while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
            last = (str(random.randint(1,9998)).zfill(4))
        return ('{}-{}-{}'.format(first, second, last))

    def __generate_email(self, pii_name):
        pii_email = pii_name.replace(' ', '.').lower() + "@" + self.__generate_uniform(self.email_domain)
        return pii_email

    def generate_pii_row(self, seed):
        """
        input: one integer seed for this generation
        output: a dictionary, key is defined in the pii_catalog
        """
        pii_ssn = rand_x_digit_num(9, False)
        pii_name = names.get_first_name() + ' ' +  names.get_last_name()
        pii_gender = self.__generate_uniform(self.gender)
        pii_phone = self.__generate_phonenumber()
        pii_email = self.__generate_email(pii_name)
        pii_blood_type = self.__generate_uniform(self.blood_type)
        res_keys = self.pii_catalog
        res_vals = [pii_ssn, pii_name, pii_gender, pii_phone, pii_email, pii_blood_type]
        res = dict(zip(res_keys, res_vals))
        return res

if __name__ == "__main__":
    myfakepiientry = fakepiientry()
    for i in range(100, 105):
        this_pii_row = myfakepiientry.generate_pii_row(i)
        print(this_pii_row)
