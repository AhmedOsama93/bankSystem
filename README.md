# 🏦 Simple Bank System Implementation

This repository contains a simple, pure Python solution to implement a basic bank system. It manages customer creation, lending with simple interest, processing repayments, and calculating outstanding debt while adhering to strict overpayment prevention rules.

## 📝 Challenge Requirements

### Functional Requirements
* **Customer Management:** Create and register new customers with profile details.
* **Lending:** Issue loans at a specified simple interest rate.
* **Repayment:** Process payments and maintain an accurate running total of repayments.
* **Overpayment Prevention:** **Crucially, prevent customers from paying back more than their outstanding debt.**
* **Status Reporting:** Return a customer's total repayments and outstanding debt.

### Non-Functional Requirements
* Implemented using **pure Python** (standard library only).
* Code is well-documented with clear type hints and docstrings.
* Comprehensive unit tests are provided using the built-in `unittest` module.

---

## 🛠️ Technical Design and SOLID Analysis

The system employs a clean Object-Oriented Design (OOD) with clear separation of responsibilities, promoting extensibility and maintainability.

### 1. Class Structure

| Class | Role | Responsibility |
| :--- | :--- | :--- |
| **`Customer`** | **Data Model / Loan State** | Calculates total debt based on loan terms, tracks payments, and reports current status. |
| **`BankSystem`** | **Business Logic / Registry** | Manages the customer dictionary, handles lending flow, and enforces business rules (like overpayment prevention). |

### 2. SOLID Principles in Design

The structure is built to adhere to the core tenets of SOLID:

| Principle | Adherence in Codebase |
| :--- | :--- |
| **S**ingle **R**esponsibility Principle (SRP) | Strongly enforced. `Customer` handles **only loan math/state**, while `BankSystem` handles **only registry/flow control**. Neither class is burdened with the other's duties. |
| **O**pen/**C**losed Principle (OCP) | Ready for extension. The core `BankSystem` logic remains closed to modification if a new feature is added to the `Customer` data model (e.g., adding a new profile field). |
| **Liskov Substitution Principle (LSP)** | Satisfied by the current structure, which avoids complex inheritance but prepares for it. |
| **Interface Segregation Principle (ISP)** & **Dependency Inversion Principle (DIP)** | While not strictly required for this scale, the separation of `Customer` state from `BankSystem` logic creates natural boundaries, making it straightforward to introduce abstract interfaces (`ILoanAccount`) for a future enterprise application. |

---

## 🔬 Handling Edge Cases

A critical component of financial applications is dealing with precision and business constraints.

| Edge Case | Solution Implemented | Rationale |
| :--- | :--- | :--- |
| **Floating-Point Imprecision** | All financial calculations (`total_debt_owed`, `get_outstanding_debt`) are explicitly **rounded to two decimal places** using `round(value, 2)`. | Ensures reliable comparisons (e.g., $120.00$ vs $120.00000000000003$) and accurate currency display. |
| **Overpayment** | The `receive_repayment` method caps the `actual_paid` amount at the `outstanding_debt` if the user attempts to pay more. | Enforces the core challenge requirement. |
| **Zero/Negative Loan or Repayment** | Input validation is performed in `lend`, and repayments on fully cleared debt (`outstanding_debt <= 0`) are safely rejected. | Prevents invalid state transitions. |

---

## 🚀 How to Run the Project

### 1. File Structure

Ensure you have the following two files in the same directory:
