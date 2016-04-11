# Pythonied

A collection of short and simple Python programs.

### [aspectratio](aspectratio.py)
Python3 command line script to calculate the missing dimension of an image when changing its width or height so its aspect ratio is kept intact.  

Useful when you want to resize an image but don't want to consult fancy image-editing software.

### [timelogger](timelogger.py)
Python3 script to log the current time and home directory of the logging user. 

The script is run via a cron job.  
Use the following code to run the script every ten minutes starting from the full hour.
```
$ crontab -e 
*/10 * * * * /path/to/python3 /path/to/script/timelogger.py
```

Rename ```timelogger_config.py.template``` to ```timelogger_config.py``` and specify the path to the directory you want to write your log file to, otherwise it will be saved in your home directory.
