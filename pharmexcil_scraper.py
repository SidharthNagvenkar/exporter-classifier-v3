from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup headless Chrome browser
options = Options()
# comment out next line if you want to see browser
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://pharmexcil.com/members_directory.php"
driver.get(url)

# Wait for table to load
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "table")]/tbody'))
    )
except Exception as e:
    print("Table not found:", e)
    driver.save_screenshot("pharmexcil_error_screenshot.png")
    driver.quit()
    exit()

# Parse table
rows = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr')
print(f"Found {len(rows)} rows")

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 6:
        data.append({
            "Company Name": cols[0].text.strip(),
            "Address": cols[1].text.strip(),
            "Contact Person": cols[2].text.strip(),
            "Email": cols[3].text.strip(),
            "Phone": cols[4].text.strip(),
            "Membership Type": cols[5].text.strip()
        })

driver.quit()

# Save to Excel
df = pd.DataFrame(data)
df.to_excel("pharmexcil_members.xlsx", index=False)
print("✅ Data saved to pharmexcil_members.xlsx")
