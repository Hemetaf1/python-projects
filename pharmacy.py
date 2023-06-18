class Drug:
    def __init__(self, name: str, amount: int, price: int):
        self.name = name
        self.price = price
        self.amount = amount


class Pharmacy:
    def __init__(self, name: str):
        self.name = name
        self.drugs = []
        self.employees = []

    def add_drug(self, drug: Drug):
        self.drugs.append(Drug)

    def add_employee(self, first_name: str, last_name: str, age: int):
        emp = {}
        emp.update({"first_name":first_name, "last_name": last_name, "age":age})
        self.employees.append(emp)
        
    def total_value(self) -> int:
        summ = 0
        for drug in self.drugs:
            summ+= drug.price * drug.amount
        return summ

    def employees_summary(self) -> str:
        a = "Employees:\n"
        for i in self.employees:
            a += f"The employee number {self.employees.index(i)+1} is {i['first_name'].title()} {i['last_name'].title()} who is {i['age']} years old.\n"
        return a