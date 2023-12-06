# Polling Analysis

This is the alpha release of a cloud-based application to allow Public First to generate polling tables. Please be aware that this version does not yet have all the features that a full release will have and bugs are to be expected.

## User Manual

### Logging in

*Currently users cannot sign up for a new account and access to the calculation portion of this application is restricted*

<details>
<summary>Weighting data</summary>

### Weighting data provided by Alchemer

In order to weight survey data click on the link that says 'click here to weight survey responses'. From this page you will be prompted to upload 2 files. The first should be the survey data provided by Alchemer and the second should be the standard weighting proportions.

Please note that both of these files should be .xlsx files. Uploading a CSV here will result in a 500 error.

Please note that using a different set of weight proportions will also result in inaccurate weights or a 500 error.

Upon successful completion of weighting, users will be redirected to the home page from where you selected the weighting option.

To download your weighted data, click on the link near the bottom of the home page entitled 'DOWNLOAD WEIGHTED DATA'. If all has gone well, the data will be downloaded to your machine. You may then open the file and scroll to the furthest column to the right and see a new column called 'weighted_respondents' which should contain the weights for each person who answered the survey.

If you wish to skip the weighting process for your survey, you will need to manually add a column with the name 'weighted_respondents' to the unweighted data and assign each respondent a value of 1. Automating this for unweighted surveys has not yet been implemented in this version of the application.
</details>

<details>
<summary>Calculations</summary>

### Running the calculations

This section will do broadly 3 things.
1. Work out the total number of people who belong in each cross break that you have selected.
1. Work out how the whole sample answered each question and how each crossbreak answered them.
1. Identify which questions were not answered by the entire sample and display their results as a percentage of those who *did* answer.

First, click on the link: 'Click here to run calculations for crossbreaks'

You will then be taken to a form where you can upload your weighted data. You will also need to enter the ID of the survey which can be found on the first page of the survey's survey legend.

Optionally, you can check or uncheck any standard crossbreaks that you would like to see data for. You can also specify non-standard crossbreaks for which you would like to see data for as well. This step is also optional. 

You may add as many non-standard crossbreaks as you like using the buttons, but note that the more you add, the longer it will take to process the whole batch.

When you're happy with your query, click the 'upload' button to run the calculations.

When the calculations are complete you will be redirected to the home page, and the data will be cached for you to download. Currently you will have 5 minutes until the cached data is wiped from the memory. 

Please also note that refreshing the browser / leaving the app untouched for too long may result in the cached data being cleared as well. If this happens you will need to restart the process again.

Cick 'DOWNLOAD CROSSBREAKS DATA' to save the data for the next step.

**NOTE: please refrain from submitting this form multiple times in quick succession as it relies upon a 3rd party API with limits on the number of requests that can be made per minute. If in doubt, give it 20 seconds or so after submitting to submit again.**
</details>

<details>
<summary>Polling Tables</summary>

### Making Polling Tables

This page will allow you to specify custom labels for questions that have a different base (i.e., the total sample of all respondents).

First, click on the link 'click here to scan the table for rebase comments'. This will take you to a page where you can upload the results you just downloaded from the previous step.

You will then be taken to a general form where you'll need to reupload the data, specify a title for the tables, and select which questions to include in the tables.

Underneath this there will be a form to specify the rebase comments for rebased questions. The app will still work if you do not fill these in but in most cases these will all need to be filled in so that the polling table's numbers make sense.

Once you're happy with all the data in this form, click the 'run table-maker' button. After a few moments, you should be taken back to the home page. From here, you can click the 'Download polling tables button' to download your shiny new polling tables.

The tables themselves should have a 'cover page' worksheet, contents worksheet, full results page (detailing all the questions and all the answers), and a sheet for each individual question.
</details>

## Technical Design

### Database Schema

The Application does not currently require a large database to handle lots of user data. Currently the only models in use are the default django user model and a custom profile model. These are connected in a one-to-one relationship.

The profile model is configured to auto-generate an un-approved profile for each new user that is registered on the system. An admin can then log into the django admin page and update a user's profile approval status, enabling them access to the features of the application.

<img src="docs/db_schema.png" alt="A diagram of the database models" />

This database schema may be expanded in future as features are added to this application.

## Caching Database

This application uses caching to store data processed in the instance's memory for quick retrieval and download by the user.

Currently this is handled using django's default caching system. This works OK for our current use-case but has some potential drawbacks if the application was ever scaled to cater for more users.
1. There is limited configuration/features for more advanced caching.
2. Caching using django's built-in caching system does not easily allow you to profile the impact on performance.
3. More critically, Django uses the application instance's own memory to store cached data. If the application were to be scaled up, the cloud computing cost of running would increase significantly, as cloud run instances are billed according to memory/CPU usage.
4. Given that the cache occupies memory, it also means that there are fewer resources in a cloud run instance that can be devoted to processing data.

Longer-term, it would be better to set up a dedicated, specialised caching database with a service like Redis (or an equivalent provision from Google Cloud). This would ideally allow us to see more analytics on caching usage, and performance, as well as limiting runaway memory usage in the application.

### Data processing

The Pandas library for python is currently used to do the heavy lifting of data processing in the backend.

The following diagrams show the different processes that this project carries out on the survey data.

#### Weighting
<img src="docs/weighting.png" alt="A diagram of the iterative proportional fitting carried out by this application" />

#### Calculating Crossbreaks
<img src="docs/polling_crossbreaks_diagram.png" alt="A diagram of how the crossbreaks processing works." />

### Producing Excel Files

In order to produce excel outputs of the polling table data, this project makes use of 2 libraries:

* [Xlsxwriter](https://xlsxwriter.readthedocs.io/)
* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)

The combination of the two of these enables the application to:
1. Efficiently *write* pandas dataframes to excel files with simple formatting. This is important because each question in the survey needs to have it's own excel sheet displaying the results, which can mean the excel file may contain hundreds of sheets. Being able to do this quickly reduces the performance bottleneck here. Xlsxwriter is designed for this purpose.
2. Implement style and format changes to the excel files that require the ability to read. For example, the headers that designate each set of crossbreaks are much more simply implemented if python can read the excel file and see exactly where each header needs to go. In order to do this with xlsxwriter, the headers would need to be added to the pandas dataframe beforehand which would be needlessly fiddly, and potentially slower.

There are some downsides, however to using both of these libraries together. Since they both alter the XML that makes up an excel file's structure in different ways, it's possible they may interfere with one another.

One example of this is writing hyperlinks to cells in xlsxwriter, then inserting rows (or performing other formatting changes) with openpyxl immediately after. I found this to cause the links to be completely wiped in the excel output, and they needed to be re-written with openpyxl instead.

## Front-End Design

### Wireframes

## Local development and Deployment