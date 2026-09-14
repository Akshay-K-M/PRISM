-- createdb prism_10a
-- pg_dump --schema-only --no-owner --no-privileges job \
-- | psql -v ON_ERROR_STOP=1 -d prism_10a

BEGIN;

-- Character returned by MIN(chn.name).
INSERT INTO char_name (
    id,
    name
) VALUES (
    1,
    'Minimal Character'
);

-- Russian company required by cn.country_code = '[ru]'.
INSERT INTO company_name (
    id,
    name,
    country_code
) VALUES (
    1,
    'Minimal Russian Company',
    '[ru]'
);

-- Query joins this table but does not filter ct.kind.
INSERT INTO company_type (
    id,
    kind
) VALUES (
    1,
    'production companies'
);

-- Required by rt.role = 'actor'.
INSERT INTO role_type (
    id,
    role
) VALUES (
    1,
    'actor'
);

-- kind_id is NOT NULL in the standard JOB schema.
-- The query does not join kind_type, so an arbitrary value is sufficient
-- because the published JOB schema does not declare foreign-key constraints.
INSERT INTO title (
    id,
    title,
    kind_id,
    production_year
) VALUES (
    1,
    'Minimal Russian Movie',
    1,
    2006
);

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

-- person_id is NOT NULL, although query 10a does not join the name table.
-- The note satisfies both LIKE predicates.
INSERT INTO cast_info (
    id,
    person_id,
    movie_id,
    person_role_id,
    note,
    role_id
) VALUES (
    1,
    1,
    1,
    1,
    '(voice) (uncredited)',
    1
);

COMMIT;

-- ============= Given Query ===============
-- SELECT MIN(chn.name) AS uncredited_voiced_character,
--        MIN(t.title) AS russian_movie
-- FROM char_name AS chn,
--      cast_info AS ci,
--      company_name AS cn,
--      company_type AS ct,
--      movie_companies AS mc,
--      role_type AS rt,
--      title AS t
-- WHERE ci.note LIKE '%(voice)%'
--   AND cn.country_code = '[ru]'
--   AND rt.role = 'actor'
--   AND t.production_year > 2005
--   AND t.id = mc.movie_id
--   AND t.id = ci.movie_id
--   AND ci.movie_id = mc.movie_id
--   AND chn.id = ci.person_role_id
--   AND rt.id = ci.role_id
--   AND cn.id = mc.company_id
--   AND ct.id = mc.company_type_id;
    
-- =========== Extracted Query =============
 
--  Select Min(char_name.name) as uncredited_voiced_character, Min(title.title) as russian_movie 
--  From cast_info, char_name, company_name, company_type, movie_companies, role_type, title 
--  Where company_type.id = movie_companies.company_type_id
--  and company_name.id = movie_companies.company_id
--  and cast_info.role_id = role_type.id
--  and cast_info.person_role_id = char_name.id
--  and cast_info.movie_id = movie_companies.movie_id
--  and movie_companies.movie_id = title.id
--  and company_name.country_code = '[ru]'
--  and role_type.role = 'actor'
--  and cast_info.note LIKE '%(voice)%'
--  and title.production_year >= 2006;