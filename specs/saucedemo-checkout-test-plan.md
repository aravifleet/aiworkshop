# Saucedemo Checkout Test Plan

## Story
- ID: `SCRUM-101`
- Feature: E-commerce checkout process
- Application: `https://www.saucedemo.com`
- Test user: `standard_user / secret_sauce`

## Objective
Validate the end-to-end checkout flow for a logged-in user, including cart review, checkout information entry, order overview, completion, validation handling, and navigation safety.

## Scope
- In scope:
  - Cart review and cart-to-checkout flow
  - Required-field validation on checkout info
  - Order overview details and totals
  - Order completion and post-completion navigation
  - Cancel, continue shopping, and direct navigation behavior
  - Browser coverage through Playwright projects
- Out of scope:
  - Real payment processing
  - Backend/API verification
  - Non-checkout product catalog behavior unrelated to checkout

## Test Data
| ID | First Name | Last Name | Postal Code | Items | Purpose |
| --- | --- | --- | --- | --- | --- |
| TD01 | John | Doe | 12345 | Sauce Labs Backpack | Happy path |
| TD02 | Jane | Smith | 560001 | Backpack + Bike Light | Multi-item totals |
| TD03 |  | Doe | 12345 | Backpack | Missing first name |
| TD04 | John |  | 12345 | Backpack | Missing last name |
| TD05 | John | Doe |  | Backpack | Missing postal code |
| TD06 | @#! | Doe | 12345 | Backpack | Invalid first name |
| TD07 | John | 1234 | 12345 | Backpack | Invalid last name |
| TD08 | John | Doe | 12 | Backpack | Short postal code |
| TD09 | John | Doe | ABCDE | Backpack | Non-numeric postal code |

## Preconditions
- The application is reachable.
- The test user can sign in successfully.
- Each test starts from a clean session unless otherwise stated.

## Scenarios

### Happy Path
| ID | Title | Coverage |
| --- | --- | --- |
| HP01 | Complete checkout with one item | AC1, AC2, AC3, AC4 |
| HP02 | Complete checkout with two items and verify totals | AC1, AC3, AC4 |
| HP03 | Continue shopping from cart and preserve cart state | AC1 |
| HP04 | Use Back Home after successful order completion | AC4 |

### Negative
| ID | Title | Coverage |
| --- | --- | --- |
| NG01 | Leave first name empty | AC2 |
| NG02 | Leave last name empty | AC2 |
| NG03 | Leave postal code empty | AC2 |
| NG04 | Submit all checkout info fields empty | AC2 |
| NG05 | Enter special characters in first name | AC5 |
| NG06 | Enter numeric last name | AC5 |
| NG07 | Enter invalid postal code format | AC5 |
| NG08 | Attempt checkout with empty cart | BR3 |
| NG09 | Open checkout pages while logged out | BR2 |

### Edge and Navigation
| ID | Title | Coverage |
| --- | --- | --- |
| EC01 | Remove item before checkout and verify cart updates | AC1 |
| EC02 | Cancel from checkout information page | BR5 |
| EC03 | Cancel from checkout overview page | BR5 |
| EC04 | Verify order completion clears cart | BR4 |
| EC05 | Verify browser back behavior across checkout steps | Technical notes |
| EC06 | Validate direct URL protection for overview/complete | BR2, flow integrity |
| EC07 | Validate overview math for subtotal, tax, and total | AC3 |

### UI Validation
| ID | Title | Coverage |
| --- | --- | --- |
| UI01 | Cart page shows name, description, price, quantity, and CTA buttons | AC1 |
| UI02 | Checkout info page shows all mandatory inputs and buttons | AC2 |
| UI03 | Error banner appears and blocks navigation on invalid required data | AC2, AC5 |
| UI04 | Overview page shows items, payment info, shipping info, subtotal, tax, total | AC3 |
| UI05 | Completion page shows success text and Back Home button | AC4 |

## Detailed Cases

### HP01: Complete Checkout With One Item
1. Sign in with the valid test user.
2. Add `Sauce Labs Backpack` to the cart.
3. Open the cart.
4. Verify item name, description, price, quantity, and visible `Continue Shopping` and `Checkout` buttons.
5. Click `Checkout`.
6. Enter `TD01`.
7. Click `Continue`.
8. Verify the overview page shows the selected item, payment info, shipping info, subtotal, tax, and total.
9. Click `Finish`.
10. Verify the confirmation page shows success content and `Back Home`.

Expected result:
- Each page transition succeeds.
- The same item remains present from cart through overview.
- The order completes successfully.

### HP02: Complete Checkout With Two Items And Verify Totals
1. Sign in with the valid test user.
2. Add `Sauce Labs Backpack` and `Sauce Labs Bike Light`.
3. Open the cart and verify both items.
4. Start checkout and enter `TD02`.
5. Continue to overview.
6. Verify subtotal equals the sum of item prices.
7. Verify total equals subtotal plus tax.
8. Finish the order successfully.

Expected result:
- Two items persist through cart and overview.
- Calculated amounts are internally consistent.

### NG01-NG04: Required Field Validation
1. Sign in and add one item.
2. Open cart and start checkout.
3. Leave the targeted field blank.
4. Click `Continue`.

Expected result:
- The user remains on the checkout info page.
- An error banner appears with the correct required-field message.

### NG05-NG07: Invalid Data Validation
1. Sign in and add one item.
2. Open cart and start checkout.
3. Enter the invalid data set.
4. Click `Continue`.

Expected result:
- The user is blocked with a validation message.
- If the application allows invalid data to proceed, log it as a defect against AC5.

### EC02: Cancel From Checkout Information
1. Sign in and add one item.
2. Open cart and click `Checkout`.
3. Click `Cancel`.

Expected result:
- The user returns to the cart.
- The cart contents remain intact.

### EC03: Cancel From Checkout Overview
1. Sign in and add one item.
2. Proceed through checkout info with valid data.
3. Click `Cancel` on the overview page.

Expected result:
- The user returns to the inventory page.
- Cart state is preserved until checkout is completed.

### EC04: Order Completion Clears Cart
1. Complete a successful order.
2. Click `Back Home`.
3. Open the cart.

Expected result:
- The cart is empty after a successful order.

### EC06: Direct URL Protection
1. Sign out or start a fresh logged-out session.
2. Attempt to open cart, checkout info, overview, and complete URLs directly.

Expected result:
- Unauthenticated access is blocked or redirected appropriately.

## Coverage Matrix
| Requirement | Covered By |
| --- | --- |
| AC1 Cart review | HP01, HP02, HP03, EC01, UI01 |
| AC2 Checkout info entry | HP01, NG01, NG02, NG03, NG04, UI02, UI03 |
| AC3 Order overview | HP01, HP02, EC07, UI04 |
| AC4 Order completion | HP01, HP04, EC04, UI05 |
| AC5 Error handling | NG05, NG06, NG07, UI03 |
| BR1 Mandatory fields | NG01, NG02, NG03, NG04 |
| BR2 Login required | NG09, EC06 |
| BR3 Cart cannot be empty | NG08 |
| BR4 Confirmation clears cart | EC04 |
| BR5 Cancel flow | EC02, EC03 |

## Risks
- The story expects stronger invalid-data validation than Saucedemo may actually enforce.
- Empty-cart and direct-URL behaviors may expose gaps versus the business rules.
- Cross-browser timing could differ on checkout transitions, so waits should target page state instead of fixed delays.
