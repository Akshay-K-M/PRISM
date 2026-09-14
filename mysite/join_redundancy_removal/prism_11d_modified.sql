dropdb --if-exists prism_11d
createdb prism_11d

pg_dump --schema-only --no-owner --no-privileges job \
  | psql -v ON_ERROR_STOP=1 -d prism_11d

psql -v ON_ERROR_STOP=1 -d prism_11d <<'SQL'
BEGIN;

TRUNCATE TABLE
    movie_link,
    movie_keyword,
    movie_companies,
    link_type,
    keyword,
    company_type,
    company_name,
    title
CASCADE;

-- Non-Polish company
INSERT INTO company_name (
    id,
    name,
    country_code
) VALUES (
    1,
    'Minimal Non-Polish Company',
    '[us]'
);

-- Must not equal 'production companies' and must not be NULL
INSERT INTO company_type (
    id,
    kind
) VALUES (
    1,
    'distributors'
);

-- Any one of the three accepted keywords is sufficient
INSERT INTO keyword (
    id,
    keyword
) VALUES (
    1,
    'based-on-novel'
);

-- No filter is applied to link_type.link, but it is mandatory
INSERT INTO link_type (
    id,
    link
) VALUES (
    1,
    'follows'
);

-- Main title satisfying production_year > 1950
-- kind_id is mandatory in the standard JOB schema
INSERT INTO title (
    id,
    title,
    kind_id,
    production_year
) VALUES (
    1,
    'Minimal Movie Based on a Book',
    1,
    1951
);

-- Non-NULL note required by the query
INSERT INTO movie_companies (
    id,
    movie_id,
    company_id,
    company_type_id,
    note
) VALUES (
    1,
    1,
    1,
    1,
    'Minimal production note'
);

INSERT INTO movie_keyword (
    id,
    movie_id,
    keyword_id
) VALUES (
    1,
    1,
    1
);

-- linked_movie_id is mandatory in the JOB schema.
-- It is not otherwise referenced by this query.
INSERT INTO movie_link (
    id,
    movie_id,
    linked_movie_id,
    link_type_id
) VALUES (
    1,
    1,
    1,
    1
);

COMMIT;

-- Verify table sizes
SELECT 'company_name' AS table_name, COUNT(*) AS row_count FROM company_name
UNION ALL
SELECT 'company_type', COUNT(*) FROM company_type
UNION ALL
SELECT 'keyword', COUNT(*) FROM keyword
UNION ALL
SELECT 'link_type', COUNT(*) FROM link_type
UNION ALL
SELECT 'movie_companies', COUNT(*) FROM movie_companies
UNION ALL
SELECT 'movie_keyword', COUNT(*) FROM movie_keyword
UNION ALL
SELECT 'movie_link', COUNT(*) FROM movie_link
UNION ALL
SELECT 'title', COUNT(*) FROM title
ORDER BY table_name;
SQL

============= Given Query ===============
SELECT cn.name AS from_company,
       mc.note AS production_note,
       t.title AS movie_based_on_book
FROM company_name AS cn,
     company_type AS ct,
     keyword AS k,
     link_type AS lt,
     movie_companies AS mc,
     movie_keyword AS mk,
     movie_link AS ml,
     title AS t
WHERE cn.country_code = '[us]'
  AND ct.kind = 'distributors'
  AND k.keyword = 'based-on-novel'
  AND t.production_year >= 1951
  AND lt.id = ml.link_type_id
  AND ml.movie_id = t.id
  AND t.id = mk.movie_id
  AND mk.keyword_id = k.id
  AND t.id = mc.movie_id
  AND mc.company_type_id = ct.id
  AND mc.company_id = cn.id
  AND ml.movie_id = mk.movie_id
  AND ml.movie_id = mc.movie_id
  AND mk.movie_id = mc.movie_id;
    
=========== Extracted Query =============
 
 Select company_name.name as from_company, movie_companies.note as production_note, title.title as movie_based_on_book 
 From company_name, company_type, keyword, link_type, movie_companies, movie_keyword, movie_link, title 
 Where movie_companies.movie_id = movie_keyword.movie_id
 and movie_keyword.movie_id = movie_link.movie_id
 and movie_link.movie_id = title.id
 and link_type.id = movie_link.link_type_id
 and keyword.id = movie_keyword.keyword_id
 and company_name.id = movie_companies.company_id
 and company_type.id = movie_companies.company_type_id
 and company_name.country_code = '[us]'
 and company_type.kind = 'distributors'
 and keyword.keyword = 'based-on-novel'
 and title.production_year >= 1951;