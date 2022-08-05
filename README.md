# Test Framework Template
**"Pop Up Testing"**

The intent is to help get automation running for multiple clients in a short span of time using a "main" repo, and allowing forks of the main repo, accounting for and allowing upstream and downstream changes, while maintaining dependencies with sound software engineering.

**Typical Customer Process:**

When a new customer is added:
 - Fork this repository (1 repository : client)
 - Continue building automation downstream on new client.
	 - If any changes to be added upstream (example: a client uncovers a business need that would be beneficial to all clients):
		 - Push changes upstream
	 -If any changes from another client are added upstream:
		 - Pull changes from upstream


## Automation Matrix:

 - Allows for permutations (See below for exclusivity constraints) of the following:
	 - Browser Testing
		 - Mobile sized browser on:
			 - Mac Window or Linux
				 - Firefox, Safari, Chrome (most versions)
	 - Mobile Testing with Appium
		 - iOS or Android
			 - Safari, Chrome browsers
	 - Most browser window sizes, most resolutions.
	 - Within internal network or public
		 - Usage of saucelabs sc proxy is programmed within
 - See [https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/](https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/) for available configuration combinations

## **Current Implementation:**

**Technology Stack**
(100% offsite)
 - Bitbucket (GIT)
 - Amazon EC2 (linux) 
	 - Hosts each client's automation client (1 x clients)
	 - Hosts jenkins server (which tasks/schedules automation runs)
 - Jenkins (as mentioned, tasks/schedules automation runs)
 - SauceLabs (used to host the automation)
 - SendGrid (used for email of reports) and SendGrid API
 - Written in Python 3
 - Tests driven by nosetests (an extension of unittest)
 - Other python libraries used:
	 - BeautifulSoup4
	 - see ./requirements.txt for others


## Typical Process

- ./util/scripts/launch_script*.sh will
	- set up env variables
	- launch sc proxy if necessary
	- run tests using nosetests parameters
	- [OPTIONAL] - connect to sauce labs to run tests on hosted machines
	- [OPTIONAL] After test run, shut down sc proxy and/or Saucelabs connection
	- create .html and xunit .xml file to report results
	- parse xunit .xml file for relevant info 
	- collect and send .html file along with report email
	- cleanup and archive .html and .xml files
- This script is typically built into a Jenkins server that allows parameterized scheduled and/or on-demand test runs.