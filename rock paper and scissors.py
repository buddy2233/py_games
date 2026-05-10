import random

def game():
    while True:
        user_choice = input("Enter a choice( rock, paper, scissors ): ").lower()
        while user_choice not in ["rock", "paper", "scissors"]:
            user_choice = input("Invalid input. Enter a choice (rock, paper, scissors): ").lower()


        p_c = ["rock", "paper", "scissors"] #posible choice
        c_c = random.choice(p_c) #computer choice
        print(f"\n You chose {user_choice}, computer chose {c_c}.\n")

        if user_choice == c_c:
            print(f" Both players selected {user_choice}, computer chose {c_c}.\n")
        elif user_choice == "rock":
            if c_c == "scissors":
                print("rock smashes scissors! You win!.")
            else:
                print("paper covers rock! You lose.")
        elif user_choice == "paper":
            if c_c == "rock":
                print("paper covers rock! You win!")
            else:
                print("scissors cuts papper! You lose.")
        elif user_choice == "scissors":
            if c_c == "paper":
                print("scissors cuts paper! You win!")
            else:
                print("rock smashes scissors! You lose.")


        play_again = input("Play again(yes/no): ").lower()
        while play_again not in ["yes", "no"]:
            play_again = input("Invalid input. Play again(yes/no): ").lower()
        if play_again == "no":
            break
if __name__ == "__main__":
    game()
                
            
            
            
            
