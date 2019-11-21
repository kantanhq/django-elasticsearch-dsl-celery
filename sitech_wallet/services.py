from sitech_wallet import exceptions
from sitech_wallet.models import Transaction


def check_amount(amount):
    if amount < 0:
        raise exceptions.AmountInvalid()


def verify_withdraw(holder, amount):
    if not holder.can_withdraw(amount):
        raise exceptions.InsufficientFunds()


def deposit(wallet, amount, meta=None):
    check_amount(amount)

    wallet.balance += amount
    wallet.save()

    transaction = Transaction(
        type=Transaction.TYPE_WITHDRAW,
        amount=amount,
        from_wallet=wallet,
        meta=meta
    ).save()
    return transaction


def force_withdraw(wallet, amount, meta=None):
    check_amount(amount)

    wallet.balance -= amount
    wallet.save()

    transaction = Transaction(
        type=Transaction.TYPE_WITHDRAW,
        amount=amount,
        from_wallet=wallet,
        meta=meta
    ).save()
    return transaction


def force_transfer(from_wallet, to_wallet, amount, meta=None):
    check_amount(amount)

    from_wallet.balance -= amount
    from_wallet.save()
    withdraw = Transaction(
        type=Transaction.TYPE_WITHDRAW,
        amount=amount,
        from_wallet=from_wallet,
        to_wallet=to_wallet,
        meta=meta
    ).save()

    to_wallet.balance += amount
    to_wallet.save()
    deposit = Transaction(
        type=Transaction.TYPE_DEPOSIT,
        amount=amount,
        from_wallet=to_wallet,
        to_wallet=from_wallet,
        meta=meta
    ).save()

    return [withdraw, deposit]
