
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from os import rename
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import imaplib
import os
import pygame
import random


account_file = open('Wizard101 Accounts.txt', 'r')  # opens account list
account_list = []
account_num = 0
# Placeholder for account number only put even numbers
answer_num = 0  # Placeholder for answer number
captcha_answer = 0
beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
pygame.mixer.init()
pygame.init()
sounda= pygame.mixer.Sound("toots.wav")
sounda.set_volume(0.1)
count = 0

sounda= pygame.mixer.Sound("toots.wav")
sounda.set_volume(0.1)

for item in account_file:  # Strips the new line character, i think i can remove the for loop, but im too scared to change it
    account_list.append(item.strip('\n'))

trivia_file = open('Trivia Answers.txt', 'r').read().split('\n')  # Opens the Trivia Answer Key
trivia_answers = {}  # Creates the answer dictionary

for item in range(int(len(trivia_file) / 2)):  # Fills the dictionary with poet answers
    trivia_answers[trivia_file[answer_num]] = trivia_file[answer_num + 1].strip("\t")  # Adds the question as key, and value as answer
    answer_num += 2  # Add 2 because you are adding the key and value so you need to go up 2 lines

trivia_links = open('Links.txt', 'r').read().split('\n')  # Creates a list of the trivia links

for account in range(int(len(account_list) / 2)):  # Loops through accounts
    driver = webdriver.Chrome(ChromeDriverManager().install())  # opens chrome
    wait = WebDriverWait(driver, 60)  # Sets wait
    driver.get("https://www.freekigames.com/trivia")  # Opens Crowns Website

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginContainer > a')))
    driver.find_element_by_css_selector('#loginContainer > a').click()  # Clicks the login button

    driver.switch_to.frame(driver.find_element_by_css_selector('#jPopFrame_content'))  # Gets into that juicy iframe
    enter_user = wait.until(EC.element_to_be_clickable((By.ID, 'userName')))
    enter_user.send_keys(account_list[account_num])  # send the username
    account_num += 1

    enter_user = wait.until(EC.element_to_be_clickable((By.ID, 'password')))  # Gets the location of the Password
    enter_user.send_keys(account_list[account_num])  # Enters the password
    account_num += 1

    wait.until(EC.element_to_be_clickable((By.ID, 'bp_login')))
    driver.find_element_by_css_selector('#bp_login').click()  # Clicks the login button

    for link in trivia_links:  # Loops through all 10 quizzes
        driver.get(link)  # Gets the new webpage cause the click isn't working for some reason

        for item in range(12):
            try:
                question = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#quizContainer > div.quizQuestion'))).text  # Waits until you can see the quiz question
                answer = trivia_answers[question]  # Gets the answer from the dictionary
            except:
                missed_questions = open("//filepath", "a")
                missed_questions.write(driver.find_element_by_css_selector('#quizContainer > div.quizQuestion').text + "\n")
                for answers in driver.find_elements_by_css_selector("#quizContainer > div.answersContainer"):
                    missed_questions.write(answers.get_attribute('textContent'))
                missed_questions.close()
                count = 0  # If the answer isn't in the dictionary then it just picks the first check box
                answer = " "  # You need to make a value for answer or else it will throw an error
                pass
            if(link == "https://www.freekigames.com/ninth-grade-vocabulary-trivia" or link == "https://www.freekigames.com/famous-world-leaders" or link == "https://www.freekigames.com/state-capitals-trivia" or link == "https://www.freekigames.com/world-capitals-trivia" or link == "https://www.freekigames.com/famous-poets"):
                answer = " " + answer
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'answerText')))  # Waits for the answer to be visible
            question_answer = driver.find_elements_by_class_name("answerText")

            for _ in range(4):  # For loop that checks if the answer matches the element
                answer_check = question_answer[_]
                answer_check = answer_check.get_attribute('textContent')  # Gets the text from the class
                answer_check = answer_check.strip('\n')  # Removes any blank spaces
                answer_check = "".join([s for s in answer_check.splitlines(True) if s.strip("\r\n")])  # Im not really sure if this is necessary, but it is supposed to remove blank lines from the item. Also I copied it form stack overflow so I have no idea how it works
                if answer_check == answer:
                    count = _  # Gets the position of the checkbox
            
            check_box = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'largecheckbox')))
            check_box = driver.find_elements_by_class_name("largecheckbox")
            check_box[count].click()  # Clicks the correct checkbox
            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#nextQuestion > div')))
                driver.find_element_by_css_selector('#nextQuestion > div').click()
            except:
                continue


        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#quizFormComponent > div.quizContainer > div:nth-child(4) > a'))).click()  # I don't know the purpose of this but im not removing it
        image_path = "//filepath"  # The path where the image is going to be saved
        driver.save_screenshot(image_path)  # Selenium takes a screenshot and saves it to previously stated path
        #send_captcha(image_path)  # Sends the image via gmail
        #captcha_answer = recieve_image(captcha_answer)
        sounda.play()
        captcha_answer = input("Enter le captcha: ")

        driver.switch_to.frame(driver.find_element_by_css_selector('#jPopFrame_content'))  # Gets into that juicy iframe
        captcha_solve = driver.find_element_by_id("captcha")  # Finds the captcha text box
        captcha_solve.send_keys(captcha_answer)  # Puts in the captcha solve that I answered in discord
        driver.find_element_by_css_selector("#bp_login").click()  # Presses ok on the captcha sovle
        log = open("Log.txt", "a")
        log.write(link + " " + driver.find_element_by_class_name("quizScore").text + "\n")
        
            
        try:
            rename(image_path,
                   "//filepath" + captcha_answer + str(account_num * random.randint(1,100)) + ".png")
        except:
            pass
    driver.quit()

