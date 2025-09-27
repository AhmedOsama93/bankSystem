from typing import Optional, Dict, Tuple
import unittest


class Customer:

    def __init__(self, name: str, nationality: str, email: str, nationality_id: str, principal_amount: float,
                 interest_rate: float):
        """Customer profile Fields and loan Fields and Calculate the fixed total debt using simple interest"""
        # Profile Fields
        self.name = name
        self.nationality = nationality
        self.email = email
        self.nationality_id = nationality_id

        self.principal_amount = principal_amount
        self.interest_rate = interest_rate
        self.total_repayments = 0.0

        self.total_debt_owed = round(self.principal_amount * (1 + self.interest_rate), 2)

    # calculate outstanding debt
    def get_outstanding_debt(self) -> float:
        return round(self.total_debt_owed - self.total_repayments, 2)

    # return current status of customer total repayments and outstanding debt
    def get_status(self) -> Tuple[float, float]:
        return self.total_repayments, self.get_outstanding_debt()


class BankSystem:

    def __init__(self):
        self.customers: Dict[str, Customer] = {}

    # create customer fields with initial value for principal_amount=0.0 and interest_rate=0.0
    def create_customer(self, name: str, nationality: str = "", email: str = "", nationality_id: str = "") -> Optional[
        Customer]:

        if name in self.customers:
            print(f"Error: Customer '{name}' already exists.")
            return None

        customer = Customer(name, nationality, email, nationality_id, principal_amount=0.0, interest_rate=0.0)
        self.customers[name] = customer
        print(f"Customer profile for '{name}' created successfully.")
        return customer

    def check_customer_exist(self, name: str) -> bool:
        if name not in self.customers:
            print(f"Error: Customer '{name}' does not exist. Cannot issue loan.")
            return False
        return True

    # customer can lend money and lend with interest_rate
    def lend(self, name: str, amount: float, interest_rate: float) -> bool:
        if not self.check_customer_exist(name):
            return False

        if amount <= 0:
            print("Error: Loan amount must be positive.")
            return False

        current_customer = self.customers[name]

        self.customers[name] = Customer(
            name,
            current_customer.nationality,
            current_customer.email,
            current_customer.nationality_id,
            principal_amount=amount,
            interest_rate=interest_rate
        )

        total_debt = self.customers[name].total_debt_owed
        print(f"Loan granted to {name}: ${amount:,.2f} at {interest_rate * 100:.1f}% interest.")
        print(f"Total debt (including interest): ${total_debt:,.2f}")
        return True

    # customer can repayment and should Prevent customers from paying back more than they owe
    def receive_repayment(self, name: str, amount: float) -> Optional[float]:

        customer = self.customers.get(name)
        if not self.check_customer_exist(name):
            return None

        outstanding_debt = customer.get_outstanding_debt()

        if outstanding_debt <= 0:
            print(f"Notice: {name} has already settled their outstanding debt. Payment rejected.")
            return 0.0

        if amount > outstanding_debt:
            actual_paid = outstanding_debt
            print(f"Warning: Attempted payment of ${amount:,.2f} exceeds outstanding debt.")
            print(f"Only ${actual_paid:,.2f} accepted to settle the debt.")
        else:
            actual_paid = amount
            print(f"Repayment received from {name}: ${actual_paid:,.2f}")

        customer.total_repayments += actual_paid
        return actual_paid

    def get_customer_status(self, name: str) -> Optional[Dict[str, float]]:

        customer = self.customers.get(name)
        if not customer:
            print(f"Error: Customer '{name}' not found.")
            return None

        total_repayments, debt = customer.get_status()
        return {
            "total_repayments": total_repayments,
            "outstanding_debt": debt
        }


# --- Helper data for customer creation ---
CUSTOMER_PROFILE = {
    "name": "Alice Smith",
    "nationality": "Canadian",
    "email": "alice@test.com",
    "nationality_id": "987654"
}


class TestCustomer(unittest.TestCase):
    """Tests for the individual Customer class logic and attribute handling."""

    def test_initial_loan_calculation_and_profile(self):
        """Test the calculation of total debt and persistence of profile data."""
        principal = 1000.00
        rate = 0.05
        # Total debt = 1000 * 1.05 = 1050.00
        c = Customer(**CUSTOMER_PROFILE, principal_amount=principal, interest_rate=rate)

        # Profile checks
        self.assertEqual(c.name, "Alice Smith")
        self.assertEqual(c.nationality, "Canadian")
        self.assertEqual(c.email, "alice@test.com")
        self.assertEqual(c.nationality_id, "987654")

        # Loan checks
        self.assertAlmostEqual(c.principal_amount, principal)
        self.assertAlmostEqual(c.interest_rate, rate)
        self.assertAlmostEqual(c.total_debt_owed, 1050.00)
        self.assertAlmostEqual(c.total_repayments, 0.0)
        self.assertAlmostEqual(c.get_outstanding_debt(), 1050.00)

    def test_repayment_updates(self):
        """Test how repayments affect outstanding debt with rounding applied."""
        c = Customer(**CUSTOMER_PROFILE, principal_amount=500.00, interest_rate=0.10)  # Total debt = $550.00
        c.total_repayments = 200.00
        self.assertAlmostEqual(c.total_repayments, 200.00)
        # Debt: 550.00 - 200.00 = 350.00
        self.assertAlmostEqual(c.get_outstanding_debt(), 350.00)

    def test_get_status(self):
        """Test the combined status reporting tuple."""
        c = Customer(**CUSTOMER_PROFILE, principal_amount=100.00, interest_rate=0.20)  # Total debt = $120.00
        c.total_repayments = 50.00
        repayments, debt = c.get_status()
        self.assertAlmostEqual(repayments, 50.00)
        self.assertAlmostEqual(debt, 70.00)


