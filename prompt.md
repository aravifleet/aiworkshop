Instructions :

Now you are acting as a AGENTIC AI DEVELOPER and you should be performing by developing an agentic QA framework for developer’s assistance
Build an agentic ai tool, where developers can give the instructions to the agentic AI through .md file or .txt file for what operations to be performed in automation
Use playwright python as automation tool
When a developer uploaded the .md file in the /upload subfolder, this agent must read all the text entered by the developer
Once the agentic AI read the details it will be generating testcases which covering - Happypath/Negative/Edge cases
After that the automation part starts - the agent must read the .md file very carefully and execute each line one by one with priority
Developer document will be mentioning the url at the top of the document, so the agentic ai must not get confuse and follow the instructions only on the specified url
Since the playwright is being used, make sure to scan the DOM structure as example flow below
Example 1 : if user mentioned https://practicetestautomation.com/practice-test-login/ - The agentic AI capture the DOM elements on this page
If the document mention to click the login page, it should click the login page and capture those DOM elements under /dom file
The reason for capturing this DOM is to make sure the agent should learn the pattern and must not depend on the elements for any use cases
Once the test automation has been completed - the output should be stored under /testresults as .txt, .csv and extent reports
All failure cases screenshot should be captured under /failusecases
And make sure those playwright workflow and framework code should be stored under /playwright-scripts

Context :

Im a senior Manual QA
I know a basic high level flow of playwright workflow
Since its a priority requirement for the organization to reduce the QA time we are building these
Make sure the flow is not complicated and human level debugging must also be possible in code level

Input data :

Create a perfect structure in this workspace and dont forget to mention # at top this workspace purpose
The format should be
The main folder name is prototype2
Dom related should be stored under prototype/dom/dom_elements - should be stored for every pages
prototype2/configuration - all types of API keys and other config related files should be stored
prototype2/playwright-script - playwright scripts should be stored in POM format on each run
prototype2/screenshots - all pass vs fail use cases screenshots should be stored in .png
prototype2/docsnew - everytime developer will be uploading the .md file of usecases or scenarios which is to be read by agentic QA and create use cases accordingly
prototype2/usecases - the use cases should be stored here with .txt, .md, .csv
prototype2/reports - the every run report should be created like extent reports
prototype2/main - store what ever necessary files which is helpful to run the agentic qa

Output indicator :  
Output indicator should be very crisp and must not drag other scenarios into it
When a developer uploaded the document under /docsnew - make sure those scenario’s check has been covered
Share the output of use caes as testresults under prototype2/results/results.csv and results.txt, results.md
Do not include technicalterms, in-depth data analysis, or speculation."
