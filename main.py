from functools import wraps

from addressbook import AddressBook, Record


def input_error(func):
    """Показує помилку введення, щоб бот міг прийняти наступну команду."""
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, AttributeError):
            return "Contact not found."
        except ValueError as error:
            return str(error)
        except IndexError:
            return "Enter user name."
    return inner


def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def require_args(args, count, usage):
    if len(args) != count:
        raise ValueError(f"Usage: {usage}")


@input_error
def add_contact(args, book):
    require_args(args, 2, "add <name> <phone>")
    name, phone = args
    name = name.lower()
    record = book.find(name)
    if record is None:
        record = Record(name)
        # Перевіряємо телефон до додавання контакту до книги.
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    require_args(args, 3, "change <name> <old_phone> <new_phone>")
    name, old_phone, new_phone = args
    book.find(name.lower()).edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book):
    require_args(args, 1, "phone <name>")
    record = book.find(args[0].lower())
    return "; ".join(str(phone) for phone in record.phones) or "No phones."


@input_error
def show_all(args, book):
    require_args(args, 0, "all")
    return str(book)


@input_error
def add_birthday(args, book):
    require_args(args, 2, "add-birthday <name> <DD.MM.YYYY>")
    book.find(args[0].lower()).add_birthday(args[1])
    return "Birthday added."


@input_error
def show_birthday(args, book):
    require_args(args, 1, "show-birthday <name>")
    birthday = book.find(args[0].lower()).birthday
    return str(birthday) if birthday is not None else "Birthday not set."


@input_error
def birthdays(args, book):
    require_args(args, 0, "birthdays")
    rows = (
        f"{item['name']}: {item['birthday']}"
        for item in book.get_upcoming_birthdays()
    )
    return "\n".join(rows) or "No upcoming birthdays."


@input_error
def hello(args, book):
    require_args(args, 0, "hello")
    return "How can I help you?"


@input_error
def close(args, book):
    require_args(args, 0, "close or exit")
    return "Good bye!"


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(close(args, book))
            if not args:
                break
        elif command == "hello":
            print(hello(args, book))
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
