--
-- CREATE VIEW statement for each query
--

--
-- Query 1: What are the 3 most popular articles of all time?
--
CREATE VIEW top_articles AS
    SELECT articles.title, count(*) AS total_views
    FROM articles, log
    WHERE log.status like '%200%'
    AND log.path = '/article' || articles.slug
    GROUP BY articles.title
    ORDER BY total_views DESC
    LIMIT 3;

--
-- Query 2: Who are the most popular article authors of all time?
--
CREATE VIEW top_authors AS
    SELECT authors.name, count(*) AS total_views
    FROM authors, articles, log
    WHERE articles.author = authors.id
    AND log.status like '%200%'
    AND log.path = '/article' || articles.slug
    GROUP BY authors.name
    ORDER BY total_views DESC;

--
--Query 3: On which days did more than 1% of requests lead to errors?
--
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
