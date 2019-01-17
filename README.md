# IR1-1B
Assignment 1b, course IR1, MSc AI UvA


I've already made something to load in the data. It puts it in dictionaries, since output can vary from type and length.

Also I figured if we are splitting tasks up it is usefull with git if the work on those happens in different files, to avoid merge conflicts.
Therefore each step in the assignment has its own class. At the beginning the onstart is called. Thats were the main functionality is supposed to happen, yet more functions can be added.
The onstart can also return output, if you want to return multiple just return a list or dictionary (same goes for input).
At the end the onFinish is called, but it doesn't return output.

All this functionality is in the parent class in file step_general

This was just a quick draft of setup, I don't mean to be nazi in how we do things.

Feel free to change whatever!