from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
import pyautogui
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
import pygame
from customtkinter import *
from PIL import Image

# Define color codes using ANSI escape sequences
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

pygame.mixer.init()

audio_file = "resource/beep.mp3"
sound = pygame.mixer.Sound(audio_file)

app = CTk()

app.geometry("600x680")
app.resizable(0, 0)

side_img_data = Image.open("resource/side-img2.png")
side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 680))

email_icon_data = Image.open("resource/email-icon.png")
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))

password_icon_data = Image.open("resource/password-icon.png")
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=680, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Selection Automator", text_color="#601E88", anchor="w", justify="left",
         font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Provide Account Credentials", text_color="#7E7E7E", anchor="w", justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14),
         image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
email_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                       text_color="#000000")
email_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left",
         font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
pass_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                      text_color="#000000", show="*")
pass_entry.pack(anchor="w", padx=(25, 0))

checkbox_frame = CTkFrame(master=frame, fg_color="#ffffff")
checkbox_frame.pack(anchor="w", padx=(25, 0), pady=(10, 0))

checkbox_titles = ["reading", "listening", "writing", "speaking"]
checkbox_vars = []

for i, title in enumerate(checkbox_titles):
    var = StringVar(value="off")
    checkbox = CTkCheckBox(master=checkbox_frame, border_color="#601E88", border_width=1.5, text=title,
                           variable=var, onvalue="on", offvalue="off")
    checkbox.grid(row=i // 2, column=i % 2, padx=10, pady=5, sticky="w")
    checkbox_vars.append(var)

CTkLabel(master=frame, text="Website url :", text_color="#601E88", anchor="w", justify="left",
         font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
url_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                     text_color="#000000")
url_entry.pack(anchor="w", padx=(25, 0))

def switch_event():
    print("switch toggled, current value:", switch_var.get())

switch_var = StringVar(value="on")
sound_toggle = CTkSwitch(master=frame, text="Play Sound on Course Selection", text_color="#601E88", fg_color="#601E88",
                         font=("Arial Bold", 10), command=switch_event, variable=switch_var, onvalue="on",
                         offvalue="off")
sound_toggle.pack(anchor="w", pady=(5, 0), padx=(25, 0))

def find_button(driver):
    while True:
        try:
            button = WebDriverWait(driver, 0.35).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@id, "btn-") and contains(@class, "icon-double-arrow-right")]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            print(f"{bcolors.OKGREEN}Module button Found{bcolors.ENDC}")
            return button
        except TimeoutException:
            print(f"{bcolors.FAIL}Module Button Not Found, retrying...{bcolors.ENDC}")
            time.sleep(1)  #add a short sleep to avoid hammering the server with requests
            driver.get(url_entry.get())
            driver.refresh()


def check_element_presence(driver, class_name, timeout=0.5):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        # print(f"{bcolors.OKCYAN}Element with class {class_name} found{bcolors.ENDC}")
        return True
    except TimeoutException:
        # print(f"{bcolors.FAIL}Element with class {class_name} not found within {timeout} seconds{bcolors.ENDC}")
        return False
    
