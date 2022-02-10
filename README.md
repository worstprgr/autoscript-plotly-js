I'm plotting a bunch of realtime data with plotly (js-version) on a single html page. But it's very eshausting to change all the variables everytime and add more variables for the y-axis.

So I made a python script, that automates it for me and outputs a ready .js file.

_At http://stats.seishin.io is a live demo, where you can see, how the plot looks like._


**How does it work?**

1. 
  You need a csv file that contains a header. Something like:
  TIME, RENT, INCOME, FOOD

  The script reads only the first line in the csv and ignores the other below.
  It grabs the first position (TIME) and links it to the x-axis.
  The other positions in the same lime are linked to the y-axis and it creates the same amount of y-variables.

2. 
  You can run the script and it asks you a few questions:
  - the title of your plot. It will be displayed at the top of the plot
  - the path to your .csv (relative to the future .js file) -> this path will be written in the .js file
  - the path to your .csv file, that contains the header -> this path will be not written in the .js file
  - - > _the reason why I've chosen this approach: My path in my project directory is different from the final working directory_

  - set the values for the plot range on the y axis. It asks first for the minimum value, then for the maximum value

3.
  After that, it creates the .js file in the same folder. Make sure the script has permissions to write files in that folder.
  
  
**Configuration:**
If you want to change the layout, you can do it at line 72 in the python code.
If you want a deeper layout change, I recommend to render the .js file first and then do the modifications in the .js file.
-> the documentation can be found here: https://plotly.com/javascript/reference/layout/


**How to implement it in html?**
First, you need the 'Plotly.js' file - _look up https://plotly.com for more instructions_.
And then, just put the two lines of the following code in your html/php file:

`<div id="AAA"></div>
<script src="BBB.js"></script>`

AAA = the name of your csv file, but without the .csv extension. E.g.: 'mydata.csv' -> 'mydata'
BBB = the path of the rendered .js file


_Feel free to fork and modify this code by your needs!_


  



