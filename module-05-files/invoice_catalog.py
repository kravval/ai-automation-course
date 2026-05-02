"""Операции над каталогом счетов (list[dict])."""

from tabulate import tabulate


def filter_unpaid(invoices: list[dict]) -> list[dict]:
    return [inv for inv in invoices if not inv["paid"]]


def filter_by_min_amount(invoices: list[dict], min_amount: float) -> list[dict]:
    return [inv for inv in invoices if inv["amount"] >= min_amount]


def filter_by_vendor(invoices: list[dict], vendor: str) -> list[dict]:
    return [inv for inv in invoices if inv["vendor"] == vendor]


def sort_by_amount(invoices: list[dict], descending: bool = False) -> list[dict]:
    return sorted(invoices, key=lambda inv: inv["amount"], reverse=descending)


def sort_by_date(invoices: list[dict], descending: bool = False) -> list[dict]:
    return sorted(invoices, key=lambda inv: inv["date"], reverse=descending)


def total_amount(invoices: list[dict]) -> float:
    return sum(inv["amount"] for inv in invoices)

def unique_vendors(invoices: list[dict]) -> set[str]:
    return {inv["vendor"] for inv in invoices}

def print_invoices_table(invoices: list[dict], title: str = "Счета") -> None:
    if not invoices:
        print(f"\n{title}: (пусто)")
        return

    rows = [
        {
            "Number": inv["number"],
            "Vendor": inv["vendor"],
            "Amount": f"${inv['amount']:,.2f}",
            "Paid": "✓" if inv["paid"] else "✗",
            "Date": inv["date"]
        }
        for inv in invoices
    ]

    print(f"\n=== {title} ({len(invoices)}) ===")
    print(tabulate(rows, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    from storage import load_json
    from pathlib import Path

    invoices = load_json(Path("data/invoices.json"))

    print_invoices_table(invoices, "Все счета")
    print_invoices_table(filter_unpaid(invoices), "Неоплаченные счета")

    print(f"\nВсего на руках: ${total_amount(invoices):,.2f}")
    print(f"К получению: ${total_amount(filter_unpaid(invoices)):,.2f}")
