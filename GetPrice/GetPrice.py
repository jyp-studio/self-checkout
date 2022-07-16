import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def gsheet(datalist):
       # google API , to post data to google sheet
    scope = ["https://spreadsheets.google.com/feeds",   
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"]

    # google api credentials , do not modify it 
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(credentials)
    sheet =  client.open("Digi_DataPrice").sheet1
    
    res = {} 
    dataframe = pd.DataFrame(sheet.get_all_records())
 
    count = 0
    # match the product name  and return its value
    for i in range(len(datalist)) : 
        index = dataframe.loc[dataframe['Data'] == datalist[i]]['Price'].index.values
        if len(index) != 0 :
            res[datalist[i]] = dataframe.at[index[0],'Price']
            count += dataframe.at[index[0],'Price']
        res['Total'] = count
        
    print(res)

def main():
    data = ['Iphone', 'Pork','hat','dog','dfsf ds','Houseplants']
    gsheet(data)

if __name__ == '__main__':
    main()
