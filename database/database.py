import os


class Database:
    def __init__(self, database_dir_path: str) -> None:
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

    def category_error(self, category_name: str) -> None:
        if not self.category_exists(category_name):
            raise Exception(f"{category_name} does not exist in the current database directory!")

    def key_exists(self, category_name: str, key: str) -> bool:
        self.category_error(category_name)
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            for line in lines:
                if key in line.keys():
                    return True
        return False

    def search(self, category_name: str, key: str, value: str) -> dict:
        self.category_error(category_name)
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            for line in lines:
                if line[key] == value:
                    return line
            f.close()
        return {}

    def search_all(self, category_name: str, key: str, value: str) -> list:
        self.category_error(category_name)
        results = []
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            results = [
                line
                for line in lines
                if line[key] == value
            ]
            f.close()
        return results

    def search_value(self, category_name: str, value: str) -> list:
        self.category_error(category_name)
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            results = [
                line
                for line in lines
                if value in str(line.values())
            ]
            f.close()
        return results

    def add_data(self, category_name: str, data_object: dict) -> None:
        self.category_error(category_name)
        with open(f'{self.database_dir_path}/{category_name}.txt', 'a') as f:
            f.write(f"{str(data_object)}\n")
            f.close()

    def replace_category(self, category_name: str, data_list: list) -> None:
        self.category_error(category_name)
        write_data_list = "\n".join([str(data) for data in data_list])
        with open(f'{self.database_dir_path}/{category_name}.txt', 'w') as f:
            f.write(write_data_list)
            f.close()

    def replace_data(self, category_name: str, key: str, value: str) -> None:
        self.category_error(category_name)
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            for line in lines:
                if key in line.keys():
                    line[key] = value
            self.replace_category(category_name, lines)
            f.close()

    def delete_data(self, category_name: str, key: str, value: str) -> None:
        self.category_error(category_name)
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            for line in lines:
                if line[key] == value:
                    lines.remove(line)
            self.replace_category(category_name, lines)
            f.close()

    def return_value(self, category_name: any, key: str) -> str:
        self.category_error(category_name)
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            for line in lines:
                if key in line.keys():
                    return line[key]
            f.close()
        return ""

    def return_all(self, category_name: str) -> list:
        self.category_error(category_name)
        with open(f'{self.database_dir_path}/{category_name}.txt', 'r') as f:
            lines = list(eval(line.strip()) for line in f.readlines())
            f.close()
        return lines
