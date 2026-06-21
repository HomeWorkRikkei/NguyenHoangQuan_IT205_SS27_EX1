from abc import ABC, abstractmethod


class BaseAccount(ABC):
    bank_name = "Vietcombank"

    def __init__(self, account_number, owner_name, balance=0):
        self.account_number = account_number
        self.owner_name = owner_name.strip().upper()
        self._BaseAccount__balance = balance

    @property
    def balance(self):
        return self._BaseAccount__balance

    def _set_balance(self, value):
        self._BaseAccount__balance = value

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented
        return self.balance + other.balance

    def __lt__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented
        return self.balance < other.balance

    @staticmethod
    def validate_account_number(account_number):
        return account_number.isdigit() and len(account_number) == 10

    @classmethod
    def update_bank_name(cls, new_name):
        cls.bank_name = new_name


class SavingsAccount(BaseAccount):
    def __init__(self, account_number, owner_name, interest_rate, balance=0):
        super().__init__(account_number, owner_name, balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        self._set_balance(self.balance + amount)

    def withdraw(self, amount):
        fee = amount * 0.02
        total = amount + fee
        if total > self.balance:
            raise ValueError("Insufficient balance")
        self._set_balance(self.balance - total)

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self._set_balance(self.balance + interest)
        return interest


class CreditAccount(BaseAccount):
    def __init__(self, account_number, owner_name, credit_limit, balance=0):
        super().__init__(account_number, owner_name, balance)
        self.credit_limit = credit_limit

    def deposit(self, amount):
        self._set_balance(self.balance + amount)

    def withdraw(self, amount):
        if self.balance - amount < -self.credit_limit:
            raise ValueError("Vượt quá hạn mức thấu chi cho phép")
        self._set_balance(self.balance - amount)


class DigitalPremiumMixin:
    def cashback_reward(self, amount):
        if amount > 5_000_000:
            reward = amount * 0.01
            self.deposit(reward)
            return reward
        return 0


class HybridAccount(SavingsAccount, DigitalPremiumMixin):
    pass


class VNPayGateway:
    def execute_pay(self, account, amount):
        account.withdraw(amount)
        print(f"VNPay paid {amount:,} VND")


class ViettelMoneyGateway:
    def execute_pay(self, account, amount):
        account.withdraw(amount)
        print(f"Viettel Money paid {amount:,} VND")


def process_payment(payment_gateway, account, amount):
    try:
        payment_gateway.execute_pay(account, amount)
    except AttributeError:
        print("Cổng thanh toán không hợp lệ hoặc chưa được tích hợp")


if __name__ == "__main__":
    print("Vietcombank Digibank Pro Simulator")