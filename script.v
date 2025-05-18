win:
    title "script.v"
    dimensions 400 300

scene start:
    background_color blue

    entity thing:
        position 0 0
        shape triangle "50,50" green
        on key_space:
            change_scene end

scene end:
    background_color black
    entity message:
        position 200 250
        shape rectangle "400,100" white
        on start:
            set message "The End!"
