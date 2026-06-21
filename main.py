from abc import ABC, abstractmethod

class BaseAccount(ABC):
    bank_name = "Vietcombank"

    def __init__(self, account_number, account_holder, initial_balance=0):
        if not self.validate_account_number(account_number):
            raise ValueError("Số tài khoản không hợp lệ! Phải gồm đúng 10 chữ số.")
        self._account_number = account_number
        self.account_holder = account_holder
        self.__balance = initial_balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def account_holder(self):
        return self._account_holder

    @account_holder.setter
    def account_holder(self, value):
        self._account_holder = " ".join(value.strip().upper().split())

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        self.__balance = value

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
        return isinstance(account_number, str) and len(account_number) == 10 and account_number.isdigit()

    @classmethod
    def update_bank_name(cls, new_name):
        cls.bank_name = new_name


class SavingsAccount(BaseAccount):
    def __init__(self, account_number, account_holder, interest_rate, initial_balance=0):
        super().__init__(account_number, account_holder, initial_balance)
        self.interest_rate = float(interest_rate)

    def deposit(self, amount):
        if amount <= 0:
            print("Số tiền nạp phải lớn hơn 0.")
            return False
        self.balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Số tiền rút phải lớn hơn 0.")
            return False
        penalty = amount * 0.02
        total_deduct = amount + penalty
        if self.balance < total_deduct:
            print("Số dư không đủ để thực hiện giao dịch (bao gồm 2% phí rút trước hạn).")
            return False
        self.balance -= total_deduct
        print(f"Phí phạt rút trước hạn (2%): {penalty:,.0f} VND")
        return True

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest


class CreditAccount(BaseAccount):
    def __init__(self, account_number, account_holder, credit_limit=20000000, initial_balance=0):
        super().__init__(account_number, account_holder, initial_balance)
        self.credit_limit = credit_limit

    def deposit(self, amount):
        if amount <= 0:
            print("Số tiền nạp phải lớn hơn 0.")
            return False
        self.balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Số tiền rút phải lớn hơn 0.")
            return False
        if self.balance - amount < -self.credit_limit:
            print("Lỗi: Vượt quá hạn mức thấu chi cho phép.")
            return False
        self.balance -= amount
        if self.balance < 0:
            print("(Sử dụng hạn mức thấu chi)")
        return True


class DigitalPremiumMixin:
    def cashback_reward(self, amount):
        if amount > 5000000:
            cashback = amount * 0.01
            print(f"[Ưu đãi Premium]: Bạn được hoàn tiền 1% ({cashback:,.0f} VND) vào tài khoản!")
            return cashback
        return 0


class HybridAccount(SavingsAccount, DigitalPremiumMixin):
    def __init__(self, account_number, account_holder, interest_rate, initial_balance=0):
        super().__init__(account_number, account_holder, interest_rate, initial_balance)

    def deposit(self, amount):
        if super().deposit(amount):
            cashback = self.cashback_reward(amount)
            if cashback > 0:
                self.balance += cashback
            return True
        return False


class VNPayGateway:
    def execute_pay(self, account, amount):
        print(f"[Hệ thống VNPay]: Đang kết nối tới tài khoản {account.account_number}...")
        if account.withdraw(amount):
            return True
        return False


class ViettelMoneyGateway:
    def execute_pay(self, account, amount):
        print(f"[Hệ thống Viettel Money]: Đang xử lý giao dịch cho tài khoản {account.account_number}...")
        if account.withdraw(amount):
            return True
        return False


def process_payment(payment_gateway, account, amount):
    if not hasattr(payment_gateway, "execute_pay"):
        print("Lỗi: Cổng thanh toán không hợp lệ hoặc chưa được tích hợp.")
        return
    
    print("Xác thực thanh toán bằng Duck Typing thành công!")
    if payment_gateway.execute_pay(account, amount):
        print(f"Tài khoản đã thanh toán hóa đơn giá trị: {amount:,.0f} VND.")
        print(f"Số dư mới: {account.balance:,.0f} VND.")
    else:
        print("Thanh toán thất bại.")


