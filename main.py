import requests
import phonenumbers
import socket
from phonenumbers import PhoneNumberFormat, NumberParseException


class SiteChecker:
    def __init__(self, url):
        """
        Конструктор класса.

        :param url: URL сайта для проверки.
        """
        self.url = url
        self.host = url.split("//")[-1]  # Извлечение имени хоста из URL.

    def check_site_status(self):
        """
        Проверяет статус сайта, отправляя HEAD запрос.
        Выводит в консоль информацию о доступности сайта.
        """
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                print(f"Сайт {self.url} работает.")
            else:
                print(f"Сайт {self.url} недоступен, статус код: {response.status_code}.")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при подключении к {self.url}: {e}")

    def get_ip_address(self):
        """
        Определяет IP адрес сайта.
        Выводит IP адрес в консоль.
        """
        try:
            ip = socket.gethostbyname(self.host)
            print(f"IP адрес хоста {self.host}: {ip}")
        except socket.gaierror as e:
            print(f"Ошибка при получении IP адреса {self.host}: {e}")

    def get_company_phone(self):
        """
        Извлекает и проверяет номера телефонов на сайте.
        Использует библиотеку phonenumbers для поиска и валидации номеров.
        Выводит найденные допустимые номера в консоль.
        """
        try:
            response = requests.get(self.url)
            for match in phonenumbers.PhoneNumberMatcher(response.text, None):
                if phonenumbers.is_valid_number(match.number):
                    formatted_number = phonenumbers.format_number(match.number, PhoneNumberFormat.INTERNATIONAL)
                    print(f"Найден допустимый номер телефона: {formatted_number}")
                    return
            print("Допустимый номер телефона не найден.")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных с {self.url}: {e}")

    def complete_tasks(self):
        """
        Выполняет все задачи: проверка доступности сайта, определение IP адреса,
        и поиск валидных номеров телефонов на сайте.
        """
        self.check_site_status()
        self.get_ip_address()
        self.get_company_phone()


if __name__ == "__main__":
    checker = SiteChecker("http://sstmk.ru")
    checker.complete_tasks()
