# Infinite-Storage-Glitch-Python
ISG but in Python


## I made Infinite Storage Glitch (https://github.com/DvorakDwarf/Infinite-Storage-Glitch) but in Python, with a few advantages

### Pros
- Uses a lot (i mean a LOT) less ram, peaking usage at around 300 megabytes or less
- Made in python, meaning that the code is slightly easier to read
### Cons
- Not really that fast (didn't benchmark), you will be waiting around 0:45 to 1:30 hours for a 5 gb file depending on hardware
- Kinda hard to customize, but i have made efforts to make it easier
- No real UI, you need to edit the script to use


- Note: if you want to use it on Windows you need to change the codec from png to something else (don't ask me why ask the opencv devs), but it isn't really the best tactic to do since png is AFAIK the best codec for compression

### More info

- Usage: Scroll down to the bottom of the script, change the path (for Windows: C:\\\path\\\file.file, for Linux: /path/file.file) wait for the program to finish, upload the file somewhere, download it, set the decoder and decode it


- i suggest adding some sort of error correction, since every 800M bytes a bit flips after compression (it is the same stuff with Infinite-Storage-Glitch, especially on windows, and i will soon upload a simple script that adds reed solomon thanks to a library)


- don't worry if the encoding slows down just that teeny tiny fraction of a second after the start since if there is poor cooling that might be the problem 


- NOTE: the scripts have a LOT of comments, beware when trying to edit them haha


- you can find the demo right here, https://youtu.be/uksj04I5eWE (warning for people that may be triggered by flashing lights, dont click the link)
