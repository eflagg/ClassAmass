ClassAmass
--------

**Description**

ClassAmass gives users one place to easily search for online courses among tens of thousands of offerings on Coursera and Udemy. Users can filter their searches based on several parameters. Users can also create a personal profile in order to conveniently track their learning, including courses in which they're currently enrolled, courses they might like to take in the future, and courses they've already completed.

**How it works**

I seeded my PostgreSQL databsase by making API calls to both Coursera and Udemy. I then had to merge the different courses I was recieving into one data model which I built to accomodate courses from both sites. 

Users input a search term which is sent to the Flask server where a SQLAlchemy query is made to the PostgreSQL database. The user can then select from the filters on the side navagation bar to indicate a price, language, whether the course is instructor- or self- led, the specific university sponsoring the course, and which site hosts the course.

### Screenshot

**Homepage**

<img src="/static/ClassAmass.png">

**Search Results**

<img src="/static/ClassAmass_search.png">

**Filtered Search Results**

<img src="/static/ClassAmass_search.png">

**User Profile Page-- Currently Enrolled and Favorited**

<img src="/static/ClassAmass_profile.png">

**User Profile Page-- Past Courses**

<img src="/static/ClassAmass_profile2.png">


### Technology Stack

**Application:** Python, Flask, Jinja, SQLAlchemy, PostgreSQL    
**APIs:** Coursera Courses, Coursera Partners, Udemy  
**Front-End**: JavaScript, HTML/CSS, Bootstrap, JQuery, AJAX, JSON


### Testing Coverage

<img src="/static/ClassAmass_tests.png">


### How to run ClassAmass locally


Create a virtual environment 

```
> virtualenv env
> source env/bin/activate
```

Install the dependencies

```
> pip install -r requirements.txt
```

In a new Terminal run App

```
> python server.py
```


Open your browser and navigate to 

```
http://localhost:5000/
```


### About the Developer    
Emily Flagg  
[Linkedin](https://www.linkedin.com/in/emilyflagg)    