# -*- coding: utf-8 -*-
from django.http import Http404, JsonResponse
from django.shortcuts import render
from .models import Post, Pad
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core.mail import EmailMessage
from main.tasks import send_verification_email


def view_post(request, slug):
    UserModel = get_user_model()
    user = UserModel.objects.get(pk=request.user.id)
    # send_verification_email.delay(request.user.id)
    email = EmailMessage('Title', 'Привет, как дела, все хорошо?', to=[user.email])
    email.send()
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Poll does not exist")

    return render(request, 'post.html', {'post': post})


def get_data(request):
    Pad.objects.all().delete()
    with webdriver.Chrome("/usr/lib/chromium-browser/chromedriver") as driver:
        driver.implicitly_wait(2)
        driver.get('https://www.olx.ua/zhitomir/q-{}/'.format('планшет'))
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