def button_callback():

    checkbox_labels = [" reading ", " listening ", " writing ", " speaking "]

    email = email_entry.get()
    password = pass_entry.get()

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url_entry.get())

    #10s time dealy for accept the cookies.
    time.sleep(random.uniform(9, 10))
 
    #return the [reading, listening, writing, speaking] from UI
    checkbox_statuses = [var.get() == 'on' for var in checkbox_vars]
    checkBoxData = {' reading ': checkbox_statuses[0], ' listening ': checkbox_statuses[1], ' writing ': checkbox_statuses[2],' speaking ': checkbox_statuses[3]}

    #main.
    while True:
        try:
            #it's wait for the button to be present
            button = find_button(driver)

            #once we find the button click it.
            #before clicking the button. it should be visible on the screen.
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
        
            # Scroll the button into view before interacting with it
            actions = ActionChains(driver)
            actions.move_to_element(button).perform()
            button.click()
            print(f"{bcolors.OKBLUE}Module Button Clicked{bcolors.ENDC}")

            #to check if the module page is worked.()
            if check_element_presence(driver, 'cs-checkout-page__main'):
                print(f'{bcolors.OKGREEN}Page Load Sucessfully!{bcolors.ENDC}') 
                if switch_var.get() == "on":
                    sound.play()
                    sound.play(loops=5)
                break
            else:
                print(f"{bcolors.FAIL},Page in High Demand, refreshing page...{bcolors.ENDC}")
                driver.get(url_entry.get())
                continue
        except Exception as e:
            print(f"{bcolors.FAIL}An error occurred: {e}{bcolors.ENDC}")
            driver.get(url_entry.get())
            continue

    #checkbox.
    for label in checkbox_labels:
        #currentcheckdata is the true/false value given by the user.
        userTickData = checkBoxData[label]

        try:
            # #find  the checkbox.
            checkbox = WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'label.cs-checkbox__label.cs-checkbox__label--exam[for="{label}"]'))
            )

            #check is psudo ::after is present or not
            isTicked = driver.execute_script("""
            var element = arguments[0];
            var after = window.getComputedStyle(element, '::after');
            return after.getPropertyValue('content') !== 'none';
            """, checkbox)

            runButtonClick = False

            if isTicked:
                #element already ticked.
                # print(label, 'is already ticked!')
                if userTickData == True:
                    #do nothing, because it's already ticked.
                    print(f'{bcolors.OKGREEN}{label} is Ticked {bcolors.ENDC}')
                else:   
                    #if user Set it to False, then
                    #click it, to disable it. because it's already ticked.
                    runButtonClick = True
            else:
                #element not ticked
                # print(label, 'is not ticked!')
                if userTickData == True:
                    #click to enable it, because it's already not clicked
                    runButtonClick = True
                    print(f'{bcolors.OKGREEN}{label} is Ticked {bcolors.ENDC}')
                else:
                    #do nothing.
                    print('')

            if(runButtonClick):
                # print(f'{label} Ticked')
                driver.execute_script("""
                var checkbox = arguments[0];
                var clickEvent = new MouseEvent('click', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true
                });
                checkbox.dispatchEvent(clickEvent);
                    """, checkbox)

            runButtonClick = False

        except TimeoutException:
            print(f"{label.capitalize()} checkbox not found")  

    #submit after checkbox.
    try:
        newbutton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.cs-button.cs-button--arrow_next'))
        )
        print(f"{bcolors.OKBLUE}Next button Clicked{bcolors.ENDC}")
        driver.execute_script("arguments[0].click();", newbutton)
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred while finding or clicking the next button: {e}{bcolors.ENDC}")
        try:
            print(f"{bcolors.WARNING}Reloading the page...{bcolors.ENDC}")
            driver.refresh()
        except Exception as e:
            print(f"{bcolors.FAIL}Failed to reload the page: {e}{bcolors.ENDC}")

    #selecting book fro me button.
    try:
        parent_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cs-layer__button-wrapper'))
        )
        # Find all buttons within the parent div
        buttons = parent_div.find_elements(By.TAG_NAME, 'button')
        # Get the second button
        second_button = buttons[1]
        # Scroll the second button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", second_button)
        print(f"{bcolors.OKBLUE}'Book For Me' Button Clicked {bcolors.ENDC}")

        try:
            second_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", second_button)
    except TimeoutException:
        print(f"{bcolors.FAIL}High priority button not found{bcolors.ENDC}")
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", button)
        print(f"{bcolors.OKGREEN}High priority button clicked via JavaScript{bcolors.ENDC}")

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_input.send_keys(email)
        print(f"{bcolors.OKGREEN}Entered Email ID {email} {bcolors.ENDC}")
    except TimeoutException:
        print(f"{bcolors.FAIL}Timeout occurred while waiting for the email input field to be present.{bcolors.ENDC}")
    except NoSuchElementException:
        print(f"{bcolors.FAIL}The email input field with ID 'username' was not found.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An unexpected error occurred: {e}{bcolors.ENDC}")

    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.send_keys(password)
        print(f"{bcolors.OKGREEN}Entered Password  {password} {bcolors.ENDC}")
    except TimeoutException:
        print(f"{bcolors.FAIL}Timeout occurred while waiting for the password input field to be present.{bcolors.ENDC}")
    except NoSuchElementException:
        print(f"{bcolors.FAIL}The password input field with ID 'password' was not found.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An unexpected error occurred: {e}{bcolors.ENDC}")

    try:
        newbutton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn.submit.arrow.right'))
        )

        print(f"{bcolors.OKBLUE}Submit Email and Password{bcolors.ENDC}")
        driver.execute_script("arguments[0].click();", newbutton)
    except TimeoutException:
        print(f"{bcolors.FAIL}Timeout occurred while waiting for the button to be present.{bcolors.ENDC}")
    except NoSuchElementException:
        print(f"{bcolors.FAIL}The button with the specified CSS selector was not found.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An unexpected error occurred: {e}{bcolors.ENDC}")

    try:
        # Wait for the button to be present and store it in a variable
        newbutton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.cs-button.cs-button--arrow_next'))
        )
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", newbutton)
        driver.execute_script("arguments[0].click();", newbutton)
        print(f"{bcolors.OKBLUE}Final confirmation{bcolors.ENDC}")
    except TimeoutException:
        print(f"{bcolors.FAIL}Timeout occurred while waiting for the button to be present.{bcolors.ENDC}")
    except NoSuchElementException:
        print(f"{bcolors.FAIL}The button with the specified CSS selector was not found.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An unexpected error occurred: {e}{bcolors.ENDC}")

    try:
        # Navigate to a webpage
        # Perform actions...
        # Wait for user confirmation before quitting the browser
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")

startButton = CTkButton(master=frame, text="Start", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
                        text_color="#ffffff", width=225, command=button_callback)
startButton.pack(anchor="w", pady=(40, 0), padx=(25, 0))

app.mainloop()