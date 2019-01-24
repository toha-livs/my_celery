# -*- coding: utf-8 -*-
from datetime import datetime
import logging
from celery import shared_task
from publish.models import Pad
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model


@shared_task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        email = EmailMessage('Title', 'Привет, как дела, все хорошо?', to=[user.email])
        email.send()
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user {}".format(user_id))


@shared_task
def display_time(x, y):
    print("The time is %s :" % str(datetime.now()))
    return True


@shared_task
def hook_olx_data(a):
    Pad.objects.all().delete()
    with webdriver.Chrome("/usr/lib/chromium-browser/chromedriver") as driver:
        driver.implicitly_wait(2)
        driver.get('https://www.olx.ua/zhitomir/q-{}/'.format(a))
        result = []
        row = 2
        while True:
            if row >= 45:
                break
            try:
                name = driver.find_element_by_xpath(
                    '//*[@id="offers_table"]/tbody/tr[{}]/td/div/table/tbody/tr[1]/td[2]/div/h3/a/strong'.format(
                        row)).text
                # print(name)
                price = driver.find_element_by_xpath(
                    '//*[@id="offers_table"]/tbody/tr[{}]/td/div/table/tbody/tr[1]/td[3]/div/p/strong'.format(
                        row)).text
                price_end = price.find(' грн')
                price = int(price[:price_end].replace(' ', ''))
                locate = driver.find_element_by_xpath(
                    '//*[@id="offers_table"]/tbody/tr[{}]/td/div/table/tbody/tr[2]/td[1]/div/p/small[1]/span'.format(
                        row)).text
                start_loc = locate.find(',')
                locate = locate[start_loc + 2:]
                result.append(Pad(name=name, price=price, locate=locate, date=datetime.now()))
                # yield {'name': name, 'price': price, 'locate': locate}
            except NoSuchElementException:
                pass
            row += 1
            pass
        Pad.objects.bulk_create(result)
    return True


# def web(a):
#     with webdriver.Chrome("/usr/lib/chromium-browser/chromedriver") as driver:
#         driver.implicitly_wait(2)
#         driver.get('https://www.olx.ua/zhitomir/q-{}/'.format(a))
#         result = []
#         row = 2
#         while True:
#             if row >= 50:
#                 return
#             try:
#                 name = driver.find_element_by_xpath(
#                     '//*[@id="offers_table"]/tbody/tr[{}]/td/div/table/tbody/tr[1]/td[2]/div/h3/a/strong'.format(
#                         row)).text
#                 # print(name)
#                 price = driver.find_element_by_xpath(
#                     '//*[@id="offers_table"]/tbody/tr[{}]/td/div/table/tbody/tr[1]/td[3]/div/p/strong'.format(
#                         row)).text
#                 locate = driver.find_element_by_xpath(
#                     '//*[@id="offers_table"]/tbody/tr[{}]/td/div/table/tbody/tr[2]/td[1]/div/p/small[1]/span'.format(
#                         row)).text
#                 start_loc = locate.find(',')
#                 locate = locate[start_loc + 2:]
#                 # result.append({'name': name, 'price': price, 'locate': locate})
#                 yield {'name': name, 'price': price, 'locate': locate}
#             except NoSuchElementException:
#                 pass
#             row += 1