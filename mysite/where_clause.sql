WHERE
(
        "variable_assignments"."var10_val" = 1
    AND "variable_assignments"."var1_val" = 1
    AND "variable_assignments"."var2_val" = 1
    AND "variable_assignments"."var3_val" = 1
    AND "variable_assignments"."var6_val" = 1
    AND "variable_assignments"."var7_val" = 1
    AND "variable_assignments"."var8_val" = 1
    AND "variable_assignments"."var9_val" = 1
)
OR
(
        "variable_assignments"."var10_val" = 0
    AND "variable_assignments"."var1_val" = 0
    AND "variable_assignments"."var2_val" = 0
    AND "variable_assignments"."var3_val" = 0
    AND "variable_assignments"."var4_val" = 1
    AND "variable_assignments"."var5_val" = 1
    AND "variable_assignments"."var6_val" = 0
    AND "variable_assignments"."var7_val" = 0
);
