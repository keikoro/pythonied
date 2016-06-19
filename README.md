# Pythonied

A collection of short and simple Python programs.

For scripts that need general configuration variables to be set, rename ```config.py.template``` to ```config.py``` and add the missing variables.

All scripts are run using:
```
$ python3 scriptname.py
```


## [aspectratio](pythonied/aspectratio.py)
**Calculate the missing dimension of an image** when changing its width or height so its aspect ratio is kept intact.  

Useful when you want to resize an image but don't want to consult fancy image editing software.


## [findfiles](pythonied/findfiles.py)
[WIP] **Find files** based on file types and file name patterns.

Depends on `config.py`.


## [gpgcreate](pythonied/gpgcreate.py)
Set up a directory for GPG keys and **create new GPG keys**.

Depends on `config.py`.

`$ python3 gpgcreate.py -h ` lists all available options for running the script.


## [searchdict](pythonied/searchdict.py)
**Search a dictionary** for the occurrence of words or words part. Additionally, all results can be intersected to look for words common to the individual sets of matches.

Depends on `config.py`.

`$ python3 searchdict.py -h ` lists all available options for running the script.


## [sendmail](pythonied/sendmail.py)
**Send an e-mail** message from an existing e-mail address to a recipient.

Depends on `config.py`.


## [timelogger](pythonied/timelogger.py)
**Log the current time** and home directory of the logging user. 

The script is run via a cron job.  
Use the following code to run the script every ten minutes starting from the full hour.  
```
$ crontab -e 
*/10 * * * * /path/to/python3 /path/to/script/timelogger.py
```

Depends on `config.py`.