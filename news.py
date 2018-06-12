'''
Database code for the Logs Analysis Project
===========================================
Full Stack Web Developer Nanodegree - Udacity
'''

# Shebang line to indicate Python version
#!/usr/bin/env python3

# Project uses a PostgreSQL database
# import psycopg2 Python module to connect to db
import psycopg2


def connect(dbname="news"):
	"""Connect to PostgreSQL db, open and close connection."""
    try:
        db = psycopg2.connect("dbname={}".format(dbname))
        c = db.cursor()
        return db, c
    except:
        print("Could not connect to the database")


# Create a view table for each query
def v_top_articles():
    """Query 1: What are the 3 most popular articles of all time?"""
    try:
        db, c = connect()
        query_1 = "create or replace view top_articles as\
        select articles.title, count(*) as total_views\
        from articles, log\
        where log.status like '%200%'\
        and log.path like concat('%', articles.slug, '%')\
        group by articles.title order by total_views desc limit 3"
        c.execute(query_1)
        db.commit()
        db.close()
    except:
        print("Could not create view top_articles")


def v_top_authors():
    """Query 2: Who are the most popular article authors of all time?"""
    try:
        db, c = connect()
        query_2 = "create or replace view top_authors as\
        select authors.name, count(*) as total_views\
        from authors, articles, log\
        where articles.author = authors.id\
        and log.status like '%200%'\
        and log.path like concat('%', articles.slug, '%')\
        group by authors.name order by total_views desc"
        c.execute(query_2)
        db.commit()
        db.close()
    except:
        print("Could not create view top_authors")


def v_status_errors():
    """Query 3: On which days did more than 1% of requests lead to errors?"""
    try:
        db, c = connect()
        query_3 = "create or replace view status_errors as\
        select * from\
            (select time::timestamp::date as Date,\
            round((sum(case log.status when \
            '404 NOT FOUND' then 1 else 0 end)*100.0)/count(log.status), 2)\
            as error_percent from log\
            group by time::timestamp::date order by error_percent desc)\
        as subq where error_percent >1"
        c.execute(query_3)
        db.commit()
        db.close()
    except:
        print("Could not create view status_errors")


# Use view tables to print results
def top_articles():
    """Prints results for query 1: 3 most popular articles of all time"""
    db, c = connect()
    query = "select * from top_articles"
    c.execute(query)
    result = c.fetchall()
    db.close()
    print("\nThree most popular articles of all time\n")
    for title, total_views in result:
        print(" \"{}\" -- {} views".format(title, total_views))


def top_authors():
    """Prints results for query 2: most popular authors of all time"""
    db, c = connect()
    query = "select * from top_authors"
    c.execute(query)
    result = c.fetchall()
    db.close()
    print("\n\nMost popular article authors of all time\n")
    for name, total_views in result:
        print(" {} -- {} views".format(name, total_views))


def status_errors():
    """Prints results for query 3:
    days in which there are more that 1% errors in requests"""
    db, c = connect()
    query = "select * from status_errors"
    c.execute(query)
    result = c.fetchall()
    db.close()
    print("\n\nDays with more than one percent errors in requests\n")
    for Date, error_percent in result:
        print("{0:%B %d, %Y} -- {1:.2f}% errors".format(Date, error_percent))


if __name__ == '__main__':
    v_top_articles()
    v_top_authors()
    v_status_errors()
    top_articles()
    top_authors()
    status_errors()
