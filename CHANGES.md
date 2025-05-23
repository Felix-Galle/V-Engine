# Changelog

## Description

All notable changes to this project will be documented in this file.

Please remember that when you Commit and Push/Sync to github, please include the changes you've made to this file.

> To suggest more features, go to [issues](https://github.com/Felix-Galle/V-Engine/isses)

## Changelog

> ## 17.05.2025
>
> ## v0.0.1
>
> __By:__ Felix-Galle
>
> - Added [CHANGES.md](https://github.com/Felix-Galle/V-Engine/CHANGES.md):
> This file is/will be used to comprehensively show the changes made by collaborators.
>
> - Added a file called [full_code.py](https://github.com/Felix-Galle/V-Engine/full_code.py):
> This file is a version of this project's code all in one file/module.
> Be aware that the latest version of full_code.py may not be the latest version of the rest of the project.
>

> ## 18.05.2025
>
> ## v0.0.2
>
> __By:__ Felix-Galle
>
> ### Updates
>
> - Added a triangle.
>
>~~~python
>   entity thing:
>       position 0 0
>       shape triangle "50,50" green
>~~~
>
> - Added Comments: Any code right of the declaration is ignored, until the next line.
>
>~~~python
>   title "Example Title & code" # This section isn't executed
>~~~
>
> - Added win settings, which must be at the top of the file.
>
>~~~python
>win:
>   title "Example_Title"
>   dimensions 200 200
>~~~
>
> ### Bugs
>
> - "KeyPress" doesn't work.
> - Polygon Triangle doesn't show up on the scene.
>
> ### Planned Features
>
> - More application arguments, e.g.:
>   - Toggleable Debug Mode: --debug or --verbose
> - More polygons.
> - Compatibility with hex color codes.
> - More control of logging (perhaps through application arguments).

> ## 21.05.25
>
> ## v0.0.3
>
> __By:__ Felix-Galle
>
> - Fixed the scene definitions now uses this syntax:
>
>~~~python
>scene "<name>":
>   # Scene code, blah blah, boring...
>~~~
>
>>More info on this can be found in `SYNTAX.md`
>
> - Added more file arguements cuz they useful :D
>
> - Made comments easier and nicer (for me) to read.
> When running the project, view the ./logs folder to see the logs.
> Log Level is currently set at DEBUG, this will change, just cuz easier to debug, hence the amazingly mindful name :|
>
>> If there are any bugs, I haven't found them cuz I'm too tired, I writing this at 04:06am :( , & I'm too lazy lol
> Imma go sleep now, gn

> ## 23/05/25
>
> ## v0.0.3.1
>
> __By:__ Felix-Galle
>
> Not much to say about this one, hence the v0.0.3.1 as opposed to v0.0.4
> Still here is the stuff changed:
>
> - Added WORKING `--debug` argument !
> This allows the logging to output more data e.g.:
>
>~~~plaintext
>[root/INFO] 2025-05-23 03:13:15,472 > V-Engine starting...
>[root/DEBUG] 2025-05-23 03:13:15,472 > Debug mode enabled
>[root/INFO] 2025-05-23 03:13:15,472 > Created by: Felix-Galle & thatfacelessone
>~~~plaintext
> -  For some unknown reason, I've also made it so that one the Lexer has finished tokenizing the thingy, it outputs every single token (which looks nerdy as heck)
>~~~plaintext
>
>[root/INFO] 2025-05-23 03:13:15,583 > Tokenizing...
>[root/DEBUG] 2025-05-23 03:13:15,583 > Lexer tokens:
>[root/DEBUG] 2025-05-23 03:13:15,583 > tok0: COMMENT,# This is a test comment
>[root/DEBUG] 2025-05-23 03:13:15,583 > tok1: NEWLINE, 
>~~~
>
>> Be aware: this 'feature' will likely be removed, it's just so my smooth ass brain can comprehend each thing in the file.
>
> I need to stop coding late at night, I do stoopid shit, and become stupid lvels o sassiness
>
> - added 'versions'... Erm akshully, I added version/change identifiers. This means that I can now pin point at what version I'm at.
