import pytest
from app.calculations import adder, divider, multiplier, subtractor, BankAccount, InsufficientFunds



@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def initialize_bank_account():
    def _create_account(amount):
        return BankAccount(amount)
    return _create_account

@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 5),
    (5, 4, 9),
    (10, 5, 15),
])

def test_adder(num1, num2, expected):
    print("Testing adder function")
    sum = adder(num1, num2)
    assert sum == expected, f"Expected {expected} but got {sum}"

def test_subtractor():
    print("Testing subtractor function")
    difference = subtractor(5, 4)
    assert difference == 1, f"Expected 1 but got {difference}"

def test_multiplier():
    print("Testing multiplier function")
    product = multiplier(2, 3)
    assert product == 6, f"Expected 6 but got {product}"

def test_divider():
    print("Testing divider function")
    quotient = divider(6, 3)
    assert quotient == 2, f"Expected 2 but got {quotient}"


@pytest.mark.parametrize("amount, expected", [
    (100, 100)])
def test_bank_account_initialization(amount, expected, initialize_bank_account):
    bank_account = initialize_bank_account(amount)
    assert bank_account.balance == expected, f"Expected balance to be {expected} but got {bank_account.balance}"


def test_bank_default_balance(zero_bank_account):
    assert zero_bank_account.balance == 0, f"Expected balance to be 0 but got {zero_bank_account.balance}"


@pytest.mark.parametrize("balance, withdrawal_amount, expected", [
    (100, 20, 80),
    (50, 50, 0),
])

def test_bank_withdrawal(balance, withdrawal_amount, expected, initialize_bank_account):
    bank_account = initialize_bank_account(balance)
    bank_account.withdraw(withdrawal_amount)
    assert bank_account.balance == expected, f"Expected balance to be {expected} but got {bank_account.balance}"


@pytest.mark.parametrize("balance, deposit_amount", [
    (120, 30),
    (755.90, 44.50)
])
def test_deposit(balance, deposit_amount, initialize_bank_account):
    bank_account = initialize_bank_account(balance)
    bank_account.deposit(deposit_amount)
    assert bank_account.balance == balance + deposit_amount, f"Expected balance to be {balance + deposit_amount} but got {bank_account.balance}"


@pytest.mark.parametrize("balance, expected", [
    (50, 55)
])
def test_collect_interest(balance, expected, initialize_bank_account):
    bank_account = initialize_bank_account(balance)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == expected, f"Expected balance to be {expected} but got {bank_account.balance}"



@pytest.mark.parametrize("deposit_amount, withdrawal_amount, expected", [
    (150, 100, 50),
    (500, 120, 380)
])
def test_bank_transaction(deposit_amount, withdrawal_amount, expected, zero_bank_account):
    zero_bank_account.deposit(deposit_amount)
    zero_bank_account.withdraw(withdrawal_amount)
    assert zero_bank_account.balance == expected, f"Expected balance to be {expected} but got {zero_bank_account.balance}"


@pytest.mark.parametrize("deposit_amount, withdrawal_amount", [
    (150, 1000),
    (500, 1200)
])
def test_insufficient_funds(deposit_amount, withdrawal_amount, initialize_bank_account):
    bank_account = initialize_bank_account(deposit_amount)
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(withdrawal_amount)
