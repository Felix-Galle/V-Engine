# Changelog

## Description

All notable changes to this project will be documented in this file.

Please remember that when you Commit and Push/Sync to github, please include the changes you've made to this file.

> To suggest more features, go to [issues](https://github.com/Felix-Galle/V-Engine/isses)

## Changes

> ## 17.05.2025
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

> ## 18.05.2025 - (01)
>
> __By:__ Felix-Galle
>
> - Added a triangle.
>
>~~~python
>   entity thing:
>       position 0 0
>       shape triangle "50,50" green
>~~~
>
> - Added Comments
> Any code right of the declaration is ignored, until the nextline.
>
>~~~python
>   title "Example Title & code" # This section isn't executed
>~~~

> ## 18.05.2025 - (02)
>
> __By:__ Felix-Galle
>
> - Added win settings, they must be at the top of the file.
>
>~~~python
>win:
>   title "Example_Title"
>   dimensions 200 200
>~~~
>
> ### Bugs
>
> - "KeyPress" don't work.
> - Polygon Triangle doesn't show up on scene
>
> ### Planned Features
>
> - More application arguements e.g.
>   - Toggleable Debug Mode: --debug or --verbose
> - More polygons
> - compatibility with hex color codes
> - More control of logging (perhaps through application arguements).
>
>
