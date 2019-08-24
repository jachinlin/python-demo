# -*- coding: utf-8 -*-

import logging

from protobuf_addressbook import addressbook_pb2


logger = logging.getLogger(__name__)


class AddressBook:

    def __init__(self, filename: str):
        self._file_name = filename
        address_book = addressbook_pb2.AddressBook()
        self._address_book = address_book
        try:
            with open(filename, 'rb') as f:
                address_book.ParseFromString(f.read())
        except IOError:
            logger.error(f"{filename}: File not found. Creating a new file.")

    def save(self) -> None:
        with open(self._file_name, 'wb') as f:
            f.write(self._address_book.SerializeToString())

    def prompt_add_person(self) -> addressbook_pb2.Person:
        person = self._address_book.people.add()
        person.id = int(input("Enter person ID number: "))
        person.name = input("Enter name: ")

        email = input("Enter email address (blank for none): ")
        if email != "":
            person.email = email

        while True:
            number = input(
                "Enter a phone number (or leave blank to finish): ")
            if number == "":
                break

            phone_number = person.phones.add()
            phone_number.number = number

            type_ = input("Is this a mobile, home, or work phone? ")
            if type_ == "mobile":
                phone_number.type = addressbook_pb2.Person.MOBILE
            elif type_ == "home":
                phone_number.type = addressbook_pb2.Person.HOME
            elif type_ == "work":
                phone_number.type = addressbook_pb2.Person.WORK
            else:
                print("Unknown phone type; leaving as default value.")
        self.save()
        return person

    def list_people(self) -> None:
        for person in self._address_book.people:
            print("Person ID:", person.id)
            print("  Name:", person.name)
            if person.email != "":
                print("  E-mail address:", person.email)

            for phone_number in person.phones:
                if phone_number.type == addressbook_pb2.Person.MOBILE:
                    print("  Mobile phone #:", end=" ")
                elif phone_number.type == addressbook_pb2.Person.HOME:
                    print("  Home phone #:", end=" ")
                elif phone_number.type == addressbook_pb2.Person.WORK:
                    print("  Work phone #:", end=" ")
                print(phone_number.number)

