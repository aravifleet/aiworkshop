# Use cases generated from exploratorytesting.md
URL: https://test-icsample1657400753.pantheonsite.io/

## TC001 TC001 - TC-test-icsample1657400753-pantheonsite-io-Happy path: positive login
Type: happy
Description: Validate that valid credentials allow the user to log in successfully.
Page URL: https://test-icsample1657400753.pantheonsite.io/user/login?current=/
Instructions:
- fill email with aravi+temp2@fleetstudio.com
- fill password with Fleet@1994
- submit auth form
- verify authenticated state
- capture DOM after login

## TC002 TC002 - TC-test-icsample1657400753-pantheonsite-io-Happy path: positive login and logout
Type: happy
Description: Validate the complete authentication round trip from login through logout.
Page URL: https://test-icsample1657400753.pantheonsite.io/user/login?current=/
Instructions:
- fill email with aravi+temp2@fleetstudio.com
- fill password with Fleet@1994
- submit auth form
- verify authenticated state
- capture DOM after login
- click logout
- verify logout succeeds
- capture DOM after logout

## TC003 TC003 - TC-test-icsample1657400753-pantheonsite-io-Negative path: invalid login is rejected
Type: negative
Description: Validate expected error handling when invalid credentials are submitted.
Page URL: https://test-icsample1657400753.pantheonsite.io/user/login?current=/
Instructions:
- fill email with invalid_email@example.com
- fill password with invalid_pass
- submit auth form
- verify error message appears
- capture DOM after invalid login

## TC004 TC004 - TC-test-icsample1657400753-pantheonsite-io-Negative path: missing login data is validated
Type: negative
Description: Validate required-field behavior for the authentication form.
Page URL: https://test-icsample1657400753.pantheonsite.io/user/login?current=/
Instructions:
- submit required inputs incorrectly
- verify validation or error feedback
- capture DOM after invalid input

## TC005 TC005 - TC-test-icsample1657400753-pantheonsite-io-Edge case: authentication controls remain visible
Type: edge
Description: Check that the login page exposes the expected controls before interaction.
Page URL: https://test-icsample1657400753.pantheonsite.io/user/login?current=/
Instructions:
- verify page loads
- verify auth form is visible
- verify links are visible
- capture DOM after auth form inspection

## TC006 TC006 - Home Page | IndieCommerce: exploratory case 1
Type: exploratory
Description: Auto-generated exploratory case for Home Page | IndieCommerce to click link Cart.
Page URL: https://test-icsample1657400753.pantheonsite.io/
Instructions:
- verify page loads
- capture DOM before actions
- click https://test-icsample1657400753.pantheonsite.io/cart
- verify page loads
- capture DOM after click
- return to previous page
- verify page loads
- capture DOM after going back
- verify links are visible
- submit required inputs incorrectly

## TC007 TC007 - Home Page | IndieCommerce: exploratory case 2
Type: exploratory
Description: Auto-generated exploratory case for Home Page | IndieCommerce to click link About.
Page URL: https://test-icsample1657400753.pantheonsite.io/
Instructions:
- verify page loads
- capture DOM before actions
- click https://test-icsample1657400753.pantheonsite.io/about-us
- verify page loads
- capture DOM after click
- return to previous page
- verify page loads
- capture DOM after going back

## TC008 TC008 - Home Page | IndieCommerce: exploratory case 3
Type: exploratory
Description: Auto-generated exploratory case for Home Page | IndieCommerce to click link Books.
Page URL: https://test-icsample1657400753.pantheonsite.io/
Instructions:
- verify page loads
- capture DOM before actions
- click https://test-icsample1657400753.pantheonsite.io/books
- verify page loads
- capture DOM after click
- return to previous page
- verify page loads
- capture DOM after going back

## TC009 TC009 - Home Page | IndieCommerce: exploratory case 4
Type: exploratory
Description: Auto-generated exploratory case for Home Page | IndieCommerce to click link Events.
Page URL: https://test-icsample1657400753.pantheonsite.io/
Instructions:
- verify page loads
- capture DOM before actions
- click https://test-icsample1657400753.pantheonsite.io/events
- verify page loads
- capture DOM after click
- return to previous page
- verify page loads
- capture DOM after going back

## TC010 TC010 - Home Page | IndieCommerce: exploratory case 5
Type: exploratory
Description: Auto-generated exploratory case for Home Page | IndieCommerce to click link Log in.
Page URL: https://test-icsample1657400753.pantheonsite.io/
Instructions:
- verify page loads
- capture DOM before actions
- click https://test-icsample1657400753.pantheonsite.io/user/login?current=/
- verify page loads
- capture DOM after click
- return to previous page
- verify page loads
- capture DOM after going back
