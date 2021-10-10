-- valid query
with downloads as
(
select count(*) as n -- adding comments throughout file
  from `bigquery-public-data.samples.github_timeline` -- to make sure
 where repository_has_downloads is true -- that it doesn't break anything
)
,nested as
(
select count(*) as n
  from `bigquery-public-data.samples.github_nested`
)
,trigrams as
(
select count(*) as n
  from `bigquery-public-data.samples.trigrams`
)
select n
    from downloads