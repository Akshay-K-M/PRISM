import signal
import sys

from .core.factory.PipeLineFactory import PipeLineFactory
from .pipeline.abstract.TpchSanitizer import TpchSanitizer
from .util.ConnectionFactory import ConnectionHelperFactory
from .util.workload_queries import TestQuery


def signal_handler(signum, frame):
    print('You pressed Ctrl+C!')
    sigconn = ConnectionHelperFactory().createConnectionHelper()
    sigconn.connectUsingParams()
    sanitizer = TpchSanitizer(sigconn)
    sanitizer.sanitize()
    sigconn.closeConnection()
    print("database restored!")
    sys.exit(0)


class TestQuery:
    def __init__(self, name: str, hidden_query: str, cs2: bool, union: bool, oj: bool, nep: bool, orf=None):
        self.qid = name
        self.cs2 = cs2
        self.union = union
        self.oj = oj
        self.nep = nep
        self.query = hidden_query
        self.orf = orf if orf is not None else False

def create_workload():
    test_workload = [TestQuery("Q1",  """SELECT n_name AS of_person,
       t_title AS biography_movie
FROM aka_name,
     cast_info,
     info_type,
     link_type,
     movie_link,
     name,
     person_info,
     title
WHERE an_name LIKE '%a%'
  AND it_info ='mini biography'
  AND lt_link ='features'
  AND pi_note ='Volker Boehm'
  AND t_production_year BETWEEN 1980 AND 1995
  AND n_id = an_person_id
  AND n_id = pi_person_id
  AND ci_person_id = n_id
  AND t_id = ci_movie_id
  AND ml_linked_movie_id = t_id
  AND lt_id = ml_link_type_id
  AND it_id = pi_info_type_id
AND pi_person_id = an_person_id
  AND pi_person_id = ci_person_id
  AND an_person_id = ci_person_id
  AND ci_movie_id = ml_linked_movie_id;
    """, False, False, False, False),
 ]
    return test_workload


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    workload = create_workload()

    workload_dict = {}
    for elem in workload:
        workload_dict[elem.qid] = workload.index(elem)

    # print(workload_dict)

    qid = "Q1" #sys.argv[1]
    hq = workload[workload_dict[qid]]
    query = hq.query
    conn = ConnectionHelperFactory().createConnectionHelper()
    conn.config.detect_union = hq.union
    conn.config.detect_oj = hq.oj
    conn.config.detect_nep = hq.nep
    conn.config.use_cs2 = hq.cs2
    conn.config.detect_or = hq.orf

    print(f"Flags: Scale Down {conn.config.scale_down}, Union {conn.config.detect_union}, OJ {conn.config.detect_oj}, "
          f"NEP {conn.config.detect_nep}, CS2 {conn.config.use_cs2}")

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    factory = PipeLineFactory()
    token = factory.init_job(conn, query)
    factory.doJob(query, token)
    result = factory.result

    if result is not None:
        print("============= Given Query ===============")
        print(query)
        print("=========== Extracted Query =============")
        print(result)
        print("================ Profile ================")
        pipe = factory.get_pipeline_obj(token)
        pipe.time_profile.print()
    else:
        print("I had some Trouble! Check the log file for the details..")
