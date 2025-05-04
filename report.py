import os
from seleniumbase import SB
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv

results = []
start = input("Enter start date (e.g. 4/1/2025): ").strip()
end = input("Enter end date (e.g. 5/1/2025): ").strip()

with SB(uc=True) as sb:
    # Login
    sb.open("https://publicaccess.courts.oregon.gov/PublicAccessLogin/Login.aspx?ReturnUrl=%2fPublicAccessLogin%2fSearch.aspx%3fID%3d900&ID=900")
    sb.sleep(3)
    sb.type("input#UserName", "mclmul02")
    sb.type("input#Password", "ztq5hcwq!qLkuQh")
    sb.click('input[name="SignOn"]')
    dropdown = "#sbxControlID2"
    sb.wait_for_element(dropdown)
    options = sb.find_elements(f"{dropdown} option")

    for index, option in enumerate(options[1:], start=1):
        value = option.get_attribute("value")
        text = option.text.strip()
        print(f"{index + 1}: Selecting {text} -> {value}")

        sb.set_value(dropdown, value)

        sb.execute_script('LocationChange(arguments[0])', sb.find_element(dropdown))
        sb.wait_for_element('a.ssSearchHyperlink')
        sb.click_link("Search Court Calendar")
        
        sb.click('select#SearchBy')
        sb.click('select#SearchBy option[value="5"]')

        sb.click('input#chkDtRangeCriminal')
        sb.click('input#chkDtRangeFamily')
        sb.click('input#chkDtRangeProbate')

        sb.type('input#DateSettingOnAfter', start)
        sb.type('input#DateSettingOnBefore', end = "5/1/2025")
        sb.click('input#SearchSubmit')
        sb.sleep(1)

        rows = sb.find_elements("tbody > tr")
        for row in rows:
            tds = row.find_elements("tag name", "td")

            if len(tds) < 4:
                continue  
            last_td_text = tds[-1].text.strip()
            if "Trial - Twelve Person Jury" in last_td_text:
                try:
                    link_element = tds[0].find_element("tag name", "a")
                    case_url = link_element.get_attribute("href")
                    case_number = link_element.text.strip()

                    results.append({
                        "case_number": case_number,
                        "case_url": case_url
                    })
                except Exception as e:
                    print(f"Error parsing row: {e}")
        sb.go_back()
        sb.sleep(1)

csv_file = "jury_trial_cases.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["case_number", "case_url"])
    writer.writeheader()
    writer.writerows(results)

print(f"Saved {len(results)} jury trial cases to {csv_file}")
