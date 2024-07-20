from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Configure Chrome options to ignore SSL certificate errors
options = webdriver.EdgeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')



driver = webdriver.Edge(options=options)

# URL of the main page
url = 'https://hprera.nic.in/PublicDashboard'
driver.get(url)

# Wait for the page to load completely (increase time based on your needs).
time.sleep(20)

# to find the first 6 project elements
p  = driver.find_element(By.XPATH, '//*[@id="reg-Projects"]/div')
projects = p.find_elements(By.CLASS_NAME, 'col-lg-6')[:6]

# List to store project details
project_details_list = []

for index, project in enumerate(projects):
    try:
        # Extract project details
        element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(project.find_element(By.CSS_SELECTOR, 'a[title="View Application"][onclick="tab_project_main_ApplicationPreview($(this));"]'))
            )
        element.click()
        
        # Wait for 3 seconds before accessing the dialogue box
        time.sleep(3)     
         # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Extract GSTIN No, PAN No, Name, Permanent Address
        fields = {}
        fields['RERA'] = element.text.split()[0]
        rows = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
        )

        # Iterate through the rows
        for row in rows:
            # Check if the row contains the desired field texts text: GSTIN No, PAN No, Name, Permanent Address
            columns = row.find_elements(By.TAG_NAME, 'td')
            if columns and columns[0].text.strip() == 'Name':
                name = row.find_element(By.CLASS_NAME, 'fw-600').text.strip()
                print(name)
                fields['Name'] = name

            if columns and columns[0].text.strip() == 'PAN No.':
                pan_no_element = row.find_element(By.TAG_NAME, 'span')
                pan_no = pan_no_element.text.strip()
                print(pan_no)
                fields['PAN No.'] = pan_no
            
            if columns and columns[0].text.strip() == 'GSTIN No.':
                gstin = row.find_element(By.TAG_NAME, 'span').text.strip()
                print(gstin)
                fields['GSTIN No.'] = gstin
            
            if columns and columns[0].text.strip() == 'Permanent Address':
                addr = row.find_element(By.TAG_NAME, 'span').text.strip()
                print(addr)
                fields['Address'] = addr
        
        project_details_list.append(fields)

        time.sleep(3)
        
        close =  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[type="button"][class="close"][data-dismiss="modal"]')))
        close.click()
        
               
        print(f'closing... {element.text.split()}')
        time.sleep(3)

    except Exception as e:
        print(f"Failed to process project {index + 1}: {e}")


print(project_details_list)

driver.quit()

# Create a DataFrame from the list of project details
df = pd.DataFrame(project_details_list)

# Display the DataFrame
print(df)
directory = os.getcwd()
file_name = 'registered_projects.csv'
full_path = os.path.join(directory, file_name)

# Save the DataFrame to the CSV file
try:
    df.to_csv(full_path, index=False)
    print(f"File saved successfully to {full_path}")
except PermissionError:
    print(f"Permission denied: Unable to write to {full_path}")
except Exception as e:
    print(f"An error occurred: {e}")
