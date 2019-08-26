from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
from datetime import datetime, timedelta,date
import time
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('application.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.

import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
cred = credentials.Certificate("firebasesecret.json")
firebase_admin.initialize_app(cred)





@app.route('/updatesheet') 
def result():
    store = firestore.client()
    doc_ref = store.collection(u'cred')
    thecreddict = ""
    try:
        docs = doc_ref.get()
        for doc in docs:
            print(u'Doc Data:{}'.format(doc.to_dict()))
            thecreddict = doc.to_dict()
    except google.cloud.exceptions.NotFound:
            print(u'Missing data')
    sheet = client.open_by_key(thecreddict['SPREAD_ID']['ID'])
    # Extract and print all of the values
    sheet1 = sheet.worksheet(thecreddict['SPREAD_ID']['FIRST_SHEET'])
    sheet2 = sheet.worksheet(thecreddict['SPREAD_ID']['SECOND_SHEET'])
    sheet1.clear()
    sheet2.clear()
    doc_ref = store.collection(u'data').document(u'paymenttrans').get().to_dict()
    allrowfirst = eval(doc_ref['theadata'])
    doc_ref = store.collection(u'data').document(u'gross').get().to_dict()
    secondrow = eval(doc_ref['theadata'])
    #print(allrowfirst)
    print("update sheet 1")
    sheet.values_update(
        thecreddict['SPREAD_ID']['FIRST_SHEET']+'!A1', 
        params={'valueInputOption': 'RAW'}, 
        body={'values': allrowfirst}
    )
    sheet.values_update(
        thecreddict['SPREAD_ID']['SECOND_SHEET']+'!A1', 
        params={'valueInputOption': 'RAW'}, 
        body={'values': secondrow}
    )
    return "yes the google sheet is updated"
if __name__ == '__main__':
   app.run()       