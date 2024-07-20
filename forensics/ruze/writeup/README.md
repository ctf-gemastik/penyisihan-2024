# Writeup

## TL;DR
- Open using FTK Imager to analyze .ad1 file
- you can see file who indicated the device is got attack by ransomware
- and you find maybe the malicous exe
- in description '.. when he installs something suddenly his device reboots and his files suddenly disappear .. ', we can assume the ransomware need to reboot/login for got executed
- in windows you can set what device will do everytime user got login in Registry Key
- check on registry HCKU:SOFTWARE\Microsoft\Windows\CurrentVersion\Run you find some malicious entry
- the entry navigate you to .bat file contain powershell command
- understanding the powershell command, you know where client file stored, and how ransomware encrypt it
- decrypt file using result of your analyze, and you recover client file