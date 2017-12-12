# Gettitle  
  
A Python 3 script depends on PhantomJS to grab the title of webpage (even the webpages use JavaScript).  
Can print out in normal or markdown format.  
Currently support auto copy to clipboard via `xclip`.  
  
---  
  
## Requirements  
  
+ PhantomJS  
  
  
## Installation  
  
`$ pip install git+https://github.com/M157q/gettitle`  
  
  
## Usage  
  
```  
usage: gettitle.py [-h] [-m] [-d] url [url ...]  
  
positional arguments:  
  url             url(s) of the webpage  
  
optional arguments:  
  -h, --help      show this help message and exit  
  -m, --markdown  output with markdown format  
  -d, --debug     print out webpage source code and title for debugging  
```  
  
  
## Testing  
  
`$ python -m unittest`  
