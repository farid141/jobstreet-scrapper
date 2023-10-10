# jobstreet-scrapper
Scrapping all job posts on jobstreet from given link. The result will be saved on csv file. You can add exclude_keyword and include_keyword to make job scanning in csv easier.

## Environment settings
1. Download webdriver according to your web browser 
2. Add webdriver path to 'path' variable in environment variable settings. You can use this reference https://phoenixnap.com/kb/windows-set-environment-variable

## Python modules
You need to install some python modules using pip command
``` bash
pip install selenium
pip install pandas
```

## Parameter setting
You can modify some parameter in 'constants.py' file to:
- customize jobstreet filters
- customize exclude and include keywords
- customize name of csv file result
