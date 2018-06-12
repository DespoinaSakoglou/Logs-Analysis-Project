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
- results.txt - contains the printed results from running the program.
- output_screenshot.png - a screenshot of the results on the command line.

## Required Libraries and Dependencies
- PostgreSQL
- Python code in DB-API
- Linux-based virtual machine (VM) Vagrant

## How to Run the Project
Download and install the Linux-based virtual machine (VM), which includes all the necessary software (including PostgreSQL) to run the application.
1) Install [Vagrant](https://www.vagrantup.com/)
2) Install [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
3) Clone this repository to your computer in a directory of your choice
4) Start the VM from your terminal, inside the vagrant directory:
   * run the command ```vagrant up``` to start up the VM
   * run the command ```vagrant ssh``` to log into the VM
   * change to your vagrant directory: ```cd /vagrant```
5) Download the data:
   Unzip the file after downloading. Put the file newsdata.sql into the vagrant directory which is shared with your VM.
6) Load the database:
   ```psql -d news -f newsdata.sql```
7) Run the program:
   ```python news.py```
   
## Views Used
The program creates the following views when running the queries on the command line:
* **top_articles**
```SQL 
create or replace view top_articles as
select articles.title, count(*) as total_views
from articles, log
where log.status like '%200%'
and log.path like concat('%', articles.slug, '%')
group by articles.title order by total_views desc limit 3;
```

* **top_authors**
```SQL
create or replace view top_authors as
select authors.name, count(*) as total_views
from authors, articles, log
where articles.author = authors.id
and log.status like '%200%'
and log.path like concat('%', articles.slug, '%')
group by authors.name order by total_views desc;
```

* **status_errors**
```SQL
create or replace view status_errors as
select * from
(select time::timestamp::date as Date,
 round((sum(case log.status when '404 NOT FOUND' then 1 else 0 end)*100.0)/count(log.status), 2)
 as error_percent from log
 group by time::timestamp::date order by error_percent desc)
as subq where error_percent >1;
```
## Output

![](/output_screenshot.png)
