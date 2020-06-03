# SocialNetwork

This Social Network Website was made and designed for a project in the COMPSCI 1XA3 Course at McMaster Univerity. The objective of this project is to evaluate my proficieny in using the django framework to make and work with the backend developement of a website. Along side Django, the project also makes use of custorm HTML file (.djhtml), JQuery (JS) AJAX and CSS. 
<br>

## Usage  

- Start By Creating a new django environment with name djangoenv ***(If you don't have one already installed)***<br>
    ```bash
    conda create -n djangoenv python=3.7 
    ```
- The Continue by activating the **Django** environment and Installing **Anaconda** <br>
    ```bash
    conda activate djangoenv
    conda install -c anaconda django
    ```
- Go to the root directory of the project (***Where the **manage.py** python script is***)
- To Run the project on a **local machine** :
    ```bash 
    python manage.py runserver localhost:8000
    ```
- To Run the project on the **mac1xa3 server** :
    ```bash
    python manage.py runserver localhost:10050
    ```
- Login with **User :** ' ' and **Password :** ' '
- All test Users and Password are mentioned under objective #11 
<br>

*************

## Objective 1: Complete Login and SignUp Pages 
### Discription :
- **Login Page:** It is a premade page, part of the project template. It uses the built-in django form AuthenticationFrom. It accepts the username and password by making a POST request. 
- **Signup Page:** The signup button on the login page, redirects the user to a Signup page. The signup pages is made using the built-in Django form, ***'UserCreationForm'*** which is part of ***'django.contrib.auth.forms'***. 
- The function signup_view in ***login/views.py*** has returns ***'signup.djhtml'***, where the form is implemented. 
- ***'signup.djhtml'*** is setup in a way which redirects you to the function ***create_user_view*** in ***login/views.py***, where the form is implemented to create a UserInfo information with the fields ***username*** and ***password***. 

## Objective 2: Adding User Profile and Interests 
### Discription : 
- ***social.djhtml*** renders the ***left_column*** used by all soical templates. 
- So the djhtml file is setup in a way, where it can display all the revalent information about the current user who is authenticated and requesting the current page. 
- It displays attributes relavent to the user which are the feilds based on the ***UserInfo*** models, from ***Project03/social/models.py***

## Objective 3: Account Settings Page
### Discription :
- If the user clicks on the circle avatar on the top right corner, They will be redirected to the account settings page. 
- This view corresponds with the ***account_view*** in ***Project03/social/views.py***. 
- The page shows two sections. The upper sections, allows the user to update their passowrd, and the lower section allows the user to update their user information. 
- The upper section user a ***PasswordChangeForm*** imported from ***django.contrib.auth.forms*** 
- It accepts user input and updates the the password field from the UserInfo object, If the user meets the specified criteria stated by the form. 
### Exceptions:
- The update user form, isn't working. Adding it or trying to use it raises a conflict with the password change form. There are manuale tags present insed the ***account.djhtml*** file. But these do not update the fields.


## Objective 4: Displaying People List
### Discription :
- By clicking on the people icon, present in the left corner of the nav bar, users are redirected to ***people.djhtml***. The middle column displays all the members of the database who are not friends with the current user who is logged in (who is requesting the account.djhtml page). 
- There is also a more button implemented in this page. The button is present under the unknown user card. 
- Clicking the more button shows a new user in the increments of one. This goes on untill all unknown users are showed. 
- each time the more button is pressed, it uses django sessions to calculate the number of times the button has been clicked, and based on the number it shows that many number of user cards. 
### Exception 
- Once all unknown users are displayed the button remains active but is ineffective as there are no more users to display.


## Objective 5: Sending Friend Requests 
### Discription : 
- The friendrequest button on the bottom of the unknown user card, is linked to JQuery events in people.js. 
- Everytime the user clicks the button, the id of the unknown user is sent to people.js and from there it is sent to ***friend_request_view***. 
- There, the user id is parsed to only contain the number and the user id is used to look up the UserInfo object that is corelated to it. 
- user_info is used to store the object of the user requesting the page. 
- Then an if statement checks if the user has sent a friend request before, If yes; it blocks the addition of a new request. Id no it allows the creation of a new ***FriendRequest*** object. 
### Exception:
- Once The request has been sent, the button is still active but no new request will be sent because of the for loop that checks if the object already exists. 


## Objective 6: Accepting / Declining Friend Requests
### Discription :
- The right column of ***people.djhtml*** shows all the fiendrequest the user requesting the page has recieved. 
- Under each request it shows a check or cross mark, representing accept or decline friend request. 
- Each button is set in a way to sent a response to ***people.js***. If the accept button is presset, it sends; "A-{{id of the user who sent the request}}" and if the reject button is pressed; it sends "D-{{id of the user who sent the request}}". 
- The A signifies accept and D signifies Decline. 
- This request is then sent to ***views.accept_decline_view***. The response is parsed and checked if the, first letter is A or D. 
- Using an if loop, if its 'A-" the block adds the both users to each others friend field. 
- And if its a 'D-', the block deletes the particular ***FriendRequest*** object
### Exception:
- Until the user request is accpted from the right column. The user who sent the request still shows up in the Unknown users list for the user requesting the page and he will be able to send a request back as well. Once either of them accept the request; both users are added to each others friend field. 


## Objective 7: Displaying Friends 
### Discription :
- The right column of ***messages.djhtml*** displays all the friends of the current user who is loggin and authenticated. 
- Once the friend request is confirmed, the user user can view their friends under this section of the website.


## Objective 8: Submitting Posts
### Discription :
- The middle section of the ***messages.djhtml*** page display a post making card and under it all the post by all users in the database.
- Similar to the above objectives, there is a post button here that is setup to send back an AJAX request to ***messages.js***. The request contains the text submission of the post.
- The post content is forwarded to ***views.post_submit_view***. A post object is created, adding the user requesting the page, the ***owner*** and the adding the post content to ***content***. 
### Exception
- The post button does not allow multiple line support. If you enter and go to the next line, the post displays the post content on the same line!


## Objective 9: Displaying Post List
### Discription :
- The middle section of the Messages.djhtm page is used to displays all the posts made by all users on the website. 
- Similar to Objective 4, a more button is implemented in the webpage to display more post. The more button works in incriments of 1. Each time it is pressed, one more new post is displayed.
- The post are also sorted in a manner to display the latest post first. 
### Exception:
- Once all the post are made, the more button is still functional. But it doen not show any more posts, as the list of posts is now empty. 


## Objective 10:Liking Posts
### Discription :
- There is sa like button present under every button. 
- The like button is setup in a way where, once it is clicked, it sends the post id to the js file from where it gets forwarded to the ***views.like_view***. 
- The the id is parsed and is used to look up the post. 
- Under the like field of the post, it add s the user name of the user who requested the page. 
- next to the like button, there is another box which shows the current number of likes on the specific post. 
- ***{{p.likes.count}}*** was used to find the number of likes objects in the like field of the particular post
### Exception:
- The button, isn't disabled after the like has been set. But only one like per user is permitted, including one like for the user. Once a user likes a post, the user will not be able to like the post again, even though the button works. 


## Objective 11: Create a Test Database
### Discription :
- There are a set of test users already premade:
- All the users have different username, but they have the same password for simplicity. 
- All users have aready created a couple of posts and have already liked a couple of posts.
    - Username : TestUser ; Password : mac1xa33
    - Username : Sam ; Password : mac1xa33
    - Username : Frodo ; Password : mac1xa33
    - Username : Pippen ; Password : mac1xa33
    - Username : Merry ; Password : mac1xa33
    - Username : Aragon ; Password : mac1xa33
    - Username : Gandalf ; Password : mac1xa33
    - Username : Gimli ; Password : mac1xa33
    - Username : Boromir ; Password : mac1xa33
    - Username : TestUser2 ; Password : mac1xa33
## Exceptions
- All users have already liked a few of the posts, so the like button might not work on a few posts since it is already liked. 
- TestUser2 is the only test user who hasn't made any friends and hasn't made or liked any posts 
- All the fields of the user are unspecified, as the second half of objective 3 (adding user fields) is not functional. 

