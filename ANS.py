#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import random
import matplotlib.pyplot as plt
import time
from IPython.display import display, HTML, Image,clear_output
import ipywidgets as widgets
import requests
from bs4 import BeautifulSoup
import json
from matplotlib.pyplot import figure
from jupyter_ui_poll import ui_events


# In[14]:


random.seed(1)
patterns = {3:4,
            6:7,
            9:8,
            10:9,
            }


# In[15]:


multiplier = [2,3,4,5]
list_of_value = [3,6,9,10]


# In[16]:


def register_btn_event(btn):
    '''
    This Function set up the button for it to work properly
    '''
    event_info['type'] = "button click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return
    


# In[17]:


def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):    
    start_wait = time.time()

    # set event info to be empty
    # as this is dict we can change entries
    # directly without using
    # the global keyword
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            # process UI events
            ui_poll(n_proc)

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            # add pause before looping
            # to check events again
            time.sleep(interval)
    
    # return event description after wait ends
    # will be set to empty string '' if no event occured
    return event_info


# In[18]:


def send_to_google_form(data_dict, form_url):
    ''' Helper function to upload information to a corresponding google form 
        You are not expected to follow the code within this function!
    '''
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok


# In[19]:


def pattern_generation(pattern,multiplier, value_list):
    """
    This function generates pattern for the ANS test
    
    The test can be customized depending on: 
    
    pattern: a dictionary of int ratio between number of dots
    
    multiplier: list of int you wish to multiply by the ratio...
    will be assigned randomly during the test, or changed specifically for each ratio

    value_list: list of int values that fits into keys of the pattern
    
    """
    random_val_num = random.randrange(len(value_list))
    random_value = value_list[random_val_num] 

    if random_value == 3:
        multiplier = [3,4,5]
    elif random_value == 6:
        multiplier = [2,3]
    elif random_value == 9:
        multiplier = [1]
    elif random_value == 10:
        multiplier = [1,2]
    
    random_mul_num = random.randrange(len(multiplier))
    random_multiplier = multiplier[random_mul_num]
    
    final_num_1 = random_value*random_multiplier
    #print(f'There are {final_num_1} blue dots!')
    
    final_num_2 = pattern[random_value]*random_multiplier
    #print(f'There are {final_num_2} red dots!')

    return final_num_1, final_num_2
    



# In[1]:


event_info = {
    'type': '',
    'description': '',
    'time': -1
}

def plot_ANS_test(num1,num2,color1,color2):
    """
    
    This function plot ANS test in a way of scatter plot

    num1: int number of scatter generated with color1

    num2: int number of scatter generated with color2

    color1(str):color corresponding to num1 of scatter

    color2(str):color corresponding to num2 of scatter

    you can customize your color, in my test i used blue and red

    the num1 and num2 can also fit to other function that generates random number to produce ANS test you want.
    
    """
    x1 = np.random.randn(num1)
    y1 = np.random.randn(num1)
    x2 = np.random.randn(num2)
    y2 = np.random.randn(num2)
    fig = plt.figure(figsize=(6, 6))
    
    plt.axis('off')
    plt.scatter(x1,y1, c = [color1])
    plt.scatter(x2,y2, c = [color2])
    
    if num1 > num2:
        #print(f'There are more {color1} dots than {color2}.')
        test = True
    elif num2 > num1:
        #print(f'There are more {color2} dots than {color1}.')
        test = False
    else:
        print('There is an issue occuring in the system!')
    
    display(fig)
    time.sleep(1.25)
    clear_output(wait = False)
    plt.close(fig)
    start_time = time.time()

    #button UI interface
    
    btn1 = widgets.Button(description = "blue")
    btn1.style.button_color = "lightblue"
    btn2 = widgets.Button(description = "red")
    btn2.style.button_color = "red"
    
    btn1.on_click(register_btn_event)
    btn2.on_click(register_btn_event)
    
    panel = widgets.HBox([btn1, btn2])
    
    html_out = HTML('<h1>Which color has more dots?</h1>')
    display(html_out)
    
    display(panel)
    result = wait_for_event(timeout = 3)
    

    while test == True:
        if result['description'] == color1 :
            score = 1
            clear_output(wait=False)
            #print('You are correct!')
        
        elif result['description'] =='':
            html_timeout = HTML('<h1>No button was pressed! Answer more quickly!</h1>')
            display(html_timeout)
    
            time.sleep(1)
            
            clear_output(wait = True)
            score = 0
            time_taken = 'overtime'
            clear_output(wait=True)
            return score, time_taken
        else:
            score = 0
            clear_output(wait=False)
            #print('You are wrong!')
        break
        
    
    while test == False:
        if result['description'] == color2 :
            score = 1
            clear_output(wait=False)
            #print('You are correct!')
        
        elif result['description'] =='':
            score = 0
            html_timeout = HTML('<h1>No button was pressed! Answer more quickly!</h1>')
            display(html_timeout)

            time.sleep(1)
            
            clear_output(wait = False)
            time_taken = 'overtime'
            return score, time_taken

        else:
            score = 0
            clear_output(wait=False)
            #print('You are wrong！')
        break
        
    end_time = time.time()
    time_taken = result['time'] - start_time
    
    #if time_taken > time_limit:
        #score = 0
       # print(f'you have taken too long!(Try to respond in {time_limit} seconds!)')
        #if the user took too long when responding, do not take that into account
    
    return score, time_taken


