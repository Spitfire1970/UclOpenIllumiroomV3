from time import sleep

def talk(message):
    return "Talk " + message


def main():
    print(talk("Hello World bye!"))
    sleep(2)


if __name__ == "__main__":
    main()