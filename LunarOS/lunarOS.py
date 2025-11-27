import time
time.sleep(2)
print("Booting v2.0LunarOS...")
time.sleep(2)
print("      ,===:'.,            `-._                ")
time.sleep(0.1)
print("                 `:.`---.__         `-._      ")
time.sleep(0.1)
print("                   `:.     `--.         `.    ")
time.sleep(0.1)
print("                     \.        `.         `.  ")
time.sleep(0.1)
print("             (,,(,    \.         `.   ____,-`.,")
time.sleep(0.1)
print("          (,'     `/   \.   ,--.___`.'  ")
time.sleep(0.1)
print("      ,  ,'  ,--.  `,   \.;'         `")
time.sleep(0.1)
print("       `{D, {    \  :    \;          ")
time.sleep(0.1)
print("         V,,'    /  /    //         ")
print("         j;;    /  ,' ,-//.    ,---.      ,   ")
time.sleep(0.1)
print("         \;'   /  ,' /  _  \  /  _  \   ,'/  ")
time.sleep(0.1)
print("               \   `'  / \  `'  / \  `.' /   ")
time.sleep(0.1)
print("                `.___,'   `.__,'   `.__,'   ")
time.sleep(0.1)
time.sleep(1.0)
print("Maric & Leonxzy studios")
time.sleep(5)
a= input("Username: ")
time.sleep(1)
print("Processing material...")
time.sleep(1.0)
print("Loading Apps...")
time.sleep(1.0)
print("Hello",a,"This is your LunarOS terminal")
time.sleep(1.0)
import snake
import calculator
import pong

def main_menu():
    while True:
        print("\nChoose a program:")
        print("1 - Snake")
        print("2 - Calculator")
        print("3 - Pong")
        print("(Type 'esc' to exit)")

        choice = input("> ").strip().lower()

        if choice == "esc":
            print("Goodbye!")
            break
        elif choice == "1":
            snake.run_snake()
        elif choice == "2":
            calculator.calculator()
        elif choice == "3":
            pong.run_pong()
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()




