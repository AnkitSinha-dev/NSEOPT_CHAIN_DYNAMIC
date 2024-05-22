import requests
import pandas as pd
import numpy as np
import time
import xlwings as xw
from bs4 import BeautifulSoup
import datetime
import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

TWO_PERCENT_MARKET_PRICE = 0.0

exchange = "NSE"


url_oc      = "https://www.nseindia.com/option-chain"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br','cookie': '_ga=GA1.1.188925864.1709098563; _abck=090717AC8F08A622AF4C26A071A53A2C~0~YAAQBtksMTkjtZKPAQAAY9v9nwuoTOqpxMtfK32MkXluSrg07nXXlPVkKyTwFjuNq9i5QiBHuuMC2tNPW814fQHu/G4TEVCDLpfVwEm0h0P/XXXrfhfUjjgST8wIn/T4ktCu2f7YQVO/wa9lC740GhcbwoKXMcum11mGic19r/gq2Q057U2DAyjl6AwWH380UwDOYA/4EKBPOSofQC19/U5w4qMUc0W9kKsNaF9Iqrzmh6qZ5XCxatH6/GtIaPBL6SeGqIpMNI5pN6IWn9i4Bp+//2vkPtPis4jIQD+hxo09nb3BbTAUHste0YIjdw1RifG1/Xl3DtVrlwoeyGzIj5Bk4UJcXAGYGsHiAtKdAoa67lDj2wzbyEsiAUjPdbDgLje6Jm+CP9q5ru0zu39LH3NxlJkqj4LmZRr5~-1~-1~-1; AKA_A2=A; defaultLang=en; nsit=shQlaYsktVw69GeSCPeT_rz3; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTcxNjM4NTE1NiwiZXhwIjoxNzE2MzkyMzU2fQ.3_Qdw7AjvbvFH6YwpykVjQguMdUl3HaM24vlRzb9TwU; bm_mi=DC22684E2085F92F83EBC27E9839FE1C~YAAQLNksMc6Pvn2PAQAAzhOHoBeo8RUBiDc7ThmhomC6WhWjv4FPwnMBwrX8YYBdNw2aUiotX9ff1FbZcEmI2e+oOmWyaIMs/YHfpYhQr/NwEICBMmuJ0rV2BbqtOuLxMkFRlkXVqkgBsHpTNKM7dlfpJPs0mIpEjogOvO8gjNE8seYvVFbgfms+tfEeLXcq8kAH60z/db/Jv8OpWOhM7gchAIsP6ksk94b2wI25D/raOSSAuHJFNBuxxdDMk3tL9abOON/sWsAhFQD7pP/UHrcRTudjF2g0cptN4Gr8GBxgHQOk7OA4IFzKvdOYUwFjgEWyC5DMflOCSOJi~1; bm_sz=D68195DF087C7242B9711C14141DC0D7~YAAQLNksMdCPvn2PAQAAzhOHoBcO0oTjD0gu8b/sBrv8yCtddoxydFUIaHupOhbxHk6YwBDkrzZ6yxPKnBcsYbYRGKGGiL/ucsgcj44++rv8vobsQ07nUXYVKc3DHi8seGG2UgxONIFcfhtrLXGBxn20UHI6Wud7LQyVNsTob1DVEsPROW09IzjjwlV6Nxkc705Y3LRwXNqwyHOVmI881GQYJj0bJPbRZH1jgyrogF1KpNzd4Hk6NnzWbsL5TTj246yK/osLtc1Q22IBoZF2ia+wU6sx3JD1+UaqO+2E+CyA3l0SfTrK4Gff5RDcai017qC+j6BkHc3s/e+MCw05ZQimye+pvJ60qAGUzo4UY/R12HsGMkTZHrAEImup7fDg6BS/5EHPnVwxxacHq3s62Dll5HXmUoxH4Ko/PXt6swfDgwC+6aMCbhGjOTOnHQWZL7PAd9GHA85Zm63fmGpWFBib~4404547~3289138; _ga_QJZ4447QD3=GS1.1.1716385095.26.0.1716385095.0.0.0; _ga_87M7PJ3R97=GS1.1.1716385095.35.1.1716385095.0.0.0; ak_bmsc=CB5DB84F982757D43C1728EDB11CF5DD~000000000000000000000000000000~YAAQLNksMeyPvn2PAQAAIxmHoBeU3+8kwgQqgE537IJ5vVTwfiOF1XMV+pqCMblj2UXBK2cNic1jphITkicr/I+ZSidiC3O1oM+59IQzc/0kdr9tyJCJPJiDKveEY1GL19fyI5vm9hgpW7ymdJpIjglXwhrdXd7w+huc+CTb8oE405a3ZyMYn4pNHmEAQU1VVhPNPIv3lX0yAmTTYdVj6w1fH9c3LvMT3h3dAhUKUuGr1Qw1QEhIFjTKbq6wI074FOjzRsS2onTOr3i0/f0E8OHRAGxI+ZCXIYx4vx3Gyv2HS7A6gVXJKGr5IGtGAsQElHNupSNDXGq6z76G+sScwrHE2ePs2cPiZ+i8Qlu+LCniRrNumlLdRRAuxzyFJ+PPnJJwx5OWEyJIxTmbezFr9jXp4ZBy9+MlBYi84u8u1/RU5rzoU6B8EeQFBVyn81SSpI7ifFwPg+8JV+G/dmp+yW8odUsx5ntOrT7v9F42uUvdHKCNJl2YN9Bj0jv0aw==; bm_sv=02E6EAC8CFC4CB6D65EF2FBCA5BC48E0~YAAQLNksMYGQvn2PAQAABjWHoBetXvdKkq75B93Bhl0PcR/jdzOYzGEWlaHZnCzVxYlBxZ4yfXk9puWGJ/4jMKKZUGNngky6ITuE6CmjoaSpJUVGYfm30dDnoToMxJ7ipkJwJRKVJxAOlK5WIjjy/W+H3JvUAC80lWFX/YKeIuOAKb39vbjG0gwc1wh6bLw+QEMQ5a5+G5bFacwrPbctnZZz73wuadLDdW6elQSUbDhAfDnZiUzHJsHACWBjlczbDs93tA==~1; RT="z=1&dm=nseindia.com&si=b33114a2-d4ed-4b59-9f6b-6de70b0be718&ss=lwhvdaly&sl=0&se=8c&tt=0&bcn=%2F%2F684d0d46.akstat.io%2F&ld=1orzk&nu=kpaxjfo&cl=afd'}
sess = requests.Session()
cookies = dict()




