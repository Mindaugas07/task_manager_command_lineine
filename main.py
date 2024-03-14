import datetime, os
from random import randint
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Dict, List, Union


class MongoDB:
    def __init__(
        self, host: str, port: int, db_name: str, collection_name: str
    ) -> None:
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def find_documents(self, query: Dict) -> List[Dict]:
        documents = self.collection.find(query)
        return list(documents)

    def update_one_document(self, query: Dict, update: Dict) -> int:
        result = self.collection.update_one(query, {"$set": update})
        return result.modified_count

    def update_many_document(self, query: Dict, update: Dict) -> int:
        result = self.collection.update_many(query, {"$set": update})
        return result.modified_count

    def delete_one_documents(self, query: Dict) -> int:
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_many_documents(self, query: Dict) -> int:
        result = self.collection.delete_many(query)
        return result.deleted_count

    def insert_one_document(self, document: Dict) -> str:
        result = self.collection.insert_one(document)
        print(f"Printed result: {result}")
        return str(result.inserted_id)

    def insert_many_document(self, document: Dict) -> List[str]:
        result = self.collection.insert_many(document)
        # print(f"Printed result: {result}")
        return list(result.inserted_ids)

    # def generate_data_base(self, numb_of_documents):
    #     for _ in range(numb_of_documents):
    #         self.create_random_person()

    def query_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$eq": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_greater_than(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$gt": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_greater_than_or_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$gte": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_in_array(
        self, field_name: str, value: List, parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$in": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_less_than(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$lt": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_less_than_or_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$lte": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_not_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$ne": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_not_in_array(
        self, field_name: str, value: List, parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$nin": value}}
        result = self.collection.find(query, parameter)
        return list(result)


def show_app_menu() -> str:

    return input(
        f"""
If you want to add a new task press {"--1--":^35}
If you want to view all tasks press {"--2--":^35} 

Press --9-- to quit our app                          
"""
    )


if __name__ == "__main__":
    taskdb = MongoDB(
        host="localhost",
        port=27017,
        db_name="task_manager",
        collection_name="tasks",
    )

    os.system("cls")

    while True:
        try:
            user_option = show_app_menu()
        except:
            print("Wrong input. Please enter a number from the list...")
            break
        if user_option == "1":
            os.system("cls")
            title = input("Enter the title of the task: ")
            description = input("Enter the task descripiton: ")
            status = "In progress"
            document = {"title": title, "description": description, "status": status}
            taskdb.insert_one_document(document)
            os.system("cls")
            print(f"Your task '{title}' was created!")

        elif user_option == "2":
            os.system("cls")
            query = {}
            task_details = taskdb.find_documents(query)
            print("Your tasks:")
            for index, task in enumerate(task_details):
                index += 1
                print(
                    f"Task nr. {index}.-- {task['title']}. Description: {task['description']}. Status: {task['status']}"
                )
            print()
            user_option = input(
                """Enter the number of the task which you wand to delete: 
                
Press --9-- to go back
"""
            )
            if user_option == "9":
                os.system("cls")

                user_option = show_app_menu()

            else:
                selected_document = task_details[int(user_option) - 1]
                query = {"_id": selected_document["_id"]}
                taskdb.delete_one_documents(query)
                os.system("cls")
                print(f"Task '{task['title']}' was deleted!")

        #     print(user_table_option)
        #     if user_table_option == "1":
        #         jazz_place.reserve_table(int(user_table_option))
        #         os.system("cls")
        #         user_options()

        #     elif user_table_option == "2":
        #         jazz_place.reserve_table(int(user_table_option))
        #         user_options()

        #     elif user_table_option == "9":
        #         os.system("cls")
        #         print(jazz_place)
        #         user_options()

        # elif user_option == "3":
        #     os.system("cls")
        #     print(jazz_place)
        #     jazz_place.reserve_table(1)

        # elif user_option == "4":
        #     os.system("cls")
        #     print(jazz_place)

        elif user_option == "9":
            os.system("cls")
            break
