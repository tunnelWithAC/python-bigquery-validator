-- valid query
with downloads as
(
select count(*) as n -- adding comments throughout file
  from `{{ params.project }}.samples.github_timeline` -- to make sure
 where repository_has_downloads is true -- that it doesn't break anything
)
,nested as
(
select count(*) as n
  from `{{ params.project }}.samples.github_nested`
)
,trigrams as
(
select count(*) as n
  from `{{ params.project }}.samples.trigrams`
)
select n
    from downloads
