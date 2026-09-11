import signal
import sys

from .core.factory.PipeLineFactory import PipeLineFactory
from .pipeline.abstract.SchemaSanitizer import SchemaSanitizer
from .util.ConnectionFactory import ConnectionHelperFactory

def signal_handler(signum, frame):
    print('You pressed Ctrl+C!')
    sigconn = ConnectionHelperFactory().createConnectionHelper()
    sigconn.connectUsingParams()
    sanitizer = SchemaSanitizer(sigconn)
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
    test_workload = [TestQuery("Buy", """SELECT * 
FROM customer_buying_record
WHERE 
      (x1 = 1 OR y1 = 1)
  AND (x2 = 1 OR y2 = 1)
  AND (x3 = 1 OR y3 = 1)
  AND (x4 = 1 OR y4 = 1)
  AND (x5 = 1 OR y5 = 1)
  AND (x6 = 1 OR y6 = 1)
  AND (x7 = 1 OR y7 = 1)
  AND (x8 = 1 OR y8 = 1)
  AND (x9 = 1 OR y9 = 1)
  AND (x10 = 1 OR y10 = 1)
  AND (x11 = 1 OR y11 = 1)
  AND (x12 = 1 OR y12 = 1)
  AND (x13 = 1 OR y13 = 1)
  AND (x14 = 1 OR y14 = 1)
  AND (x15 = 1 OR y15 = 1)
  AND (x16 = 1 OR y16 = 1)
  AND (x17 = 1 OR y17 = 1)
  AND (x18 = 1 OR y18 = 1)
  AND (x19 = 1 OR y19 = 1)
  AND (x20 = 1 OR y20 = 1)
  AND (x21 = 1 OR y21 = 1)
  AND (x22 = 1 OR y22 = 1)
  AND (x23 = 1 OR y23 = 1)
  AND (x24 = 1 OR y24 = 1)
  AND (x25 = 1 OR y25 = 1)
  AND (x26 = 1 OR y26 = 1)
  AND (x27 = 1 OR y27 = 1)
  AND (x28 = 1 OR y28 = 1)
  AND (x29 = 1 OR y29 = 1)
  AND (x30 = 1 OR y30 = 1);""", False, False, False, False, True),


                     TestQuery("Anantha-Q2", """SELECT *
FROM variable_assignments
WHERE 
   (var1_val = 0 AND var2_val = 0 AND var3_val = 0 AND var4_val = 1 AND   var5_val = 1 AND var6_val = 0 AND var7_val = 0 AND var8_val = 0 AND var9_val = 0 AND var10_val = 0)
OR (var1_val = 0 AND var2_val = 1 AND var3_val = 0 AND var4_val = 0 AND var5_val = 1 AND var6_val = 1 AND var7_val = 0 AND var8_val = 1 AND var9_val = 0 AND var10_val = 1)
OR (var1_val = 1 AND var2_val = 0 AND var3_val = 1 AND var4_val = 1 AND var5_val = 0 AND var6_val = 0 AND var7_val = 1 AND var8_val = 0 AND var9_val = 1 AND var10_val = 0)
OR (var1_val = 1 AND var2_val = 1 AND var3_val = 1 AND var4_val = 0 AND var5_val = 0 AND var6_val = 1 AND var7_val = 1 AND var8_val = 1 AND var9_val = 1 AND var10_val = 1)
;""", False, False, False, False, True),

                     TestQuery("Anantha-Q1", """SELECT *
    FROM variable_assignments
    WHERE 
  (
    (var1_val = 0 AND var2_val = 0 AND var3_val = 0 AND var4_val = 1)
    OR (var1_val = 0 AND var2_val = 0 AND var3_val = 1 AND var4_val = 0)
    OR (var1_val = 0 AND var2_val = 1 AND var3_val = 0 AND var4_val = 0)
    OR (var1_val = 0 AND var2_val = 1 AND var3_val = 1 AND var4_val = 1)
    OR (var1_val = 1 AND var2_val = 0 AND var3_val = 0 AND var4_val = 0)
    OR (var1_val = 1 AND var2_val = 0 AND var3_val = 1 AND var4_val = 1)
    OR (var1_val = 1 AND var2_val = 1 AND var3_val = 0 AND var4_val = 1)
    OR (var1_val = 1 AND var2_val = 1 AND var3_val = 1 AND var4_val = 0)
  )

  AND (
    (var2_val = 0 AND var3_val = 0 AND var4_val = 0 AND var5_val = 0)
    OR (var2_val = 0 AND var3_val = 0 AND var4_val = 1 AND var5_val = 1)
    OR (var2_val = 0 AND var3_val = 1 AND var4_val = 0 AND var5_val = 1)
    OR (var2_val = 0 AND var3_val = 1 AND var4_val = 1 AND var5_val = 0)
    OR (var2_val = 1 AND var3_val = 0 AND var4_val = 0 AND var5_val = 1)
    OR (var2_val = 1 AND var3_val = 0 AND var4_val = 1 AND var5_val = 0)
    OR (var2_val = 1 AND var3_val = 1 AND var4_val = 0 AND var5_val = 0)
    OR (var2_val = 1 AND var3_val = 1 AND var4_val = 1 AND var5_val = 1)
  )

  AND (
    (var3_val = 0 AND var4_val = 0 AND var5_val = 0 AND var6_val = 0)
    OR (var3_val = 0 AND var4_val = 0 AND var5_val = 1 AND var6_val = 1)
    OR (var3_val = 0 AND var4_val = 1 AND var5_val = 0 AND var6_val = 1)
    OR (var3_val = 0 AND var4_val = 1 AND var5_val = 1 AND var6_val = 0)
    OR (var3_val = 1 AND var4_val = 0 AND var5_val = 0 AND var6_val = 1)
    OR (var3_val = 1 AND var4_val = 0 AND var5_val = 1 AND var6_val = 0)
    OR (var3_val = 1 AND var4_val = 1 AND var5_val = 0 AND var6_val = 0)
    OR (var3_val = 1 AND var4_val = 1 AND var5_val = 1 AND var6_val = 1)
  )

  AND (
    (var4_val = 0 AND var5_val = 0 AND var6_val = 0 AND var7_val = 0)
    OR (var4_val = 0 AND var5_val = 0 AND var6_val = 1 AND var7_val = 1)
    OR (var4_val = 0 AND var5_val = 1 AND var6_val = 0 AND var7_val = 1)
    OR (var4_val = 0 AND var5_val = 1 AND var6_val = 1 AND var7_val = 0)
    OR (var4_val = 1 AND var5_val = 0 AND var6_val = 0 AND var7_val = 1)
    OR (var4_val = 1 AND var5_val = 0 AND var6_val = 1 AND var7_val = 0)
    OR (var4_val = 1 AND var5_val = 1 AND var6_val = 0 AND var7_val = 0)
    OR (var4_val = 1 AND var5_val = 1 AND var6_val = 1 AND var7_val = 1)
  )

  AND (
    (var5_val = 0 AND var6_val = 0 AND var7_val = 0 AND var8_val = 1)
    OR (var5_val = 0 AND var6_val = 0 AND var7_val = 1 AND var8_val = 0)
    OR (var5_val = 0 AND var6_val = 1 AND var7_val = 0 AND var8_val = 0)
    OR (var5_val = 0 AND var6_val = 1 AND var7_val = 1 AND var8_val = 1)
    OR (var5_val = 1 AND var6_val = 0 AND var7_val = 0 AND var8_val = 0)
    OR (var5_val = 1 AND var6_val = 0 AND var7_val = 1 AND var8_val = 1)
    OR (var5_val = 1 AND var6_val = 1 AND var7_val = 0 AND var8_val = 1)
    OR (var5_val = 1 AND var6_val = 1 AND var7_val = 1 AND var8_val = 0)
  )

  AND (
    (var6_val = 0 AND var7_val = 0 AND var8_val = 0 AND var9_val = 0)
    OR (var6_val = 0 AND var7_val = 0 AND var8_val = 1 AND var9_val = 1)
    OR (var6_val = 0 AND var7_val = 1 AND var8_val = 0 AND var9_val = 1)
    OR (var6_val = 0 AND var7_val = 1 AND var8_val = 1 AND var9_val = 0)
    OR (var6_val = 1 AND var7_val = 0 AND var8_val = 0 AND var9_val = 1)
    OR (var6_val = 1 AND var7_val = 0 AND var8_val = 1 AND var9_val = 0)
    OR (var6_val = 1 AND var7_val = 1 AND var8_val = 0 AND var9_val = 0)
    OR (var6_val = 1 AND var7_val = 1 AND var8_val = 1 AND var9_val = 1)
  )

  AND (
    (var7_val = 0 AND var8_val = 0 AND var9_val = 0 AND var10_val = 0)
    OR (var7_val = 0 AND var8_val = 0 AND var9_val = 1 AND var10_val = 1)
    OR (var7_val = 0 AND var8_val = 1 AND var9_val = 0 AND var10_val = 1)
    OR (var7_val = 0 AND var8_val = 1 AND var9_val = 1 AND var10_val = 0)
    OR (var7_val = 1 AND var8_val = 0 AND var9_val = 0 AND var10_val = 1)
    OR (var7_val = 1 AND var8_val = 0 AND var9_val = 1 AND var10_val = 0)
    OR (var7_val = 1 AND var8_val = 1 AND var9_val = 0 AND var10_val = 0)
    OR (var7_val = 1 AND var8_val = 1 AND var9_val = 1 AND var10_val = 1)
  )

  AND (
    (var8_val = 0 AND var9_val = 0 AND var10_val = 0 AND var1_val = 0)
    OR (var8_val = 0 AND var9_val = 0 AND var10_val = 1 AND var1_val = 1)
    OR (var8_val = 0 AND var9_val = 1 AND var10_val = 0 AND var1_val = 1)
    OR (var8_val = 0 AND var9_val = 1 AND var10_val = 1 AND var1_val = 0)
    OR (var8_val = 1 AND var9_val = 0 AND var10_val = 0 AND var1_val = 1)
    OR (var8_val = 1 AND var9_val = 0 AND var10_val = 1 AND var1_val = 0)
    OR (var8_val = 1 AND var9_val = 1 AND var10_val = 0 AND var1_val = 0)
    OR (var8_val = 1 AND var9_val = 1 AND var10_val = 1 AND var1_val = 1)
  )


  AND (
    (var9_val = 0 AND var10_val = 0 AND var1_val = 0 AND var2_val = 0)
    OR (var9_val = 0 AND var10_val = 0 AND var1_val = 1 AND var2_val = 1)
    OR (var9_val = 0 AND var10_val = 1 AND var1_val = 0 AND var2_val = 1)
    OR (var9_val = 0 AND var10_val = 1 AND var1_val = 1 AND var2_val = 0)
    OR (var9_val = 1 AND var10_val = 0 AND var1_val = 0 AND var2_val = 1)
    OR (var9_val = 1 AND var10_val = 0 AND var1_val = 1 AND var2_val = 0)
    OR (var9_val = 1 AND var10_val = 1 AND var1_val = 0 AND var2_val = 0)
    OR (var9_val = 1 AND var10_val = 1 AND var1_val = 1 AND var2_val = 1)
  )


  AND (
    (var10_val = 0 AND var1_val = 0 AND var2_val = 0 AND var3_val = 0)
    OR (var10_val = 0 AND var1_val = 0 AND var2_val = 1 AND var3_val = 1)
    OR (var10_val = 0 AND var1_val = 1 AND var2_val = 0 AND var3_val = 1)
    OR (var10_val = 0 AND var1_val = 1 AND var2_val = 1 AND var3_val = 0)
    OR (var10_val = 1 AND var1_val = 0 AND var2_val = 0 AND var3_val = 1)
    OR (var10_val = 1 AND var1_val = 0 AND var2_val = 1 AND var3_val = 0)
    OR (var10_val = 1 AND var1_val = 1 AND var2_val = 0 AND var3_val = 0)
    OR (var10_val = 1 AND var1_val = 1 AND var2_val = 1 AND var3_val = 1)
  );""",
                               False, False, False, False, True),
                     TestQuery("Customer", """SELECT * 
FROM customer_buying_record
WHERE 
      (x1 = 1 OR y1 = 1)
  AND (x2 = 1 OR y2 = 1)
  AND (x3 = 1 OR y3 = 1)
  AND (x4 = 1 OR y4 = 1)
  AND (x5 = 1 OR y5 = 1)
  AND (x6 = 1 OR y6 = 1)
  AND (x7 = 1 OR y7 = 1)
  AND (x8 = 1 OR y8 = 1)
  AND (x9 = 1 OR y9 = 1)
  AND (x10 = 1 OR y10 = 1)
  AND (x11 = 1 OR y11 = 1)
  AND (x12 = 1 OR y12 = 1)
  AND (x13 = 1 OR y13 = 1)
  AND (x14 = 1 OR y14 = 1)
  AND (x15 = 1 OR y15 = 1)
  AND (x16 = 1 OR y16 = 1)
  AND (x17 = 1 OR y17 = 1)
  AND (x18 = 1 OR y18 = 1)
  AND (x19 = 1 OR y19 = 1)
  AND (x20 = 1 OR y20 = 1)
  AND (x21 = 1 OR y21 = 1)
  AND (x22 = 1 OR y22 = 1)
  AND (x23 = 1 OR y23 = 1)
  AND (x24 = 1 OR y24 = 1)
  AND (x25 = 1 OR y25 = 1)
  AND (x26 = 1 OR y26 = 1)
  AND (x27 = 1 OR y27 = 1)
  AND (x28 = 1 OR y28 = 1)
  AND (x29 = 1 OR y29 = 1)
  AND (x30 = 1 OR y30 = 1);""", False, False, False, False, True)

                     ]
    return test_workload


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    workload = create_workload()

    workload_dict = {}
    for elem in workload:
        workload_dict[elem.qid] = workload.index(elem)

    # print(workload_dict)

    qid = "Buy" #sys.argv[1]
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
