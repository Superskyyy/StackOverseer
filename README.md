# StackOverseer
See the titles of the 10 newest User-defined-related questions and the 10 most voted in the past week.

The Q&A monitor:
- StackOverflow disallows accessing any answer-related-content via iFrames or API. So a RSS feed parser would give the best results.

Bonus Feature:

- Data visualization of "User heatmap who asked a Android related question over the past week"
    - This feature is implemented using Leaflet.js
    - This feature is rendered via AJAX call to Django backend static file, ideally a cron-job will scrape the API often.
- Data visualization of "Technologies most related to Android over the past week" 

## Built With


### Technologies 
* [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines.
* [jQuery](https://github.com/jquery/jquery) - jQuery JavaScript Library.
* [Bootstrap](https://github.com/twbs/bootstrap) - The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.
* [Font-Awesome](https://github.com/FortAwesome/Font-Awesome) - The iconic SVG, font, and CSS toolkit.
* [Leaflet](https://github.com/Leaflet/Leaflet) - JavaScript library for mobile-friendly interactive maps.
* [wordcloud2.js](https://github.com/search?q=wordcloud2) - Tag cloud/Wordle presentation on 2D canvas or HTML.
* [Feedparser](https://github.com/kurtmckee/feedparser) - Parse feeds in Python.
* [Docker](https://www.docker.com/) - Docker Engine.
* [Gunicorn](https://pypi.org/project/gunicorn/) - Python Http Server.

### Services

* [Tom Tom](https://developer.tomtom.com/) - A Geocoder API Service.
* [StackExchange API](https://api.stackexchange.com/) - StackExchange API

## TO DO LIST: 

- Cleanup code
- Better Responsive Design



    
### Deploy

Docker - Gunicorn - Tencent Cloud



## This project is Dockerized
#### Configurations
1. Modify settings.py in StackOverseer, make sure docker is set to `True`

- To run the project in pure local env (Not recommended).

- To build the source code in your local Docker
    - The docker container will automatically reflect latest change of source code.
    So don't build again, run ```> docker-compose up ``` instead.
    
    1. Clone the code, make sure docker is running
    2. Make sure the DOCKER Variable is set to True in settings.py
    3. Run following commands
        ```bash
        
        [Windows Git Bash]> winpty docker-compose run web python manage.py createsuperuser
        
        [Unix & Powershell]> docker-compose run web python manage.py createsuperuser
        
        docker-compose build
        
        docker-compose up

        ```



### PyLint
- Pycharm - Preference - Plugin - Marketplace 

- Search for Pylint, Install it and reboot Pycharm.
Pylint will appear as an icon in lower left corner, there's one inside VCS - Commit too.




## Requirements

* [Python 3.7+](https://www.python.org/)
* `python` on the PATH



#### Python path can be found by
  
```  
import sys
      
print("Python EXE : " + sys.executable)
```   

