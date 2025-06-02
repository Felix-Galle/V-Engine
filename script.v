// This is a test comment

win:
    title "script.v"
    dimensions 400 300

scene "start":

    background_color blue

    on key_space:
        change_scene "test"

    //entity "thing":
    //    position 0 0
    //    shape rectangle "50,100" green
    //    on key_space:
    //        change_scene "end"

scene "test":
    background_color white
