# Pythonied

A collection of short and simple Python programs.

For scripts that need general configuration variables to be set, rename ```config.py.template``` to ```config.py``` and add the missing variables.

All scripts are run using:
```
$ python3 scriptname.py
```

### [aspectratio](pythonied/aspectratio.py)
Python3 command line script to **calculate the missing dimension of an image** when changing its width or height so its aspect ratio is kept intact.  

Useful when you want to resize an image but don't want to consult fancy image editing software.


### [gpgcreate](pythonied/gpgcreate.py)
Set up a directory for GPG keys and **create new GPG keys**.

Uses ```config.py```.



### [sendmail](pythonied/sendmail.py)
Program to **send an e-mail** message from an existing e-mail address to a recipient.

Uses ```config.py```.


### [timelogger](pythonied/timelogger.py)
Python3 script to **log the current time** and home directory of the logging user. 

The script is run via a cron job.  
Use the following code to run the script every ten minutes starting from the full hour.  
```
$ crontab -e 
*/10 * * * * /path/to/python3 /path/to/script/timelogger.py
```

Uses ```config.py```.