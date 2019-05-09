# coding=utf-8
from unittest import TestCase

from sixecho import Client

class TestSixecho(TestCase):
    def test_tokenize(self):
        client = Client()
        word = 'ในการเขียนโปรแกรมในภาษา Python โมดูล (Module) คือไฟล์ของโปรแกรมที่กำหนดตัวแปร ฟังก์ชัน หรือคลาสโดยแบ่งย่อยออกไปจากโปรแกรมหลัก และสามารถนำมาใช้งานได้โดยการนำเข้ามาในโปรแกรม (Import) กล่าวอีกนัยหนึ่ง โมดูลก็คือไลบรารี่ที่สร้างไว้และนำมาใช้งานในโปรแกรม ในบทนี้ เราจะพูดถึงความหมายของโมดูล การสร้าง และการใช้งานโมดูลในการเขียนโปรแกรม นอกจากนี้ เราจะแนะนำให้คุณรู้จักกับ Package ซึ่งเป็นแนวคิดในการจัดการกับโมดูลในรูปแบบของ Namespace'
        words = client.tokenize(str=word)
        self.assertTrue(words>0)
        print("AAAAAAAAAAAAAA")
    
    # def printProgressBar(self):