import os
from seleniumbase import SB
from selenium.webdriver.common.keys import Keys
import pandas as pd

with SB(uc=True) as sb:
    # Login
    sb.open("https://publicaccess.courts.oregon.gov/PublicAccessLogin/Login.aspx?ReturnUrl=%2fPublicAccessLogin%2fSearch.aspx%3fID%3d900&ID=900")
    sb.sleep(3)
    