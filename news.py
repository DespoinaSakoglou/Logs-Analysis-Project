#!/usr/bin/env python3
'''
Database code for the Logs Analysis Project
===========================================
Full Stack Web Developer Nanodegree - Udacity
'''


# Project uses a PostgreSQL database
# import psycopg2 Python module to connect to db
import psycopg2


def connect(dbname="news"):
	"""Connect to PostgreSQL db, open and close connection."""
    try:
        db = psycopg2.connect("dbname={}".format(dbname))
        c = db.cursor()
        return db, c
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def execute_query(query):
    """Take an SQL query, execute it and return the results"""
    try:
        db, c = connect()
        c.execute(query)
        result = c.fetchall()
        db.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Use VIEW tables from create_views.sql to print results
def top_articles():
    """Prints results for query 1: 3 most popular articles of all time"""
    query_1 = """
            SELECT * FROM top_articles;
            """
    result = execute_query(query_1)
    print("\nThree most popular articles of all time\n")
    for title, total_views in result:
        print(" \"{}\" -- {} views".format(title, total_views))


def top_authors():
    """Prints results for query 2: most popular authors of all time"""
    query_2 = """
            SELECT * FROM top_authors;
            """
    result = execute_query(query_2)
    print("\n\nMost popular article authors of all time\n")
    for name, total_views in result:
        print(" {} -- {} views".format(name, total_views))


def status_errors():
    """Prints results for query 3:
    days in which there are more that 1% errors in requests"""
    query_3 = """
            SELECT * FROM status_errors;
            """
    result = execute_query(query_3)
    print("\n\nDays with more than one percent errors in requests\n")
    for Date, error_percent in result:
        print("{0:%B %d, %Y} -- {1:.2f}% errors".format(Date, error_percent))


if __name__ == '__main__':
    top_articles()
    top_authors()
    status_errors()
