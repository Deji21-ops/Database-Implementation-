import csv
import sqlite3

DB_NAME = "ChurchDB.db"

# Connecting to SQLite

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Creating tables

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Member;")
    cursor.execute("DROP TABLE IF EXISTS Leader;")
    cursor.execute("DROP TABLE IF EXISTS Role;")

    cursor.execute("""
        CREATE TABLE Role(
            role_id INTEGER PRIMARY KEY,
            role_name TEXT,
            description TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE Leader(
            leader_id INTEGER PRIMARY KEY,
            name TEXT,
            role INTEGER,
            discipled_by INTEGER,
            FOREIGN KEY (role) REFERENCES Role(role_id),
            FOREIGN KEY (discipled_by) REFERENCES Leader(leader_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE Member(
            member_id INTEGER PRIMARY KEY,
            name TEXT,
            cell_leader_id INTEGER,
            FOREIGN KEY (cell_leader_id) REFERENCES Leader(leader_id)
        );
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")



# Loadimng CSVs

def load_roles():
    conn = get_connection()
    cursor = conn.cursor()
    with open("roles.csv") as f:
        for row in csv.DictReader(f):
            cursor.execute("INSERT INTO Role VALUES (?, ?, ?)",
                           (row["role_id"], row["role_name"], row["description"]))
    conn.commit()
    conn.close()
    print("Loaded roles.csv ✔")


def load_leaders():
    conn = get_connection()
    cursor = conn.cursor()
    with open("leaders.csv") as f:
        for row in csv.DictReader(f):
            discipled_by = row["discipled_by"] if row["discipled_by"] else None
            cursor.execute("INSERT INTO Leader VALUES (?, ?, ?, ?)",
                           (row["leader_id"], row["name"], row["role"], discipled_by))
    conn.commit()
    conn.close()
    print("Loaded leaders.csv ✔")


def load_members():
    conn = get_connection()
    cursor = conn.cursor()
    with open("members.csv") as f:
        for row in csv.DictReader(f):
            cursor.execute("INSERT INTO Member VALUES (?, ?, ?)",
                           (row["member_id"], row["name"], row["cell_leader_id"]))
    conn.commit()
    conn.close()
    print("Loaded members.csv ✔")


# Query FUnctions

#Query 1:

def query_primary_leaders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Leader WHERE discipled_by = 1;")
    results = cursor.fetchall()
    conn.close()
    return results

#Query 2:

def query_cell_leaders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Leader WHERE role = 3;")
    results = cursor.fetchall()
    conn.close()
    return results

#Query 3:

def query_disciples_per_leader():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT L2.name, COUNT(*)
        FROM Leader L1
        JOIN Leader L2 ON L1.discipled_by = L2.leader_id
        GROUP BY L2.name;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

#Query 4:

def query_members_per_cell():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Leader.name, COUNT(Member.member_id)
        FROM Member
        JOIN Leader ON Member.cell_leader_id = Leader.leader_id
        GROUP BY Leader.name;
    """)
    results = cursor.fetchall()
    conn.close()
    return results


# ASCII Visualisation plotly wasn't working

def ascii_bar_chart(title, labels, values):
    print("\n" + title)
    print("-" * len(title))

    max_label = max(len(label) for label in labels)
    max_value = max(values)

    for label, value in zip(labels, values):
        bar = "#" * value
        print(f"{label:<{max_label}} | {bar} ({value})")



# Main program

if __name__ == "__main__":
    print("Creating tables...")
    create_tables()

    print("Loading CSV data...")
    load_roles()
    load_leaders()
    load_members()

    print("\nRunning queries...\n")

    # Query 1 — Primary Leaders

    print("Primary Leaders:")
    primaries = query_primary_leaders()
    for p in primaries:
        print("-", p[0])

    # Query 2 — Cell Leaders

    print("\nCell Leaders:")
    cells = query_cell_leaders()
    for c in cells:
        print("-", c[0])

    # Query 3 — Disciples per Leader

    print("\nDisciples per Leader:")
    disciples = query_disciples_per_leader()
    for d in disciples:
        print(f"{d[0]} → {d[1]}")

    # Query 4 — Members per Cell Leader

    print("\nMembers per Cell Leader:")
    members = query_members_per_cell()
    for m in members:
        print(f"{m[0]} → {m[1]}")

    # Visualisations

    ascii_bar_chart(
        "ASCII Chart: Disciples Per Leader",
        [d[0] for d in disciples],
        [d[1] for d in disciples]
    )

    ascii_bar_chart(
        "ASCII Chart: Members Per Cell Leader",
        [m[0] for m in members],
        [m[1] for m in members]
    )

    print("\nCW.py completed successfully.")
