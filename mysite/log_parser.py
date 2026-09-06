import ast
import re
from pathlib import Path

LOG_FILE = Path("unmasque.log")
OUTPUT_FILE = Path("where_clause.sql")

MARKER = "new or predicates..."


def extract_list_literals(text):
    """Extract consecutive balanced [...] expressions."""
    literals = []
    start = None
    depth = 0
    quote = None
    escaped = False

    for i, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue

        if char in ("'", '"'):
            quote = char
        elif char == "[":
            if depth == 0:
                start = i
            depth += 1
        elif char == "]" and depth:
            depth -= 1
            if depth == 0:
                literals.append(text[start:i + 1])

    return literals


def is_predicate(value):
    return (
        isinstance(value, tuple)
        and len(value) >= 4
        and isinstance(value[0], str)
        and isinstance(value[1], str)
        and isinstance(value[2], str)
    )


def normalize_groups(value):
    """
    Accepted forms:
      [(...), (...)]       -> one AND group
      [[(...), (...)]]     -> one or more AND groups
    """
    if not isinstance(value, list) or not value:
        return []

    if all(is_predicate(item) for item in value):
        return [value]

    groups = []
    for item in value:
        if isinstance(item, list) and item and all(
            is_predicate(predicate) for predicate in item
        ):
            groups.append(item)

    return groups


def parse_snapshot(payload):
    groups = []

    for literal in extract_list_literals(payload):
        try:
            value = ast.literal_eval(literal)
        except (SyntaxError, ValueError):
            continue

        groups.extend(normalize_groups(value))

    # Remove duplicate groups while preserving order.
    unique_groups = []
    seen = set()

    for group in groups:
        key = tuple(group)
        if key not in seen:
            seen.add(key)
            unique_groups.append(group)

    return unique_groups


def find_final_snapshot(log_text):
    """
    Select the latest snapshot having the greatest number of:
      1. OR groups
      2. total predicates

    This excludes earlier, partially constructed branches.
    """
    best_groups = []
    best_score = (0, 0, -1)

    for line_number, line in enumerate(log_text.splitlines()):
        if MARKER not in line:
            continue

        payload = line.split(MARKER, 1)[1].strip()
        groups = parse_snapshot(payload)

        score = (
            len(groups),
            sum(len(group) for group in groups),
            line_number
        )

        if score > best_score:
            best_score = score
            best_groups = groups

    return best_groups


def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


def sql_value(value):
    if value is None:
        return "NULL"

    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"

    if isinstance(value, (int, float)):
        return str(value)

    return "'" + str(value).replace("'", "''") + "'"


def predicate_to_sql(predicate, qualify_table=True):
    table, column, operator, value = predicate[:4]

    allowed_operators = {
        "=", "!=", "<>", "<", "<=", ">", ">=",
        "LIKE", "NOT LIKE", "IS", "IS NOT"
    }

    operator = operator.upper()
    if operator not in allowed_operators:
        raise ValueError(f"Unsupported SQL operator: {operator}")

    if qualify_table:
        left_side = (
            f"{quote_identifier(table)}."
            f"{quote_identifier(column)}"
        )
    else:
        left_side = quote_identifier(column)

    if value is None and operator == "=":
        return f"{left_side} IS NULL"

    if value is None and operator in ("!=", "<>"):
        return f"{left_side} IS NOT NULL"

    return f"{left_side} {operator} {sql_value(value)}"


def build_where_clause(groups, qualify_table=True):
    if not groups:
        raise ValueError("No complete OR-predicate snapshot was found.")

    or_parts = []

    for group in groups:
        and_parts = [
            predicate_to_sql(predicate, qualify_table)
            for predicate in group
        ]

        or_parts.append(
            "(\n        " + "\n    AND ".join(and_parts) + "\n)"
        )

    return "WHERE\n" + "\nOR\n".join(or_parts) + ";"


def main():
    log_text = LOG_FILE.read_text(
        encoding="utf-8",
        errors="replace"
    )

    groups = find_final_snapshot(log_text)
    where_clause = build_where_clause(
        groups,
        qualify_table=True
    )

    OUTPUT_FILE.write_text(
        where_clause + "\n",
        encoding="utf-8"
    )

    print(f"OR groups found: {len(groups)}")
    print(
        "Predicates per group:",
        [len(group) for group in groups]
    )
    print(f"Written to: {OUTPUT_FILE.resolve()}")
    print()
    print(where_clause)


if __name__ == "__main__":
    main()