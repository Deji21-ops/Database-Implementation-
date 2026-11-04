# Database-Implementation-
Designed and implemented a relational database based on the G12 Evangelistic Church Movement, focusing on database design, entity relationships and structured data management. Applied SQL and relational modelling techniques to organise information and support efficient data storage and retrieval. 

Project Motivation

This project was developed from a desire to combine my personal Christian faith and religious interests with my technical skills. By applying database design and implementation to the G12 Evangelistic Church Movement, I was able to turn a personal interest into a practical technical project. 

# G12 Church Leadership Database Project

## 📋 Overview
This project presents a relational database system designed to model and manage the **G12 Church Leadership Structure**. The G12 vision is a scalable discipleship model where leaders mentor twelve primary leaders, who in turn lead cell groups, ensuring structured accountability, spiritual growth, and seamless communication across the organization.

The database is implemented and tested using **SQLite** (standard SQL syntax, fully compatible with **MySQL**).

---

## 🏛️ Business Rules & Model
- **Discipleship Hierarchy:** 
  - Every Leader (except the Senior Leader / Pastor) is mentored/discipled by exactly **one** leader above them (`discipled_by`).
  - A Senior Leader (typically `Leader_Id = 1`) directly mentors Primary Leaders.
  - Primary Leaders mentor Cell Leaders.
- **Member Management:** 
  - Church **Members** belong to a specific **Cell Leader** (`Cell_Leader_Id` / `cell_leader_id`) responsible for their spiritual development and pastoral support.
- **Roles & Levels:** 
  - Roles define leadership levels (e.g., Senior Leader, Primary Leader, Cell Leader) to clarify organizational responsibilities and reporting pathways.

---

## 📐 Entity-Relationship Diagram (ERD) & Schema Design

```
                     +-------------------+
                     |       Role        |
                     +-------------------+
                     | PK  Role_id       |
                     |     Role_name     |
                     |     Description   |
                     +---------+---------+
                               | 1
                               |
                           [Has_Role]
                               |
                               | M
                     +---------v---------+
                     |      Leader       | <----+
                     +-------------------+      |
                     | PK  Leader_Id     |      | (Disciples / discipled_by)
                     |     name          |      | 1:M Self-Reference
                     |     role          | -----+
                     |     discipled_by  |
                     +---------+---------+
                               | 1
                               |
                            [Leads]
                               |
                               | M
                     +---------v---------+
                     |      Member       |
                     +-------------------+
                     | PK  Member_Id     |
                     |     Name          |
                     | FK  Cell_Leader_Id|
                     +-------------------+
```

### Entities & Relationships
1. **`Leader`**: Represents all leaders within the G12 framework.
   - **Attributes:** `Leader_Id` (PK), `name`, `role` (FK to Role), `discipled_by` (Self-referencing FK to `Leader_Id`).
   - **Self-referencing Relationship (`Disciples` / `discipled_by`):** Models the 1-to-Many hierarchy where one leader disciples multiple lower-level leaders.
2. **`Role`**: Categorizes leadership responsibilities.
   - **Attributes:** `Role_Id` (PK), `Role_name`, `Description`.
   - **Relationship (`Has_Role`):** 1-to-Many with `Leader` (One role can be assigned to multiple leaders).
3. **`Member`**: Represents general church members attending cell groups.
   - **Attributes:** `Member_Id` (PK), `Name`, `Cell_Leader_Id` (FK to Leader).
   - **Relationship (`Leads`):** 1-to-Many between `Leader` and `Member` (Each Cell Leader oversees multiple members; each member has exactly one Cell Leader).

---

## 💻 Database Queries (SQL)

### Query 1: Retrieve Primary Leaders
Finds all Primary Leaders who are directly discipled by the Senior Pastor (`Leader_Id = 1`).

```sql
SELECT name
FROM Leader
WHERE discipled_by = 1;
```

---

### Query 2: Filter Leaders by Role (Cell Leaders)
Lists all leaders assigned specifically to Role 3 (Cell Leaders).

```sql
SELECT name
FROM Leader
WHERE role = 3;
```

---

### Query 3: Count Disciples per Leader
Calculates the total number of leaders being mentored by each leader in the hierarchy.

```sql
SELECT discipled_by, COUNT(*) AS total_disciples
FROM Leader
WHERE discipled_by IS NOT NULL
GROUP BY discipled_by;
```

---

### Query 4: Cell Group Member Count
Groups church members by their assigned Cell Leader to measure cell group sizes and leadership responsibility.

```sql
SELECT cell_leader_id, COUNT(*) AS member_count
FROM Member
GROUP BY cell_leader_id;
```

---

## 🛠️ Compatibility & Implementation Notes
- **Database Engine:** SQLite / MySQL.
- **Integrity Constraints:** Foreign key constraints (`discipled_by` $\rightarrow$ `Leader.Leader_Id`, `Cell_Leader_Id` $\rightarrow$ `Leader.Leader_Id`, `role` $\rightarrow$ `Role.Role_Id`) maintain relational and hierarchical integrity.
