# GUI class that displays the title and menu of the application.


class GUI:
    def displayTitle(self):
        # Display the title and author information
        text = [
            "ST1507 DSAA: Expression Evaluator & Sorter",
            "-----------------------------------------------------------",
            "",
            " - Done by: Jun Xian (put ur no here) & Phylicia (2308908)",
            " - Class DAAA/2A/22",
            ""
        ]
    
        max_length = max(len(line) for line in text)
        border = '*' * (max_length + 4)

        print(border)
        for line in text:
            print(f"* {line.ljust(max_length)} *")
        print(border)

    def displayMenu(self):
        # Display the menu options
        menu_options = [
            "\nPlease select your choice ('1', '2', '3', '4', '5', '6', '7')",
            "1. Evaluate expression",
            "2. Sort Expression",
            "3. Extra Feature",
            "4. Extra Feature",
            "5. Extra Feature",
            "6. Extra Feature",
            "7. Exit"
]

        for option in menu_options:
            print(option)

    def getChoice(self):
        # Get the user's choice and validate it
        choice = (input("Enter your choice: "))

        valid_choices = ['1', '2', '3', '4', '5', '6', '7']
        if choice not in valid_choices:
            return "Invalid choice. Please enter a number between 1 and 7."
        print('\n')
        return choice
    
    def waitForEnter(self):
        # Wait for the user to press Enter to continue
        while True:
            pressEnter = input("\nPress Enter to continue...")

            if pressEnter == "":
                break
            else:
                print("Invalid input. Please press Enter to continue.")

    def processChoice(self, choice):
        if choice == '1':
            #ensure can handle divide by zero

            self.waitForEnter()

        elif choice == '2':
            return
            
        elif choice == '3':
            return
            
        elif choice == '4':
            return

        elif choice == '5':
            return


        elif choice == '6':
            return

        elif choice == '7':
            print("Bye, thanks for using ST1507 DSAA: Expression Evaluator & Sorter")
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
