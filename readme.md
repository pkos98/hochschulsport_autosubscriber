# hochschulsport_autosubscriber
This is a little script which automates the registration & subscription process 
of the hochschulsport @ Augsburg.

_Usage:_
```
usage: main.py [-h] [-c COURSE COURSE COURSE] [-l] [-o LIST_OFFERS] [-i]
               [--headless]
```

_Dependencies:_
* Python 3:
    * requests
    * selenium (chromium or firefox webdriver)
    * BeautifulSoup4

_Currently not implemented:_
* Subscribe to a course using an existing account