def set_cookie():
    request = sess.get(url_oc, headers=headers)
    cookies = dict(request.cookies)
    
    
    


def last_thursdays(year):
    exp = []
    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        if month == 1 or month == 2 or month == 3 or month == 4 or month == 5 or month == 6 or month == 7 or month == 8 or month == 9:
            date = f"{year}-0{month}-01"
        if month == 10 or month == 11 or month == 12:
            date = f"{year}-{month}-01"

        # we have a datetime series in our dataframe...
        df_Month = pd.to_datetime(date)

        # we can easily get the month's end date:
        df_mEnd = df_Month + pd.tseries.offsets.MonthEnd(1)

        # Thursday is weekday 3, so the offset for given weekday is
        offset = (df_mEnd.weekday() - 3) % 7

        # now to get the date of the last Thursday of the month, subtract it from
        # month end date:
        df_Expiry = df_mEnd - pd.to_timedelta(offset, unit='D')
        exp.append(df_Expiry)

    return exp


def current_market_price(ticker, exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"

    for _ in range(1000000):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        class1 = "YMlKec fxKbKc"

        price = float(soup.find(class_=class1).text.strip()[1:].replace(",", ""))
        yield price

        time.sleep(5)


def get_dataframe(ticker, exp_date_selected):
    set_cookie()
    while True:
        try:

            url = f"https://www.nseindia.com/api/option-chain-equities?symbol=UBL"
     
            data = sess.get(url, headers=headers,cookies=cookies).json()["records"]["data"]
            ocdata = []
            for i in data:
                for j, k in i.items():
                    if j == "CE" or j == "PE":
                        info = k
                        info["instrumentType"] = j
                        ocdata.append(info)

            df = pd.DataFrame(ocdata)
            # wb = xw.Book("optionchaintracker.xlsx")
            # st = wb.sheets("vedl")
            # st.range("A1").value = df
            # print(df)

            expiry_dates = df['expiryDate'].unique().tolist()
            fin_exp_dates = []
            for i in expiry_dates:
                temp_expiry = datetime.datetime.strptime(i, '%d-%b-%Y')
                fin_exp_dates.append(temp_expiry.strftime('%d-%m-%Y'))

            strikes = df.strikePrice.unique().tolist()
            strike_size = int(strikes[int(len(strikes) / 2) + 1]) - int(strikes[int(len(strikes) / 2)])

            for price in current_market_price(ticker, exchange):
                two_percent_cmp = price + 0.02 * price
                TWO_PERCENT_MARKET_PRICE = two_percent_cmp
                break

            print(TWO_PERCENT_MARKET_PRICE)

            # access dataframe for atm price
            atm = int(round(TWO_PERCENT_MARKET_PRICE / strike_size, 0) * strike_size)
            print(atm)

            output_ce = pd.DataFrame()

            atm_pe = atm
            output_pe = pd.DataFrame()

            for _ in range(5):

                # (for ce)
                ab = True
                while ab:

                    fd = df[df['strikePrice'] == atm]

                    if fd.empty:
                        print("empty df ce", atm)
                        atm = atm + 0.5
                        if atm > strikes[-1]:
                            break
                    else:
                        ab = False

                # print(fd)

                # (for pe)
                ab_pe = True
                while ab_pe:

                    fd_pe = df[df['strikePrice'] == atm_pe]

                    if fd_pe.empty:
                        print("empty df pe", atm_pe)
                        atm_pe = atm_pe - 0.5
                    else:
                        ab_pe = False

                # print(fd_pe)

                # (for ce)convert expiry date in particular format
                fd = fd.reset_index()
                for i in range(len(fd)):
                    expiry_date_str = fd["expiryDate"].iloc[i]
                    temp_expiry = datetime.datetime.strptime(expiry_date_str, '%d-%b-%Y')
                    result_expiry = temp_expiry.strftime('%d-%m-%Y')
                    fd.at[i, "expiryDate"] = result_expiry
                # print(fd)
                # print(type(fd["expiryDate"].iloc[0]))

                # (for pe) convert expiry date in particular format
                fd_pe = fd_pe.reset_index()
                for i in range(len(fd_pe)):
                    expiry_date_str_pe = fd_pe["expiryDate"].iloc[i]
                    temp_expiry_pe = datetime.datetime.strptime(expiry_date_str_pe, '%d-%b-%Y')
                    result_expiry_pe = temp_expiry_pe.strftime('%d-%m-%Y')
                    fd_pe.at[i, "expiryDate"] = result_expiry_pe

                adjusted_expiry = exp_date_selected
                adjusted_expiry_pe = exp_date_selected

                # (subset_ce (CE))
                subset_ce = fd[(fd.instrumentType == "CE") & (fd.expiryDate == adjusted_expiry)]
                # print(subset_ce)
                output_ce = pd.concat([output_ce, subset_ce])

                # (subset_pe (PE))
                subset_pe = fd_pe[(fd_pe.instrumentType == "PE") & (fd_pe.expiryDate == adjusted_expiry_pe)]
                # print(subset_pe)
                output_pe = pd.concat([output_pe, subset_pe])

                # (for CE)
                atm += strike_size

                # (for PE)
                atm_pe -= strike_size

            output_ce = output_ce[["strikePrice", "expiryDate", "lastPrice", "instrumentType"]]
            output_pe = output_pe[["strikePrice", "expiryDate", "lastPrice", "instrumentType"]]

            output_ce.reset_index(drop=True, inplace=True)
            output_pe.reset_index(drop=True, inplace=True)

            return output_ce, output_pe

        except Exception as e:
            pass


# output_ce, output_pe = get_dataframe()
# print(output_ce)
# print(output_pe)
def highlight_ratio(s):
    if s["CE Premium %"] > 1:
        if s["PE Premium %"] > 1:
            return ['background-color: paleturquoise'] * len(s)
        else:
            return ['background-color: paleturquoise'] * 2 + ['background-color: white'] * 2
    else:
        if s["PE Premium %"] > 1:
            return ['background-color: white'] * 2 + ['background-color: paleturquoise'] * 2
        else:
            return ['background-color: white'] * len(s)


@st.experimental_fragment
def frag_table(table_number):
    shares = pd.read_csv("FNO Stocks - All FO Stocks List, Technical Analysis Scanner.csv")
    share_list = list(shares["Symbol"])

    today_year = datetime.datetime.now().year
    exp_date_list = last_thursdays(today_year)
    date_list = []
    today_date = datetime.date.today()
    for i in range(len(exp_date_list)):
        x = (exp_date_list[i].date() - today_date).days
        if x > 0:
            date_list.append(exp_date_list[i].date().strftime('%d-%m-%Y'))
    print(date_list)
    c1, c2 = st.columns(2)
    with c1:
        selected_option = st.selectbox("Share List", share_list, key="share_list" + str(table_number))
    with c2:
        exp_option = st.selectbox("Expiry Date", date_list, key="exp_list" + str(table_number))
        if selected_option in share_list:
            ticker = selected_option
            output_ce, output_pe = get_dataframe(ticker, exp_option)
            ########################################## Stock LTP and Matrix #######################################
            stock_ltp = 0.0
            for price in current_market_price(ticker, exchange):
                stock_ltp = price
                break

        # ********************************** MATRIX ******************************************
        l1, l2 = len(output_ce), len(output_pe)
        if l1 < l2:
            fin_len = l1
        else:
            fin_len = l2
        matrix = np.zeros((fin_len, 4))
        df = pd.DataFrame(matrix, columns=["CE Premium %", "CE (Premium + SP)%", "PE Premium %", "PE (Premium + SP)%"])

        for i in range(len(df)):
            df.at[i, "CE Premium %"] = round((output_ce["lastPrice"].iloc[i] / stock_ltp) * 100, 2)
            df.at[i, "CE (Premium + SP)%"] = round(
                (((output_ce["strikePrice"].iloc[i] - stock_ltp) + output_ce["lastPrice"].iloc[i]) / stock_ltp) * 100,
                2)
            df.at[i, "PE Premium %"] = round((output_pe["lastPrice"].iloc[i] / stock_ltp) * 100, 2)
            df.at[i, "PE (Premium + SP)%"] = round(
                (((stock_ltp - output_pe["strikePrice"].iloc[i]) + output_pe["lastPrice"].iloc[i]) / stock_ltp) * 100,
                2)

        # ************************************************************************************
    col1, col2, col3 = st.columns(3)

    with col1:
        output_ce = output_ce.style.set_properties(**{'background-color': 'palegreen','font-size': '20pt'})
        output_ce = output_ce.format({'lastPrice': "{:.2f}".format, 'strikePrice':"{:.1f}".format})
        st.dataframe(output_ce)
    with col2:
        output_pe = output_pe.style.set_properties(**{'background-color': 'antiquewhite'})
        output_pe = output_pe.format({'lastPrice': "{:.2f}".format, 'strikePrice':"{:.1f}".format})
        st.dataframe(output_pe)
    with col3:
        df = df.style.apply(highlight_ratio, axis=1)
        df = df.format(formatter="{:.2f}".format)
        st.table(df)
    st.write(f'{ticker} LTP:', stock_ltp)


# frag_table(1)
# frag_table(2)
# frag_table(3)


import requests

import requests

# Create a session object
session = requests.Session()

# Make an initial request to capture cookies
response = session.get('https://www.nseindia.com')
print("Initial cookies:", session.cookies.get_dict())

# Use the same session to make further requests
response = session.get('https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY')
data = response.json()
print(data)




