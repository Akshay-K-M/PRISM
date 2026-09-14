dropdb --if-exists prism_13d
createdb prism_13d

pg_dump --schema-only --no-owner --no-privileges job \
  | psql -v ON_ERROR_STOP=1 -d prism_13d

psql -v ON_ERROR_STOP=1 -d prism_13d <<'SQL'
BEGIN;

TRUNCATE TABLE
    movie_info_idx,
    movie_info,
    movie_companies,
    company_name,
    company_type,
    info_type,
    kind_type,
    title
CASCADE;

-- 10 US companies
INSERT INTO company_name (
    id,
    name,
    country_code
)
SELECT
    i,
    'US Production Company ' || i,
    '[us]'
FROM generate_series(1, 10) AS g(i);

-- 10 matching company types
INSERT INTO company_type (
    id,
    kind
)
SELECT
    i,
    'production companies'
FROM generate_series(1, 10) AS g(i);

-- 10 rating info-type rows
INSERT INTO info_type (
    id,
    info
)
SELECT
    i,
    'rating'
FROM generate_series(1, 10) AS g(i);

-- 10 movie kind rows
INSERT INTO kind_type (
    id,
    kind
)
SELECT
    i,
    'movie'
FROM generate_series(1, 10) AS g(i);

-- 10 titles
INSERT INTO title (
    id,
    title,
    kind_id,
    production_year
)
SELECT
    i,
    'Movie ' || i,
    i,
    2000 + i
FROM generate_series(1, 10) AS g(i);

-- 10 movie-company associations
INSERT INTO movie_companies (
    id,
    movie_id,
    company_id,
    company_type_id,
    note
)
SELECT
    i,
    i,
    i,
    i,
    'Company record ' || i
FROM generate_series(1, 10) AS g(i);

-- 10 movie-info rows
INSERT INTO movie_info (
    id,
    movie_id,
    info_type_id,
    info
)
SELECT
    i,
    i,
    i,
    'Movie information ' || i
FROM generate_series(1, 10) AS g(i);

-- 10 indexed ratings with exactly two decimal places
INSERT INTO movie_info_idx (
    id,
    movie_id,
    info_type_id,
    info
)
SELECT
    i,
    i,
    i,
    TO_CHAR(
        ROUND(7.00 + i::numeric / 10.00, 2),
        'FM999999990.00'
    )
FROM generate_series(1, 10) AS g(i);

COMMIT;

-- Verify that every referenced table contains 10 rows
SELECT
    'company_name' AS table_name,
    COUNT(*) AS row_count
FROM company_name

UNION ALL
SELECT 'company_type', COUNT(*) FROM company_type

UNION ALL
SELECT 'info_type', COUNT(*) FROM info_type

UNION ALL
SELECT 'kind_type', COUNT(*) FROM kind_type

UNION ALL
SELECT 'movie_companies', COUNT(*) FROM movie_companies

UNION ALL
SELECT 'movie_info', COUNT(*) FROM movie_info

UNION ALL
SELECT 'movie_info_idx', COUNT(*) FROM movie_info_idx

UNION ALL
SELECT 'title', COUNT(*) FROM title

ORDER BY table_name;

-- Verify the exact two-decimal rating values
SELECT
    id,
    movie_id,
    info_type_id,
    info
FROM movie_info_idx
ORDER BY id;
SQL

============= Given Query ===============
SELECT cn.name AS producing_company,
       miidx.info AS rating,
       t.title AS movie
FROM company_name AS cn,
     company_type AS ct,
     info_type AS it,
     kind_type AS kt,
     movie_companies AS mc,
     movie_info AS mi,
     movie_info_idx AS miidx,
     title AS t
WHERE cn.country_code = '[us]'
  AND ct.kind = 'production companies'
  AND it.info = 'rating'
  AND kt.kind = 'movie'
  AND mi.movie_id = t.id
  AND kt.id = t.kind_id
  AND mc.movie_id = t.id
  AND cn.id = mc.company_id
  AND ct.id = mc.company_type_id
  AND miidx.movie_id = t.id
  AND it.id = miidx.info_type_id
  AND mi.movie_id = miidx.movie_id
  AND mi.movie_id = mc.movie_id
  AND miidx.movie_id = mc.movie_id;
    
=========== Extracted Query =============
 
 Select company_name.name as producing_company, movie_info_idx.info as rating, title.title as movie 
 From company_name, company_type, info_type, kind_type, movie_companies, movie_info, movie_info_idx, title 
 Where movie_companies.movie_id = movie_info.movie_id
 and movie_info.movie_id = movie_info_idx.movie_id
 and movie_info_idx.movie_id = title.id
 and kind_type.id = title.kind_id
 and info_type.id = movie_info_idx.info_type_id
 and company_name.id = movie_companies.company_id
 and company_type.id = movie_companies.company_type_id
 and company_name.country_code = '[us]'
 and company_type.kind = 'production companies'
 and info_type.info = 'rating'
 and kind_type.kind = 'movie';