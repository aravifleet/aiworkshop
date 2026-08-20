# User Story: PANTHEON-101 - IndieCommerce Checkout Process

## Story Title

As a bookstore customer, I want to add books to my cart and proceed through checkout so that I can purchase products online.

## Story Description

Validate the checkout journey for the IndieCommerce storefront hosted on Pantheon. The flow should allow a signed-in customer to browse a product, add it to the cart, review cart contents, enter checkout information when applicable, and continue toward order submission with clear feedback at each step.

## Application URL

https://test-icsample1657400753.pantheonsite.io/

## Test Credentials

- Username: aravi+temp2@fleetstudio.com
- Password: Fleet@1994

## Acceptance Criteria

### AC1: Customer Login

- GIVEN I am a returning customer
- WHEN I navigate to the login experience
- THEN I should be able to sign in with valid credentials
- AND I should land in an authenticated account or shopping context

### AC2: Add Product to Cart

- GIVEN I am signed in
- WHEN I open a product detail page
- THEN I should be able to add the product to the cart
- AND the cart should reflect the added item

### AC3: Cart Review

- GIVEN I have at least one item in my cart
- WHEN I open the cart page
- THEN I should see cart contents and quantity controls
- AND I should see an action to continue to checkout

### AC4: Checkout Entry

- GIVEN I am on the cart page with items
- WHEN I choose the checkout action
- THEN I should be redirected into the checkout flow
- AND any required customer or shipping fields should be visible

### AC5: Checkout Validation

- GIVEN I am in the checkout flow
- WHEN I leave required fields empty or invalid
- THEN I should see validation feedback
- AND I should not be able to continue until the required data is provided

## Business Rules

1. A customer must be able to authenticate before protected purchase actions.
2. A product must be addable from a live product page.
3. Cart contents should be visible before checkout.
4. Checkout should only be possible from a meaningful cart state.
5. Any missing checkout fields should be surfaced clearly to the customer.

## Technical Notes

- Use Playwright for browser automation.
- Prefer adaptive selector discovery because this app is not Saucedemo-based.
- Validate the real UI flow discovered on the live site instead of assuming fixed routes.
- Generate a gap report if the live application structure differs from the story expectations.

## Checkout Preferences

Add as many checkout preference blocks as needed. The automation creates one execution path for each block.

### Checkout Preference 1

- Name: House Account full purchase
- Product Selection: First purchasable product
- Address Strategy: Random US address
- Shipping Method: Any
- Payment Method: House Account
- Payment Detail: Random
- Review Before Purchase: Yes
- Complete Purchase: Yes
- Stop After: purchase

### Checkout Preference 2

- Name: Credit card review only
- Product Selection: First purchasable product
- Address Strategy: Random US address
- Shipping Method: UPS Ground
- Payment Method: Credit card
- Payment Detail: Random
- Review Before Purchase: Yes
- Complete Purchase: No
- Stop After: review

## Definition of Done

- [ ] The adaptive suite reads this story file successfully
- [ ] Login, add-to-cart, cart, and checkout entry are discovered dynamically
- [ ] Story-to-app gaps are documented in generated artifacts
- [ ] Adaptive execution results are saved for review
