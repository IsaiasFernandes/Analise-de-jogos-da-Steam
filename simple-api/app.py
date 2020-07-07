# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import time
import requests
from flask_cors import CORS
API_KEY = "89cc6390-b8bb-11ea-9b07-07be0860785734f43c6b-7b8a-4447-bcbf-54fabba42544"


app = Flask(__name__)
CORS(app)


class Steam:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://store.steampowered.com/?l=portuguese'
        self.search_bar = 'store_nav_search_term'
        self.Review = 'page1'

    def navigate(self):
        self.driver.get(self.url)

    def search(self, word='None'):
        self.driver.find_element_by_id(self.search_bar).send_keys(word)
        time.sleep(2)
        self.driver.find_element_by_id(
            self.search_bar).send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        self.driver.find_element_by_id(
            self.search_bar).send_keys(Keys.ENTER)

    def searchReview(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'apphub_AppName')))

        name = self.driver.find_element_by_class_name('apphub_AppName')
        name = name.text
        SCROLL_PAUSE_TIME = 0.5

        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        while True:

            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'ViewAllReviewssummary')))
        self.driver.find_element_by_xpath(
            "//a[contains(text(),'Ver todas as análises')]").click()

        return name

    def _take_Review(self):
        return self.driver.find_element_by_id(self.Review)

    def get_all_Reviews(self):

        reviews = self._take_Review()
        return reviews.get_attribute("outerHTML")


def take_Review_bs4(scrapingData):
    soup = BeautifulSoup(scrapingData, 'html.parser')
    time.sleep(5)
    msg = soup.findAll('div', 'apphub_CardTextContent')
    return msg


def classify(text):
    urlM = "https://machinelearningforkids.co.uk/api/scratch/" + API_KEY + "/classify"

    response = requests.get(
        urlM, params={"data": text})

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


def start(name):
    ff = webdriver.Firefox()
    s = Steam(ff)
    s.navigate()

    s.search(name)
    dice = s.searchReview()

    time.sleep(5)
    scrapingData = s.get_all_Reviews()
    time.sleep(2)
    clean = take_Review_bs4(scrapingData)
    cont = 0
    bem = 0
    mal = 0
    for cl in clean:

        date_posted = cl.find('div', 'date_posted')
        early_access_review = cl.find('div', 'early_access_review')

        date_posted.decompose()
        if early_access_review != None:
            early_access_review.decompose()

        texto = cl.text
        demo = classify(texto[0:1000])
        label = demo["class_name"]
        confidence = demo["confidence"]
        if label == 'Falar_Bem':
            bem += 1
        else:
            mal += 1
        cont += 1

    ff.quit()

    dadosRetorno = (bem, mal, cont, dice)

    return dadosRetorno


@app.route('/games', methods=['POST'])
def games():
    data = request.get_json()

    if data == '':
        return jsonify({'error': 'not found'}), 404
    else:
        dados = start(str(data['name']))

        return jsonify(dados), 201


if __name__ == '__main__':
    app.run(debug=True)
