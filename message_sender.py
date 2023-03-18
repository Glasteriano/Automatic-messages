from message_2b_sent import message as std_msg
from message_2b_sent import inter_code as ddi

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as selenium_errors

import time
import pandas as pd
import urllib.parse
from datetime import datetime
#############################################################################################################


how_many_numbers_I_sent, how_many_attempts = 0, 0
max_message_sent = int(input('To how many numbers do you want to send? '))
skipped_rows = int(input("How many rows do you want to skip? "))

start = datetime.now()

contacts_df = pd.read_excel("202802c.xlsx")  # Get the Excel file

browser = webdriver.Firefox()  # Using Firefox to access
browser.get("https://web.whatsapp.com")

while len(browser.find_elements(By.ID, "pane-side")) < 1:  # Waiting untill the pane-side ID appears to indicate I'm logged in
    time.sleep(2)

print('\nI\'m in\n')

time.sleep(15)  # Waiting some time to load everything and do not be so fast
#____________________________________________________________________________________________________________


for index, number in enumerate(contacts_df["Telefone1"], start=(skipped_rows - 1) if skipped_rows > 0 else 0):
    # Just skipping the rows I don't want to send to, while I avoid crash the code with negative indexes 

    area_code = contacts_df["DDD1"][index]  # Getting the area code in every line
    number = contacts_df['Telefone1'][index]  # Getting the right number by its index
    area_code, number = int(area_code), int(number)
    final_msg = urllib.parse.quote(std_msg)  # Transforming the message to be better usable in URLs
    
    print(f'{"#" * 10} Sending to: {area_code, number} {"#" * 10}')

    link = f'https://web.whatsapp.com/send?phone={ddi}{area_code}{number}&text={final_msg}'  # Putting al together in that link
    browser.get(link)

    how_many_attempts += 1

    while len(browser.find_elements(By.ID, "pane-side")) < 1:  # Again, waiting some time to pane-side ID shows up
        time.sleep(2)
    
    time.sleep(15)  # Waiting everything load properly

    previous_message = browser.find_elements(By.CLASS_NAME, '_27K43')
    #________________________________________________________________________________________________________


    if previous_message:  # Checking if I wrote something before
        with open('message_already.txt', 'a') as already_file:
            already_file.write(f'--| {index + 2}: There is something written! - {area_code, number}\n')
            print(f'{"-" * 10} There is something written: {area_code, number} {"-" * 10}\n')

        continue
    #________________________________________________________________________________________________________


    # Using the CSS selector to find the right field, by XPath was not working
    css_button = '#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._2xy_p._3XKXx > button'

    try:  # Trying to send the message

        browser.find_element(By.CSS_SELECTOR, css_button).click()

    except selenium_errors.NoSuchElementException:  # If I don't find the button, a error is raised

        with open('not_exist.txt', 'a') as no_number:  # Writing the number who got the error
            no_number.write(f'--| {index + 2}: Number does not exist! - {area_code, number}\n')
            print(f'{"-" * 10} Number does not exist: {area_code, number} {"-" * 10}\n')

        continue

    print(f'\tMessage sent - {area_code, number}')
    how_many_numbers_I_sent += 1

    print(f'Total sent: {how_many_numbers_I_sent} of {max_message_sent} number(s)\n')
    #________________________________________________________________________________________________________


    with open('successful.txt', 'a') as accomplished:  # Writing the number who successfully got the message
            accomplished.write(f'--| {index + 2}: Messagem sent! - {area_code, number}\n')
    #________________________________________________________________________________________________________


    if how_many_numbers_I_sent >= max_message_sent:  # Limiting how many messages will be sent
        time.sleep(3)
        browser.close()
        break

    time.sleep(10)  # Waiting to go to the next number

end = datetime.now()

print("It's over!")
print(f'Time: {end - start}')
print(f'\nYou sent to {how_many_numbers_I_sent} number(s)')
print(f'You tried {how_many_attempts} number(s)\n')
