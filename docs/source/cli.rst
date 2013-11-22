Command Line Interface
======================

As of 0.2.1, wunderpy has a companion cli program under the name "wunderlist".

Examples
""""""""
::

    > wunderlist --help
    usage: wunderlist [-h] [-a] [-c] [-d] [-o] [--display] [-l LIST] [-t TASK]
    
    A Wunderlist CLI client.
    
    optional arguments:
      -h, --help            show this help message and exit
      -a, --add             Add a task or list.
      -c, --complete        Complete a task.
      -d, --delete          Delete a task or list.
      -o, --overview        Display an overview of your Wunderlist. Limited to 5
                            tasks per list.
      --display             Display all items in a list specified with --list.
      -l LIST, --list LIST  Used to specify a list, either for a task in a certain
                            list, or for a command that only operates on lists.
                            Default is inbox.
      -t TASK, --task TASK  Used to specify a task name.
      
      > wunderlist -a --task "Buy Milk" # add task Buy Milk to the inbox
      > wunderlist -a --task "Acquire Tanks" --list "World Domination" # add to World Domination list
      > wunderlist -c --task "Buy Milk" # complete Buy Milk task
      > wunderlist -o # display a short overview of all lists
      > wunderlist --display --list "World Domination" # display all tasks in the World Domination list