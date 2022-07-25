import gspread
# from oauth2client.soauth2clientervice_account import ServiceAccountCredentials
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


 # google API , to post data to google sheet
scope = ["https://spreadsheets.google.com/feeds",   
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]

# google api credentials , do not modify it 
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
sheet =  client.open("Digi_DataPrice").sheet1

SoldList = []

def gsheet(datalist):
   
    # output dictionary for prices(including total price) and product name
    res = {} 
    
    # dictionary for inventories of product and product name "BEFORE THE PURCHASE"
    PreInvres = {}

    # output dictionary for inventories of product and product name
    Invres = {}
    
    # it is used to count total prices 
    count = 0

    # 購買前的商品庫存量
    dataframe = pd.DataFrame(sheet.get_all_records())
    for i in range(len(datalist)) : 
        index = dataframe.loc[dataframe['Data'] == datalist[i]]['Price'].index.values
        if len(index) != 0 :
            
            # 找出這個產品還有多少庫存量
            PreInventoryRes = dataframe.iloc[index]['Inventory']
            # 型態轉換
            PreLeftStock = PreInventoryRes.tolist()
            PreInvres[datalist[i]] = PreLeftStock[0]


    # match the product name  and return its value
    for i in range(len(datalist)) : 
        dataframe = pd.DataFrame(sheet.get_all_records())
    
        # To see if the cloud storage has the product or not, and return row index 
        index = dataframe.loc[dataframe['Data'] == datalist[i]]['Price'].index.values
        if len(index) != 0 :

            #----------Get the price from cloud-----------------#
            res[datalist[i]] = dataframe.at[index[0],'Price']

            # count is the total price to buy all products
            count += dataframe.at[index[0],'Price']
            

            #--------Get inventories of product "AFTER the purchase" ---------------#
            
            # get the inventory of the product, and then update the latest inventory value  
            InventoryRes = int(dataframe.iloc[index]['Inventory']) 
            InventoryRes -= 1

            # 更新後的商品庫存量 ，接著要把這些資訊上傳至資料庫
            LeftStock = InventoryRes

            # 找出cloud storage裡面對應到 Inventory 的 column index 
            ProductInvCol = dataframe.columns.get_loc("Inventory")
            
            # update the latest inventory value to google sheet 
            sheet.update_cell(index +2 , ProductInvCol +1 , LeftStock)

            # 存成dict型式
            Invres[datalist[i]] = LeftStock
            

            #--------上傳該次購買商品的數量到另外一個google sheet ---------------#
            # 開啟儲存個產品銷量的google sheet            
            Soldsheet = client.open('Digi_DataPrice').worksheet('SellingRecord')
            Solddataframe = pd.DataFrame(Soldsheet.get_all_records())
            
            # Get the quantity that has been sold before
            # 找出該產品之前已經賣過多少數量
            SoldAmount = int(Solddataframe.iloc[index]['SoldAmount'])
            SoldAmount += 1 

            # 找出cloud storage裡面對應到 SoldAmount 的 column index 
            SoldAmountCol = Solddataframe.columns.get_loc("SoldAmount")
            
            # upload 
            Soldsheet.update_cell(index +2 , SoldAmountCol +1  , SoldAmount)
            
            print("--------------")

        res['Total'] = count
    
   
    print(f"Each price of product and total value : {res}")
    print(f"The inventories of products before purchasing : {PreInvres} ")
    print(f"The inventories of products after purchasing  : {Invres} " )
    return res, Invres

def main():
    data = ['mouse', 'mouse', 'keyboard','cup','laptop','chair','Nothing']
    print(len(data))
    SoldData, InventoryData = gsheet(data)
    print(SoldData)
    print("+++++")
    print(InventoryData)

if __name__ == '__main__':
    main()
