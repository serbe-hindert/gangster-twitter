import random
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



def twitterLogin(driver, username, password):
    driver.get("https://x.com")

    # tackle cookies
    cookieButton = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='BottomBar']"))
    )[-1].find_elements(By.XPATH, ".//button")[-1]
    cookieButton.click()

    driver.get("https://x.com/login")

    # twitter login takes time to spawn in
    nameInput = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.NAME, "text"))
    )
    nameInput.send_keys(username)
    nameInput.send_keys(Keys.RETURN)

    passwordInput = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.NAME, "password"))
    )
    passwordInput.send_keys(password)
    passwordInput.send_keys(Keys.RETURN)

def twitterLetConnect(driver):
    searchInput = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"))
    )
    searchInput.send_keys("#connect")
    searchInput.send_keys(Keys.RETURN)

    newestButton = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.XPATH, "//a[@href='/search?q=%23connect&src=typed_query&f=live']"))
    )
    newestButton.click()

    CONNECT_GREETINGS = [
        "Let's connect!",
        "Hey there, let's connect!",
        "Let's connect 😊",
        "Let's connect",
        "Hi, let's connect!",
        "How about we connect?",
        "Would love to connect with you!",
        "Let's get connected!",
        "Looking forward to connecting with you!",
        "Ready to connect?",
        "Connect with me!",
        "I'd like to connect with you!",
    ]

    while True:
        loadedTweets = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
        )

        random.shuffle(CONNECT_GREETINGS)
        greetingIndex = 0

        for i in range(len(loadedTweets) - 1):
            tweet = loadedTweets[i]

            # check if already following the tweeter
            # twitter acting up sometimes
            try:
                hoverElement = WebDriverWait(tweet, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, ".//div[@data-testid='User-Name']"))
                )
                hoverAction = ActionChains(driver)
            except StaleElementReferenceException:
                continue

            # twitter acting up sometimes
            try:
                hoverAction.move_to_element(hoverElement).perform()
            except:
                driver.execute_script("arguments[0].scrollIntoView(true);", hoverElement)
                WebDriverWait(driver, 10).until(expected_conditions.visibility_of(hoverElement))
                continue

            # man i dont even know how this error can be created
            try:
                followCard = WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, ".//div[@data-testid='HoverCard']"))
                )
            except TimeoutException:
                driver.execute_script("arguments[0].scrollIntoView(true);", hoverElement)
                WebDriverWait(driver, 10).until(expected_conditions.visibility_of(hoverElement))
                continue

            # oops our own tweet is in the search
            try:
                followButton = followCard.find_element(By.XPATH, ".//button")
            except NoSuchElementException:
                driver.execute_script("arguments[0].scrollIntoView(true);", hoverElement)
                WebDriverWait(driver, 10).until(expected_conditions.visibility_of(hoverElement))
                continue

            isConnectable = False
            if (followButton.get_attribute("data-testid").endswith("-follow")):
                print("FOLLOW!! NEU" + followButton.get_attribute("data-testid"))
                isConnectable = True
                driver.execute_script("arguments[0].click();", followButton)

            # move off the hover card
            xIcon = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, ".//a[@href='/home']"))
            )
            ActionChains(driver).move_to_element(xIcon).perform()
            WebDriverWait(driver, 10).until(
                expected_conditions.invisibility_of_element(followCard)
            )

            # scroll this post, which actually scrolls into next post
            driver.execute_script("arguments[0].scrollIntoView(true);", hoverElement)
            WebDriverWait(driver, 10).until(expected_conditions.visibility_of(hoverElement))


            if (isConnectable):
                # like tweet
                sleep(1)
                likeButton = WebDriverWait(tweet, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, ".//button[@data-testid='like']"))
                )
                driver.execute_script("arguments[0].click();", likeButton)

                sleep(1)

                # comment on tweet
                commentButton = tweet.find_element(By.XPATH, ".//button[@data-testid='reply']")
                driver.execute_script("arguments[0].click();", commentButton)

                # shit ass communities make it crash
                try:
                    commentField = WebDriverWait(driver, 10).until(
                        expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, ".notranslate.public-DraftEditor-content"))
                    )
                except TimeoutException:
                    continue
                commentField.send_keys(CONNECT_GREETINGS[greetingIndex])
                if (greetingIndex < len(CONNECT_GREETINGS) - 1):
                    greetingIndex += 1
                else:
                    greetingIndex = 0

                replyButton = WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-testid='tweetButton']"))
                )
                driver.execute_script("arguments[0].click();", replyButton)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)




def main():
    driver = webdriver.Firefox()
    driver.maximize_window()

    try:
        twitterLogin(driver, "AntiG_Fehlinger", "abdulrazackkarimouousame")
        twitterLetConnect(driver)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()