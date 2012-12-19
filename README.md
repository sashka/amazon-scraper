Amazon-scraper
==============

Installation
------------

First, install dependencies. This is how to do it on clean Ubuntu Precise:

    sudo apt-get update
    sudo apt-get install git python-dev libxml2-dev libxslt1-dev

    git clone git@github.com:svetlyak40wt/amazon-scraper.git
    # if it says: Permission denied (publickey)
    # then you need to generate a private/public ssh keys and
    # put public key to GitHub: https://github.com/settings/ssh

    # skip this step if git was able to clone repository
    ssh-keygen
    # answer default to all questions
    cat ~/.ssh/id_rsa.pub

    cd amazon-scraper

Next, create a virtual environment:

    python virtualenv.py env
    env/bin/pip install -r requrements.txt

Execution
---------
    
    # generate a proxies list
    python env/src/scrapy-proxynova/scrapy_proxynova/proxies.py ru 1 20 proxies.txt
    # run scraper
    env/bin/scrapy crawl amazon -o data.json -t json
