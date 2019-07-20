# Import basic files
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


class InstaBot():

    def __init__(self, userID, password):
        self.userID = userID
        self.password = password
        self.ibot = webdriver.Firefox()
    

    # auto sigin using the login information
    def signin(self):
        ibot = self.ibot
        ibot.get('https://www.instagram.com/accounts/login/')

        #wait some time to load the webpage
        time.sleep(3)

        #Get the username and password
        userID = ibot.find_element_by_name('username')
        password = ibot.find_element_by_name('password')

        #clear the garbage value
        userID.clear()
        password.clear()

        #send the data to the instagram and return the webpage
        userID.send_keys(self.userID)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        
        #wait some time and then don't show notification
        time.sleep(4)
        notification_off_button = ibot.find_element_by_xpath('//button[text()= "Not Now"]')
        notification_off_button.click()


    # search for the insta hash tag and return a array of links of the posts or users
    def search_hashtag(self,instahash):
        ibot = self.ibot
        url = 'https://www.instagram.com/explore/tags/'+instahash
        ibot.get(url)
        time.sleep(2)
        posts = ibot.find_elements_by_css_selector("article a")
        return [elem.get_attribute('href')
                    for elem in posts]

    # Like a post on the basis of the hashtag
    def like_post(self, instahash):
        ibot = self.ibot
        likelinks = self.search_hashtag(instahash)


        for link in likelinks:
                ibot.get(link)
                like = ibot.find_element_by_xpath("//span[@aria-label='Like']")
                try:
                    ActionChains(ibot).move_to_element(like).click(like).perform()
                    time.sleep(5)
                except Exception as error:
                    # @todo need to handle the error for the change in the screen size here
                    # not working in the mobile view of the code
                    print(error)
                    time.sleep(10)

    # Follow a person on the basis of the hashtag
    def follow_with_hashtag(self, instahash):
        ibot = self.ibot
        followlinks = self.search_hashtag(instahash)


        for link in followlinks:
                ibot.get(link)
                follow_button = ibot.find_element_by_css_selector('button')
                if(follow_button.text != 'Following'):
                    try:
                        follow_button.click()
                        time.sleep(2)
                    except:
                        time.sleep(10)
    
    # follow a valid username
    # @todo: createa a method to check if the username is valid or not
    def follow_with_username(self, valid_username):
        ibot = self.ibot
        userlink = 'https://www.instagram.com/' + valid_username
        ibot.get(userlink)
        follow_button = ibot.find_element_by_css_selector('button')

        if(follow_button.text != 'Following'):
            try:
                follow_button.click()
                time.sleep(4)
            except:
                time.sleep(10)
        else:
            print('You already follow the user: '+ valid_username)

    
    # Unfollow a user by username
    def unfollow_with_username(self, valid_username):
        ibot = self.ibot
        userlink = 'https://www.instagram.com/' + valid_username
        ibot.get(userlink)
        unfollow_button = ibot.find_element_by_css_selector('button')

        if(unfollow_button.text == 'Following'):
            try:
                unfollow_button.click()
                time.sleep(4)
                confirm_unfollow_button = ibot.find_element_by_xpath('//button[text() = "Unfollow"]')
                confirm_unfollow_button.click()
            except:
                time.sleep(10)
        else:
            print('You donot follow the user : '+ valid_username)

  

    # close browser
    def close_bot(self):
        ibot = self.ibot
        ibot.close()
    
    # close browser upon exit
    def __exit__(self,exc_type,exc_value,traceback):
        ibot = self.ibot
        ibot.close()
    

instabot = InstaBot('email_or_phone','your_password')
instabot.signin()
time.sleep(3)

file_path = 'C/Users/login/OneDrive/Desktop/picture.png'
instabot.unfollow_with_username(file_path)