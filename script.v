scene start:
    background_color blue
    entity player:
        position 100 100
        shape rectangle "50,50" red
        on start:
            set speed 5
        on key_Right:
            set position 200 100
        on key_Left:
            set position 0 100
        on key_space:
            change_scene end

scene end:
    background_color black
    entity message:
        position 200 250
        shape rectangle "400,100" white
        on start:
            set message "The End!"
