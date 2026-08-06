##### **Scenario :**

We have developed a test instance with the url \- [https://practicetestautomation.com/practice-test-login/](https://practicetestautomation.com/practice-test-login/) and we want a exploratory testing , no rules are set, this exploratory testing should generate at least 5 use cases per page.

1. Click all the available links \- Header links and capture each screenshot and store it in /screenshot folder for reference
2. If any click if responsive time take more than \>20 seconds mark it as fail case and update the test results /results
3. Do not forget to generate use cases by exploring the mentioned url and do all possible actions and create use cases contains negative/edge and happy path
4. On every use case run \- make sure the /results folder contains all use cases output in .csv, .md & .txt format
5. Once the use cases has been completed stop the automation run and publish the results as extent report under /reports
6. The test case results should be matches with the results posted across use cases 50 : 50 i.e

#####

#####

##### **Test case 1: Positive LogIn test**

1. Open page
2. Type username **student** into Username field
3. Type password **Password123** into Password field
4. Push **Submit** button
5. Verify new page URL contains **practicetestautomation.com/logged-in-successfully/**
6. Verify new page contains expected text ('Congratulations' or 'successfully logged in')
7. Verify button **Log out** is displayed on the new page

---

##### **Test case 2: Negative username test**

1. Open page
2. Type username **incorrectUser** into Username field
3. Type password **Password123** into Password field
4. Push **Submit** button
5. Verify error message is displayed
6. Verify error message text is **Your username is invalid\!**

---

##### **Test case 3: Negative password test**

1. Open page
2. Type username **student** into Username field
3. Type password **incorrectPassword** into Password field
4. Push **Submit** button
5. Verify error message is displayed
6. Verify error message text is **Your password is invalid\!**
