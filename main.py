from gui import GUI

if __name__ == "__main__":
    app = GUI()
    app.displayTitle()

    while True:
        app.waitForEnter()
        while True:
            app.displayMenu()
            choice = app.getChoice()
            if choice == "Invalid choice. Please enter a number between 1 and 7.":
                print(choice)
                continue

            app.processChoice(choice)