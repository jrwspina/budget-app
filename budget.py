class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
    
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def get_balance(self):
        balance = 0
        for entry in self.ledger:
            balance += float(entry["amount"])
        return float(balance)

    def check_funds(self, amount):
        funds = self.get_balance()
        if amount > funds:
            return False
        return True

    def get_expenditure(self):
        expenditure = 0.0
        for entry in self.ledger:
            if entry["amount"] < 0:
                expenditure += abs(float(entry["amount"]))
        return expenditure

    def withdraw(self, amount, description=""):
        if(self.check_funds(amount)):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def transfer(self, amount, budget_category):
        if(self.check_funds(amount)):
            self.withdraw(amount, f"Transfer to {budget_category.category}")
            budget_category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def __str__(self):
        budget_lines = self.category.center(30, '*')
        lines = []
        for entry in self.ledger:
            desc_elem = entry['description'][0:23]
            amount_elem = f"{entry['amount']:.2f}"[0:7]
            width = 30 - len(desc_elem)
            amount_elem = amount_elem.rjust(width)
            line = desc_elem + amount_elem
            lines.append(line)
        for line in lines:
            budget_lines += '\n' + line
        return budget_lines + '\n' + f'Total: {self.get_balance():.2f}'    
    
def create_spend_chart(categories):
    chart_labels_y = [i for i in range(100, -1, -10)]
    categories_percentage = []
    total_spent = sum([category.get_expenditure() for category in categories])
    categories_percentage = categories_percentage = [int((category.get_expenditure()*100 / total_spent // 10) * 10) for category in categories]

    categories_labels_y = [[i for i in range(c, -1, -10)] for c in categories_percentage]
    marked, unmarked = " o ", "   "
    chart = ""
    for label in chart_labels_y:
        label_elem = str(label) + '|'
        width = 4 - len(label_elem)
        label_elem = " "*width + label_elem
        values = []
        for c_labels in categories_labels_y:
            if(label in c_labels):
                values.append(marked)
            else:
                values.append(unmarked)
        for v in values:
            label_elem += v
        chart += label_elem + ' ' + '\n'
  
    width = max([len(x) for x in [c.category for c in categories]])
    x_labels = " "*4 + "-" + "-"*3*len(categories)
    categories_names = [c.category + " "*(width - len(c.category)) for c in categories]
    for i in range(width):
        letters = [" " + name[i] + " " for name in categories_names]
        line = " "*4
        for l in letters:
            line += l
        x_labels += "\n" + line + ' '
        
    return "Percentage spent by category\n" + chart + x_labels