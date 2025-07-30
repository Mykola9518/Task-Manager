while True:
    print ("TASK MANAGER")
    try:
        operation_desc = [
        'Select action:\n'
        '1 - Add a task \n'
        '2 - Show all tasks \n'
        '3 - Find a task \n'
        '4 - Task filter \n'
        '5 - Delete task \n'
        '6 - Mark as done \n'
        '7 - Quit \n'
        ]
        operation = ['1', '2', '3', '4', '5', '6', '7']
        for item in operation_desc:
            print(item)
        print("Enter operation")
        select_action = str(input())
        if select_action in operation:
            if select_action == '1':
                print('Add a task')
            elif select_action == '2':
                print('Show all tasks')
            elif select_action == '3':
                print('Find a task')
            elif select_action == '4':
                print('Task filter')
            elif select_action == '5':
                print('Delete task')
            elif select_action == '6':
                print('Mark as done')
            elif select_action == '7':
                print('Quit the program')
                break
        else:
            raise ValueError('Not corrected operation')
    except:
        print('Error')



