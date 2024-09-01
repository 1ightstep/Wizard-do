import os

class Database:
    def __init__(self, database_dir_path: str):
        self.database_dir_path = os.getcwd()+database_dir_path
        if not os.path.exists(self.database_dir_path):
            os.makedirs(self.database_dir_path)

    def create_data_category(self, category_name: str) -> None:
        if not os.path.exists(f'{self.database_dir_path}/{category_name}.txt'):
            new_category_file = open(f'{self.database_dir_path}/{category_name}.txt', 'x')
            new_category_file.close()

    def category_exists(self, category_name: str) -> bool:
        category_path = f"{self.database_dir_path}/{category_name}.txt"
        if os.path.exists(category_path):
            return True
        return False

    def search(self, category_name, key: str, value: str) -> None:
        if not self.category_exists(category_name):
            raise Exception(f"{category_name} does not exist in the current database directory!")
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            for line in lines:
                if line[key] == value:
                    return line
            f.close()

    def add_data(self, category_name: str, data_object: dict) -> None:
        if not self.category_exists(category_name):
            raise Exception(f"{category_name} does not exist in the current database directory!")
        with open(f'{self.database_dir_path}/{category_name}.txt', 'a') as f:
            f.write(str(data_object)+"\n")
            f.close()

    def delete_data(self, category_name: str, ):

if __name__ == "__main__":
    test = Database("/database")
    test.create_data_category("tasks")
    test.add_data("tasks", {"task_name": "name", "task_tag": "blue"})
    print(test.search("tasks", "task_name", "name"))


