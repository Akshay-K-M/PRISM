-- createdb prism_15d
-- pg_dump --schema-only --no-owner --no-privileges prism_10a \
-- | psql -v ON_ERROR_STOP=1 -d prism_15d

psql -v ON_ERROR_STOP=1 -d prism_15d <<'SQL'
BEGIN;

TRUNCATE TABLE
    aka_title,
    company_name,
    company_type,
    info_type,
    keyword,
    movie_companies,
    movie_info,
    movie_keyword,
    title
CASCADE;

-- ---------------------------------------------------------
-- Dimension and lookup tables
-- ---------------------------------------------------------

INSERT INTO company_name (
    id,
    name,
    country_code
) VALUES (
    1,
    'Minimal US Internet Company',
    '[us]'
);

INSERT INTO company_type (
    id,
    kind
) VALUES (
    1,
    'production companies'
);

INSERT INTO info_type (
    id,
    info
) VALUES (
    1,
    'release dates'
);

INSERT INTO keyword (
    id,
    keyword
) VALUES (
    1,
    'internet'
);

-- ---------------------------------------------------------
-- Central title row
-- kind_id is mandatory in the standard JOB schema.
-- Query 15d does not join kind_type, so kind_id = 1 is enough.
-- ---------------------------------------------------------

INSERT INTO title (
    id,
    title,
    kind_id,
    production_year
) VALUES (
    1,
    'Minimal Internet Movie',
    1,
    1991
);

-- ---------------------------------------------------------
-- Alternative title
-- aka_title.kind_id is also mandatory.
-- ---------------------------------------------------------

INSERT INTO aka_title (
    id,
    movie_id,
    title,
    kind_id,
    production_year
) VALUES (
    1,
    1,
    'Minimal Alternative Internet Movie',
    1,
    1991
);

-- ---------------------------------------------------------
-- Release information
-- The note satisfies mi.note LIKE '%internet%'.
-- ---------------------------------------------------------

INSERT INTO movie_info (
    id,
    movie_id,
    info_type_id,
    info,
    note
) VALUES (
    1,
    1,
    1,
    'USA: 1 January 1991',
    'Released on the internet'
);

-- ---------------------------------------------------------
-- Movie keyword
-- ---------------------------------------------------------

INSERT INTO movie_keyword (
    id,
    movie_id,
    keyword_id
) VALUES (
    1,
    1,
    1
);

-- ---------------------------------------------------------
-- Movie company
-- ---------------------------------------------------------

INSERT INTO movie_companies (
    id,
    movie_id,
    company_id,
    company_type_id
) VALUES (
    1,
    1,
    1,
    1
);

COMMIT;

-- ---------------------------------------------------------
-- Verify the number of rows in every table used by 15d
-- ---------------------------------------------------------

SELECT 'aka_title' AS table_name, COUNT(*) AS row_count FROM aka_title
UNION ALL
SELECT 'company_name', COUNT(*) FROM company_name
UNION ALL
SELECT 'company_type', COUNT(*) FROM company_type
UNION ALL
SELECT 'info_type', COUNT(*) FROM info_type
UNION ALL
SELECT 'keyword', COUNT(*) FROM keyword
UNION ALL
SELECT 'movie_companies', COUNT(*) FROM movie_companies
UNION ALL
SELECT 'movie_info', COUNT(*) FROM movie_info
UNION ALL
SELECT 'movie_keyword', COUNT(*) FROM movie_keyword
UNION ALL
SELECT 'title', COUNT(*) FROM title
ORDER BY table_name;
SQL

-- ============= Given Query ===============
-- SELECT at.title AS aka_title,
--        t.title AS internet_movie_title
-- FROM aka_title AS at,
--      company_name AS cn,
--      company_type AS ct,
--      info_type AS it1,
--      keyword AS k,
--      movie_companies AS mc,
--      movie_info AS mi,
--      movie_keyword AS mk,
--      title AS t
-- WHERE cn.country_code = '[us]'
--   AND it1.info = 'release dates'
--   AND mi.note LIKE '%internet%'
--   AND t.production_year > 1990
--   AND t.id = at.movie_id
--   AND t.id = mi.movie_id
--   AND t.id = mk.movie_id
--   AND t.id = mc.movie_id
--   AND mk.movie_id = mi.movie_id
--   AND mk.movie_id = mc.movie_id
--   AND mk.movie_id = at.movie_id
--   AND mi.movie_id = mc.movie_id
--   AND mi.movie_id = at.movie_id
--   AND mc.movie_id = at.movie_id
--   AND k.id = mk.keyword_id
--   AND it1.id = mi.info_type_id
--   AND cn.id = mc.company_id
--   AND ct.id = mc.company_type_id;
    
-- =========== Extracted Query =============
 
--  Select aka_title.title as aka_title, title.title as internet_movie_title 
--  From aka_title, company_name, company_type, info_type, keyword, movie_companies, movie_info, movie_keyword, title 
--  Where keyword.id = movie_keyword.keyword_id
--  and info_type.id = movie_info.info_type_id
--  and company_type.id = movie_companies.company_type_id
--  and company_name.id = movie_companies.company_id
--  and aka_title.movie_id = movie_companies.movie_id
--  and movie_companies.movie_id = movie_info.movie_id
--  and movie_info.movie_id = movie_keyword.movie_id
--  and movie_keyword.movie_id = title.id
--  and company_name.country_code = '[us]'
--  and info_type.info = 'release dates'
--  and movie_info.note LIKE '%internet%'
--  and title.production_year >= 1991;