# Logs Analysis Project
This project is part of the Udacity Full Stack Web Developer Nanodegree program.

## Description
A python program that builds an internal reporting tool that uses information from a database and analyzes the data.
The database is from a newspaper site and contains articles, as well as the web server log for the site.
The program connects to the database, uses SQL queries to analyze the log data and prints out the answers to some questions.

The database includes three tables:
- The **authors** table includes information about the authors of articles.
- The **articles** table includes the articles themselves.
- The **log** table includes one entry for each time a user has accessed the site.

The reporting tool should answer the following questions:
- What are the three most popular articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

## Contents
The project consists of the following files:
- news.py - contains the python script to run.
- create_views.sql - contains the ```SQL CREATE VIEW table``` statements and the queries used.
- results.txt - contains the printed results from running the program.
- output_screenshot.png - a screenshot of the results on the command line.

## Required Libraries and Dependencies
- PostgreSQL
- Python code in DB-API
- Linux-based virtual machine (VM) Vagrant

## How to Run the Project
Download and install the Linux-based virtual machine (VM), which includes all the necessary software (including PostgreSQL) to run the application.
1) Install [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
   Install the platform package for your operating system. You do not need the extension pack or the SDK.
2) Install [Vagrant](https://www.vagrantup.com/)
3) Clone this repository to your computer in a directory of your choice
4) Start the VM from your terminal, inside the vagrant directory:
   * run the command ```vagrant up``` to start up the VM
   * run the command ```vagrant ssh``` to log into the VM
   * change to your vagrant directory: ```cd /vagrant```
   Files in the VM's /vagrant directory are shared with the repository's folder on your computer.
5) Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
   Unzip the file after downloading. Put the file newsdata.sql into the vagrant directory which is shared with your VM.
6) Load the database:
   ```psql -d news -f newsdata.sql```
7) Create the VIEW tables from create_views.sql:
   ```psql -d news -f create_views.sql```
8) Run the program:
   ```python3 news.py```
   
## Views Used
The program creates the following views when loading create_views.sql on the command line:
* **top_articles**
```SQL 
CREATE VIEW top_articles AS
    SELECT articles.title, count(*) AS total_views
    FROM articles, log
    WHERE log.status like '%200%'
    AND log.path = '/article' || articles.slug
    GROUP BY articles.title
    ORDER BY total_views DESC
    LIMIT 3;
```

* **top_authors**
```SQL
CREATE VIEW top_authors AS
    SELECT authors.name, count(*) AS total_views
    FROM authors, articles, log
    WHERE articles.author = authors.id
    AND log.status like '%200%'
    AND log.path = '/article' || articles.slug
    GROUP BY authors.name
    ORDER BY total_views DESC;
```

* **status_errors**
```SQL
CREATE VIEW status_errors AS
    SELECT * FROM
        (SELECT time::timestamp::date AS Date,
        round((sum(CASE log.status WHEN
        '404 NOT FOUND' THEN 1 ELSE 0 END)*100.0)/count(log.status), 2)
        AS error_percent
        FROM log
        GROUP BY time::timestamp::date
        ORDER BY error_percent DESC) AS subq
    WHERE error_percent >1;
```
## Output

![](/output_screenshot.png)