class TestBankSystem(unittest.TestCase):
    """Tests for the BankSystem class and its business logic."""

    def setUp(self):
        """Set up a fresh BankSystem instance before each test."""
        self.bank = BankSystem()
        # Create a base customer for most tests
        self.bank.create_customer("Bob", "US", "bob@test.com", "112233")

    # --- Utility Test (check_customer_exist) ---
    def test_check_customer_exist(self):
        """Verify the customer existence check utility method works."""
        self.assertTrue(self.bank.check_customer_exist("Bob"))
        self.assertFalse(self.bank.check_customer_exist("Noname"))

    # --- Customer Creation Tests ---
    def test_create_customer_successful(self):
        """Verify new customer creation and profile data storage."""
        cust = self.bank.create_customer("Charlie", "UK", "charlie@test.co.uk", "C123")
        self.assertIsNotNone(cust)
        self.assertIn("Charlie", self.bank.customers)
        self.assertEqual(cust.nationality, "UK")

    def test_create_duplicate_customer(self):
        """Verify that duplicate customer creation is prevented."""
        # 'Bob' is created in setUp, attempt to create again.
        self.assertIsNone(self.bank.create_customer("Bob", "AU", "new@bob.com", "112233"))

    # --- Lending Tests ---
    def test_lend_successful(self):
        """Verify successful loan issuance and debt calculation."""
        self.assertTrue(self.bank.lend("Bob", 600.00, 0.10))
        status = self.bank.get_customer_status("Bob")
        # Total debt = 600 * 1.10 = 660.00
        self.assertAlmostEqual(status['outstanding_debt'], 660.00)
        self.assertAlmostEqual(status['total_repayments'], 0.0)
        # Verify profile data persists after re-lending
        self.assertEqual(self.bank.customers["Bob"].nationality, "US")

    def test_lend_non_existent_customer(self):
        """Verify lending fails for a non-existent customer."""
        self.assertFalse(self.bank.lend("Noname", 100.00, 0.10))

    def test_lend_zero_amount(self):
        """Verify lending fails for zero or negative amount."""
        self.assertFalse(self.bank.lend("Bob", 0.00, 0.10))
        self.assertFalse(self.bank.lend("Bob", -50.00, 0.10))

    # --- Repayment Tests ---
    def test_receive_repayment_partial(self):
        """Test a partial repayment."""
        self.bank.lend("Bob", 100.00, 0.20)  # Total debt = $120.00
        actual_paid = self.bank.receive_repayment("Bob", 50.00)
        self.assertAlmostEqual(actual_paid, 50.00)
        status = self.bank.get_customer_status("Bob")
        self.assertAlmostEqual(status['total_repayments'], 50.00)
        self.assertAlmostEqual(status['outstanding_debt'], 70.00)  # 120 - 50 = 70

    def test_receive_repayment_overpayment_prevention(self):
        """Test the core requirement to prevent paying more than owed."""
        self.bank.lend("Bob", 100.00, 0.20)  # Total debt = $120.00
        # Attempt to pay $150 when only $120 is owed
        actual_paid = self.bank.receive_repayment("Bob", 150.00)
        # Should only accept the outstanding debt of $120.00
        self.assertAlmostEqual(actual_paid, 120.00)
        status = self.bank.get_customer_status("Bob")
        self.assertAlmostEqual(status['outstanding_debt'], 0.00)
        self.assertAlmostEqual(status['total_repayments'], 120.00)

    def test_repayment_on_zero_debt(self):
        """Test repayment on a fully paid loan."""
        self.bank.lend("Bob", 100.00, 0.0)  # Total debt = $100.00
        self.bank.receive_repayment("Bob", 100.00)
        # Second attempt to pay
        actual_paid = self.bank.receive_repayment("Bob", 10.00)
        self.assertAlmostEqual(actual_paid, 0.0)
        status = self.bank.get_customer_status("Bob")
        self.assertAlmostEqual(status['outstanding_debt'], 0.00)
        self.assertAlmostEqual(status['total_repayments'], 100.00)

    def test_receive_repayment_non_existent_customer(self):
        """Test repayment fails for a non-existent customer."""
        self.assertIsNone(self.bank.receive_repayment("Noname", 10.00))

    # --- Status Tests ---
    def test_get_customer_status_non_existent(self):
        """Test getting status for a customer who was never created."""
        self.assertIsNone(self.bank.get_customer_status("Invisible"))

    # --- Challenge Scenario Test ---
    def test_challenge_example_scenario(self):
        """Verify the exact scenario provided in the instructions."""
        self.bank.create_customer("Hussein", "EG", "h@test.com", "123")  # New customer creation
        self.bank.lend("Hussein", 200.00, 0.10)  # Total debt = $220.00

        # Step 1: Repays $100
        paid_1 = self.bank.receive_repayment("Hussein", 100.00)
        self.assertAlmostEqual(paid_1, 100.00)

        # Status Check: Repayments $100, Debt $120
        status_1 = self.bank.get_customer_status("Hussein")
        self.assertAlmostEqual(status_1['total_repayments'], 100.00)
        self.assertAlmostEqual(status_1['outstanding_debt'], 120.00)

        # Step 2: Attempted Overpayment of $150
        paid_2 = self.bank.receive_repayment("Hussein", 150.00)
        # Only $120 should be accepted
        self.assertAlmostEqual(paid_2, 120.00)

        # Final Status Check: Repayments $220, Debt $0
        status_2 = self.bank.get_customer_status("Hussein")
        self.assertAlmostEqual(status_2['total_repayments'], 220.00)
        self.assertAlmostEqual(status_2['outstanding_debt'], 0.00)