def main():
    accounts = []
    current_account = None

    while True:
        print("\n===== VIETCOMBANK DIGIBANK PRO SIMULATOR =====")
        print("1. Mở tài khoản mới (Chọn loại tài khoản)")
        print("2. Xem thông tin & Kiểm tra thứ tự kế thừa (MRO)")
        print("3. Giao dịch Nạp / Rút tiền & Tính điểm thưởng (Đa hình)")
        print("4. Tích lũy / Áp dụng lãi suất định kỳ")
        print("5. Kiểm tra tính năng gộp tài khoản & So sánh (Overloading)")
        print("6. Thanh toán hóa đơn qua Cổng trung gian (Duck Typing)")
        print("7. Thoát chương trình")
        print("==============================================")
        
        choice = input("Chọn chức năng (1-7): ").strip()

        if choice == "1":
            print("\n--- CHỌN LOẠI TÀI KHOẢN ---")
            print("1. Savings Account (Tài khoản Tiết kiệm)")
            print("2. Credit Account (Tài khoản Tín dụng)")
            print("3. Hybrid Account (Tài khoản Đa năng)")
            type_choice = input("Chọn loại tài khoản (1-3): ").strip()
            
            acc_num = input("Nhập số tài khoản 10 chữ số: ").strip()
            if not BaseAccount.validate_account_number(acc_num):
                print("Số tài khoản không hợp lệ! Phải gồm đúng 10 chữ số.")
                continue
                
            name = input("Nhập tên chủ tài khoản: ").strip()
            
            try:
                if type_choice == "1":
                    rate = float(input("Nhập lãi suất năm (ví dụ 0.05): ").strip())
                    new_acc = SavingsAccount(acc_num, name, rate)
                    print(f"\nMở tài khoản Tiết kiệm thành công!")
                elif type_choice == "2":
                    limit = float(input("Nhập hạn mức tín dụng (mặc định 20,000,000): ").strip() or 20000000)
                    new_acc = CreditAccount(acc_num, name, limit)
                    print(f"\nMở tài khoản Tín dụng thành công!")
                elif type_choice == "3":
                    rate = float(input("Nhập lãi suất năm (ví dụ 0.05): ").strip())
                    new_acc = HybridAccount(acc_num, name, rate)
                    print(f"\nMở tài khoản Đa năng Hybrid thành công!")
                else:
                    print("Lựa chọn loại tài khoản không hợp lệ.")
                    continue
                
                new_acc.account_holder = name
                accounts.append(new_acc)
                current_account = new_acc
                print(f"Chủ tài khoản: {current_account.account_holder}")
            except Exception as e:
                print(f"Lỗi khởi tạo: {e}")

        elif choice == "2":
            if not current_account:
                print("Hệ thống chưa có thông tin tài khoản. Vui lòng mở tài khoản ở Chức năng 1 trước.")
                continue
            print("\n--- THÔNG TIN TÀI KHOẢN HIỆN TẠI ---")
            print(f"Loại tài khoản: {current_account.__class__.__name__}")
            print(f"Ngân hàng: {current_account.bank_name}")
            print(f"Số tài khoản: {current_account.account_number}")
            print(f"Chủ tài khoản: {current_account.account_holder}")
            print(f"Số dư: {current_account.balance:,.0f} VND")
            if hasattr(current_account, "interest_rate"):
                print(f"Lãi suất: {current_account.interest_rate * 100}% / năm")
            if hasattr(current_account, "credit_limit"):
                print(f"Hạn mức tín dụng: {current_account.credit_limit:,.0f} VND")
            print(f"Thứ tự kế thừa (MRO): {[cls.__name__ for cls in current_account.__class__.__mro__]}")

        elif choice == "3":
            if not current_account:
                print("Hệ thống chưa có thông tin tài khoản.")
                continue
            print("\n--- GIAO DỊCH NẠP / RÚT TIỀN ---")
            print("1. Nạp tiền")
            print("2. Rút tiền")
            tx_choice = input("Chọn giao dịch (1-2): ").strip()
            amount = float(input("Nhập số tiền: ").strip().replace(",", ""))
            
            if tx_choice == "1":
                if current_account.deposit(amount):
                    print("Nạp tiền thành công!")
                    print(f"Số dư mới: {current_account.balance:,.0f} VND")
            elif tx_choice == "2":
                if current_account.withdraw(amount):
                    print("Rút tiền thành công!")
                    print(f"Số dư còn lại: {current_account.balance:,.0f} VND")
            else:
                print("Lựa chọn không hợp lệ.")

        elif choice == "4":
            if not current_account:
                print("Hệ thống chưa có thông tin tài khoản.")
                continue
            if isinstance(current_account, (SavingsAccount, HybridAccount)):
                print("\n--- TÍNH LÃI ĐỊNH KỲ ---")
                old_balance = current_account.balance
                interest = current_account.apply_interest()
                print(f"Số dư trước tính lãi: {old_balance:,.0f} VND")
                print(f"Lãi suất năm: {current_account.interest_rate * 100}%")
                print(f"Tiền lãi nhận được: +{interest:,.0f} VND")
                print(f"Số dư mới sau khi cộng lãi: {current_account.balance:,.0f} VND")
            else:
                print("Tài khoản hiện tại không hỗ trợ tính năng tính lãi suất định kỳ.")

        elif choice == "5":
            if not current_account:
                print("Hệ thống chưa có thông tin tài khoản.")
                continue
            if len(accounts) < 2:
                print("Hệ thống cần ít nhất 2 tài khoản để thực hiện so sánh/gộp.")
                continue
            
            print("\n--- ĐỒNG BỘ & SO SÁNH TÀI KHOẢN (OPERATOR OVERLOADING) ---")
            print(f"Tài khoản hiện tại (A): {current_account.account_holder} (Số dư: {current_account.balance:,.0f} VND)")
            print("Danh sách tài khoản đối ứng:")
            for i, acc in enumerate(accounts):
                if acc != current_account:
                    print(f"[{i}] {acc.account_number} ({acc.account_holder} - Số dư: {acc.balance:,.0f} VND)")
            
            idx = int(input("Chọn chỉ số tài khoản đối ứng (B): ").strip())
            other_account = accounts[idx]
            
            is_less = current_account < other_account
            total = current_account + other_account
            
            comp_str = "NHỎ HƠN" if is_less else "LỚN HƠN HOẶC BẰNG"
            print(f"[Kết quả So sánh (__lt__)]: Số dư tài khoản A {comp_str} số dư tài khoản B.")
            print(f"[Kết quả Tổng hợp (__add__)]: Tổng số tiền sở hữu của cả 2 tài khoản là: {total:,.0f} VND.")

        elif choice == "6":
            if not current_account:
                print("Hệ thống chưa có thông tin tài khoản.")
                continue
            print("\n--- THANH TOÁN HÓA ĐƠN QUA CỔNG TRUNG GIAN ---")
            print("1. Thanh toán qua VNPay")
            print("2. Thanh toán qua Viettel Money")
            print("3. Thử nghiệm Cổng thanh toán lỗi (Edge Case)")
            gw_choice = input("Chọn cổng thanh toán (1-3): ").strip()
            amount = float(input("Nhập số tiền hóa đơn: ").strip().replace(",", ""))
            
            if gw_choice == "1":
                gateway = VNPayGateway()
            elif gw_choice == "2":
                gateway = ViettelMoneyGateway()
            elif gw_choice == "3":
                gateway = object()
            else:
                print("Cổng thanh toán không hợp lệ.")
                continue
                
            process_payment(gateway, current_account, amount)

        elif choice == "7":
            print("Cảm ơn đã trải nghiệm hệ thống Vietcombank Digibank Pro Simulator!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại từ 1 đến 7.")

if __name__ == "__main__":
    main()