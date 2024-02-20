# AutoLogin
Selenium script for checking website login info.  
The automation isn't detected by websites. Proxy usage is available for anonymity.

## Dependencies
Install Google Chrome and Chromedriver from https://googlechromelabs.github.io/chrome-for-testing

To install the dependencies run
```bash
pip install selenium
pip install selenium-wire
```

## How to use
1) Add the path to your webdriver (line 14) and Chrome folder (line 18). 
2) Put your login info into the [logs.txt](logs.txt).
3) To use proxies, put your proxy addresses into the [socks.txt](socks.txt) file. Otherwise, delete *seleniumwire_options* variable from the code.
4) Enter your target website on lines 76, 120 instead of *https://www.yorsite.com/*.
5) Change names, IDs, XPATHes of the elements by the names, IDs, XPATHes from your target website code (lines 78, 82, 94, 95, 101, 105, 107, 108, 118).
6) Run the script.
7) Example of the **output.txt**:  
login1 password1:VALID!!!  
login2 password2:Incorrect log pass  
login3 password3:Need to check again