# In[2]:


def Full_ANS_test(numoftrial):
    """

    This runs the test by combination of previous functions.

    you can customize the number of trial you want to take

    the ideal number of trial for my project is 64, so I used 64.
    
    """
    data_consent_info = """DATA CONSENT INFORMATION:

    Please read:
    
    we wish to record your response data
    
    to an anonymised public data repository.
    
    Your data will be used for educational teaching purposes
    
    practising data analysis and visualisation.
    
    Please type yes in the box below if you consent to the upload."""
    
    print(data_consent_info)
    
    result = input("> ")
    
    if result == "yes":
    
        print("Thanks for your participation.")
        
        print("Please contact philip.lewis@ucl.ac.uk")
        
        print("If you have any questions or concerns")
        
        print("regarding the stored results.")
        
    else:
        
        # end code execution by raising an exception
        
        raise(Exception("User did not consent to continue test."))
        
    clear_output(wait = True)
    
    variation = True
    variation_trigger = [0,1]
    random_var_num = random.randrange(len(variation_trigger))
    total_score = 0
    total_time_taken = 0
    blu_num = 0
    red_num = 0
    test_id = 0
    id_instructions = """

    Enter your anonymised ID
    
    To generate an anonymous 4-letter unique user identifier please enter:
    
    - two letters based on the initials (first and last name) of a childhood friend
    
    - two letters based on the initials (first and last name) of a favourite actor / actress
    
    e.g. if your friend was called Charlie Brown and film star was Tom Cruise
    
    then your unique identifer would be CBTC
    
    """

    print(id_instructions)
    print('Please enter your userid:')
    userid = input('>')
    clear_output(wait = True)

    
    print("User entered id:", userid)
    print('How old are you?')
    print('Enter your answer as a number')
    age = input('>')
    print('What is your profession?')
    profession = input('>')
    data_dict = {
        'Userid': userid,
        'age':age,
        'profession':profession
    }
    ans = []
    clear_output(wait = True)

    print('The test is consist of an plot with different number of blue dots and red dots')
    time.sleep(2.5)
    
    clear_output(wait = True)
    
    print('Your task is to identify which color has more.')
    time.sleep(2.5)

    clear_output(wait = True)
    
    print('You can answer the question by clicking on corresponding buttons, make sure you answer within 3 seconds\nor buttons will disappear')
    time.sleep(2.5)
    clear_output(wait = True)
        
 
    
    
    
    print('The Test will start in 3')
    time.sleep(1)
    clear_output(wait = True)
    print('The Test will start in 2')
    time.sleep(1)
    clear_output(wait = True)
    print('The Test will start in 1')
    time.sleep(1)
    clear_output(wait = True)
    time.sleep(1)




    if random_var_num == 1 :
        
        for i in range(1,numoftrial+1):
            
            blu_num, red_num = pattern_generation(patterns,multiplier, list_of_value)
            score, time_taken = plot_ANS_test(blu_num,red_num,'blue','red')

            total_score += score
            if time_taken == float:
                total_time_taken += time_taken
            test_id = test_id + 1
            ans.append(f'{score}, {test_id}, {time_taken}, {blu_num}, {red_num}')
            data_dict[str(i)] = ans[-1]
            

            
            time.sleep(1.5)
    elif random_var_num == 0 :
        
        for i in range(1,numoftrial+1):
            
            red_num,blu_num = pattern_generation(patterns,multiplier, list_of_value)
            score, time_taken = plot_ANS_test(red_num,blu_num,'red','blue')

            total_score += score
            
            if time_taken == float:
                total_time_taken += time_taken
            test_id+=1
            ans.append(f'{score}, {test_id}, {time_taken}, {blu_num}, {red_num}')
            data_dict[str(i)] = ans[-1]
            

            time.sleep(1.5)
    #print(total_time_taken)
    #print(total_score)
    #print(ans)
    #print(data_dict)
    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLScu7e3Ky-ue5pjFxBri526nsoeeacsWfDec5hady-zTFGJsbw/viewform'
    send_to_google_form(data_dict, form_url)
    return total_time_taken, total_score
   


# In[12]:


#Test start HERE!!!!!!!!!!!!!!!!!!!!!#

#total_time, total_score = Full_ANS_test(64)


# In[ ]:


# remember to add time for user to response
#clear after each time user answer a question at start
#might be too difficult


# In[9]:





# In[ ]:




