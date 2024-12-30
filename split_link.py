# Imports
from datetime import datetime

# Split the URL into variables

def set_variables(file_url):
    beginning, auth_token = file_url.split(".m3u8")
    input_m3u8 = beginning.split("/")[-1] + ".m3u8"
    base_url = file_url.split("hls/")[0] + "hls/"

    year, month_num, day = beginning.split("/")[7].split("_")[1:4]
    month_name = datetime.strptime(month_num, "%m").strftime("%B")

    date = f"{year}_{month_name}_{day}"

    return base_url, input_m3u8, auth_token, month_num, date

    '''
    Variable format:

    base_url: 
        https://weverse-rmcnmv.akamaized.net/c/read/v2/VOD_ALPHA/weverse_2024_09_27_0/hls/
    input_m3u8:
        81431ed9-7ce1-11ef-b614-a0369ffb34e8.m3u8
    auth_token:
        ?__gda__=1727469565_976e9cf32cf03c5d016b356062d27dfc
    date:
        {year}_{month_name}_{day}
    '''