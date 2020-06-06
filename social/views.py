from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

from . import models

def messages_view(request):
    """Private Page Only an Authorized User Can View, renders messages page
       Displays all posts and friends, also allows user to make new posts and like posts
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render private.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        ufriends = list(user_info.friends.all())
        
        
        posts = list(models.Post.objects.all().order_by('-timestamp'))
        likec = []
        
        posts = posts[:(request.session.get('count',1))]
        context = { 'user_info' : user_info,
                    'ufriends': ufriends
                  , 'posts' : posts,
                    'c' : likec } 
        return render(request,'messages.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def account_view(request):
    """Private Page Only an Authorized User Can View, allows user to update
       their account information (i.e UserInfo fields), including changing
       their password
    Parameters
    ---------
      request: (HttpRequest) should be either a GET or POST
    Returns
    --------
      out: (HttpResponse)
                 GET - if user is authenticated, will render account.djhtml
                 POST - handle form submissions for changing password, or User Info
                        (if handled in this view)
    """
    if request.user.is_authenticated:
        pass_change_form = PasswordChangeForm(request)

        # TODO Objective 3: Create Forms and Handle POST to Update UserInfo / Password

        user_info = models.UserInfo.objects.get(user=request.user)
        interest_list = list(user_info.interests.all())
        if len(interest_list) == 0:
            interest_list = [1,2,3,4,5]
        if user_info.birthday is not None:
            render_birthday = dt.datetime.strftime(user_info.birthday, "%Y-%m-%d")
        else:
            render_birthday = "0001-01-01"
        context = {'user_info': user_info,
                   'pass_change_form': pass_change_form,
                   'fields': ["Employment", "Location", "Birthday", "Interests"],
                   'render_birthday': render_birthday,
                   'interest_list': interest_list}
        return render(request, 'account.djhtml', context)

    request.session['failed'] = True
    return redirect('login:login_view')

def info_update_view(request):
    user_info = models.UserInfo.objects.get(user=request.user)
    if request.method == 'POST':
        employment = request.POST.get('Employment', 'Unspecified')
        location = request.POST.get('Location', 'Unspecified')
        birthday = request.POST.get('Birthday', '0001-01-01')
        interest = request.POST.get('Interests', models.Interest('No Interest'))

        if type(interest) == str and interest != '':
            interest = models.Interest(label=f"{interest}")
            interest.save(using='default')
            user_info.interests.add(interest)

        if birthday == '':
            birthday = '0001-01-01'

        if type(birthday) == str and birthday != '0001-01-01':
            birthday = dt.datetime.strptime(birthday,'%Y-%m-%d')
            birthday = birthday.date().strftime('%Y-%m-%d')
            user_info.birthday = birthday

        user_info.employment = employment
        user_info.location = location
        user_info.save(using='default')
    return redirect('social:account_view')


def people_view(request):
    """Private Page Only an Authorized User Can View, renders people page
       Displays all users who are not friends of the current user and friend requests
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render people.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        user_friends = user_info.friends.all()
        all_people = list(models.UserInfo.objects.all())
        not_myself = all_people.remove(user_info)
        only_strangers = [x for x in all_people if x not in user_friends]
        only_strangers = only_strangers[:(request.session.get('counter',1))]


        # TODO Objective 5: create a list of all friend requests to current user
        friend_requests = list(models.FriendRequest.objects.all())
        frcount = True

        context = { 'user_info' : user_info,
                    'all_people' : all_people,
                    'user_friends' : user_friends,
                    'only_strangers' : only_strangers,
                    'friend_requests' : friend_requests,
                    'frcount' : frcount}


        return render(request,'people.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def like_view(request):
    '''Handles POST Request recieved from clicking Like button in messages.djhtml,
       sent by messages.js, by updating the corrresponding entry in the Post Model
       by adding user to its likes field
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postID,
                                a string of format post-n where n is an id in the
                                Post model

	Returns
	-------
   	  out : (HttpResponse) - queries the Post model for the corresponding postID, and
                             adds the current user to the likes attribute, then returns
                             an empty HttpResponse, 404 if any error occurs
    '''
    postIDReq = request.POST.get('postID')
    if postIDReq is not None:
        # remove 'post-' from postID and convert to int
        postID = int(postIDReq[5:])

        if request.user.is_authenticated:
            # TODO Objective 10: update Post model entry to add user to likes field
            post = models.Post.objects.get(id=postID)
            user_info = models.UserInfo.objects.get(user=request.user)
            post.likes.add(user_info)

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('like_view called without postID in POST')

def post_submit_view(request):
    '''Handles POST Request recieved from submitting a post in messages.djhtml by adding an entry
       to the Post Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postContent, a string of content

	Returns
	-------
   	  out : (HttpResponse) - after adding a new entry to the POST model, returns an empty HttpResponse,
                             or 404 if any error occurs
    '''
    postContent = request.POST.get('postContent')
    if postContent is not None:
        if request.user.is_authenticated:
            user_info = models.UserInfo.objects.get(user=request.user)
            postr = models.Post.objects.create(owner=user_info, content=postContent)

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('post_submit_view called without postContent in POST')

def more_post_view(request):
    '''Handles POST Request requesting to increase the amount of Post's displayed in messages.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST

	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating hte num_posts sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of posts dispalyed

        # TODO Objective 9: update how many posts are displayed/returned by messages_view
        # update the # of people dispalyed
        j = request.session.get('count',1)
        request.session['count'] = j+1

        # return status='success'
        return HttpResponse(j)

    return redirect('login:login_view')

def more_ppl_view(request):
    '''Handles POST Request requesting to increase the amount of People displayed in people.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST

	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating the num ppl sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of people dispalyed
        i = request.session.get('counter',1)
        request.session['counter'] = i+1

        # return status='success'
        return HttpResponse(i)

    return redirect('login:login_view')

def friend_request_view(request):
    '''Handles POST Request recieved from clicking Friend Request button in people.djhtml,
       sent by people.js, by adding an entry to the FriendRequest Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute frID,
                                a string of format fr-name where name is a valid username

	Returns
	-------
   	  out : (HttpResponse) - adds an etnry to the FriendRequest Model, then returns
                             an empty HttpResponse, 404 if POST data doesn't contain frID
    '''
    frID = request.POST.get('frID')
    if frID is not None:
        # remove 'fr-' from frID
        username = frID[3:]

        if request.user.is_authenticated:
            all_people = list(models.UserInfo.objects.all())
            user_info = models.UserInfo.objects.get(user=request.user)
            user_req = models.UserInfo.objects.get(user_id=username)
            fv = list(models.FriendRequest.objects.all())
            counter = 0
            for frr in fv:
                if frr.to_user == user_req:
                    if frr.from_user != user_info:
                       counter = 0
                    else :
                        counter =+ 1
            if counter <= 0 :
                friendr = models.FriendRequest.objects.create(to_user=user_req, from_user=user_info)
                friendr.save()
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('friend_request_view called without frID in POST')

def accept_decline_view(request):
    '''Handles POST Request recieved from accepting or declining a friend request in people.djhtml,
       sent by people.js, deletes corresponding FriendRequest entry and adds to users friends relation
       if accepted
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute decision,
                                a string of format A-name or D-name where name is
                                a valid username (the user who sent the request)

	Returns
	-------
   	  out : (HttpResponse) - deletes entry to FriendRequest table, appends friends in UserInfo Models,
                             then returns an empty HttpResponse, 404 if POST data doesn't contain decision
    '''
    data = request.POST.get('decision')
    if data is not None:
        ans = data[:2]
        username = data[2:]

        if request.user.is_authenticated:
            user_info = models.UserInfo.objects.get(user=request.user)  
            user_fr = models.UserInfo.objects.get(user=username) 
            instance = models.FriendRequest.objects.filter(to_user=user_info, from_user=user_fr)
            if ans[:2] == "A-":                                                                             
                user_info.friends.add(user_fr)
                user_fr.friends.add(user_info)  
                instance.delete()   
            else:  
                instance.delete()
                
                # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('accept-decline-view called without decision in POST')
