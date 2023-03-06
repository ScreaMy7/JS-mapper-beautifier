# JS-mapper-beautifier
A tool which takes JS files links as input and beautifies JS files or maps the webpack.

<h1 align="left">
  <img src="https://github.com/ScreaMy7/JS-mapper-beautifier/raw/main/carbon.png" alt="pymap" width="700px">
  <br>
</h1>

# Usage
```
python main.py -i jsfile.txt -o ProgramName
```

Just give js file link as input , the tool itself identifies .map and .js file, and does
Firstly beautifies the code, if the file is a js file, or Identifies the .map file and parses it to recreate the folder structure.

The const.py has two constants ,which are the folder name for beautified JS file. If there is name-collision just change the value of constants.

This tool is part of blog post series on Javascript analysis for bug hunters avaliable at https://screamy7.github.io/.


This is a new tool so it so some bugs might pop up.
