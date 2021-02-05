import random


class Initiative:

    def __init__(self):
        self.order = []
        self.members = {}

    def intake(self, member: str, bonus: int):
        self.members[member] = bonus

    def insert(self, member: str, bonus: int):
        self.members[member] = bonus
        roll = random.randint(1, 20) + bonus
        self.order.append((member, roll))
        self.order.sort(reverse=True, key=lambda tup: tup[1])

    def remove(self, member: str):
        try:
            self.members.pop(member)
            return None
        except KeyError:
            return f"{member} was not in initiative."

    def rollup_initiative(self):
        self.order = []
        for member in self.members:
            roll = random.randint(1, 20)
            self.order.append((member, self.members[member] + roll))
            self.order.sort(reverse=True, key=lambda tup: tup[1])

    def clear(self):
        self.order = []
        self.members = {}

    def present(self):
        send_string = ""
        for member in self.order:
            send_string += f"{member[0]}: {member[1]}\n"
        return send_string