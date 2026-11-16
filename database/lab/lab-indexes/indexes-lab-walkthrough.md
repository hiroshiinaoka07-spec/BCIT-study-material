# ACIT 3910 — Slow Inserts and Indexing Lab

Do the Slow Inserts lab first, then the Indexing lab, inside the VirtualBox VM. Download `Insert10.sql`, `Insert300.sql`, and `Insert300nokeys.sql` from D2L and `cd` into that folder before the redirects. Use your VM’s MySQL root password when prompted.

There are 17 screenshots. Take each one only at the step marked **SCREENSHOT**.

## Part 1 — Slow Inserts

Open **two** windows. Window A runs the import. Window B is a second MySQL login used only for the timing queries.

```text
mysql -u root -p
```

If `mysql` is not on the PATH:

```text
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

### Method 1 — `Insert10.sql` (10 rows per INSERT)

Window A:

```text
mysql -u root -p < Insert10.sql
```

As soon as it asks for the password and starts, switch to Window B and run Timing Query 1:

```sql
SELECT @startTime := NOW() AS StartTime,
       @startCount := COUNT(*) AS StartCount
FROM lotsofdata.user;
```

**SCREENSHOT:** `01_Insert10_start.jpg`

Wait at least 10 seconds, then run Timing Query 2 and Timing Query 3:

```sql
SELECT @endTime := NOW() AS EndTime,
       @endCount := COUNT(*) AS EndCount
FROM lotsofdata.user;
```

```sql
SELECT @endTime AS EndTime,
       @endCount AS EndCount,
       TIMESTAMPDIFF(SECOND, @startTime, @endTime) AS elapsedTime,
       (@endCount - @startCount) AS newRows,
       TIME_FORMAT(
         SEC_TO_TIME(
           1000000 / ((@endCount - @startCount) /
                      TIMESTAMPDIFF(SECOND, @startTime, @endTime))
         ),
         '%Hh %im %ss'
       ) AS EstimatedTime
FROM DUAL;
```

**SCREENSHOT:** `02_Insert10_end.jpg` — the result grid of Timing Query 3, including `EstimatedTime`.

Do not wait for the import to finish. Close Window A. Ctrl+C will not stop it.

### Method 2 — `Insert300.sql` (300 rows per INSERT)

Window A:

```text
mysql -u root -p < Insert300.sql
```

Window B, same three queries as above.

**SCREENSHOT:** `03_Insert300_start.jpg` right after Timing Query 1.

**SCREENSHOT:** `04_Insert300_end.jpg` of Timing Query 3.

Close Window A. Do not wait for it to finish.

Method 2 is faster. One `INSERT` with 300 value tuples does far less statement overhead than many `INSERT`s of 10 tuples, for the same 1,000,000 rows.

### Method 3 — `Insert300nokeys.sql` (indexes off)

Let this one finish. Start a stopwatch the moment you press Enter after the password.

The lab writes the filename both ways. Use the name of the file you downloaded:

```text
mysql -u root -p < Insert300nokeys.sql
```

When the prompt returns, stop the stopwatch.

**SCREENSHOT:** `05_Insert300nokeys_stopwatch.jpg`

Then, in MySQL:

```sql
SELECT COUNT(*) FROM lotsofdata.user;
```

**SCREENSHOT:** `06_Insert300nokeys_complete.jpg` — the count, which should be 1,000,000.

Method 3 is faster than Method 2. The file loads the rows with keys/indexes disabled, so MySQL does not maintain the primary key and secondary indexes on every row. The cost is that MySQL is no longer enforcing uniqueness or foreign keys during the load. Only do that when the file is already known to be valid.

## Part 2 — Indexing

Stay on this same `lotsofdata.user` table (1,000,000 rows).

### Workbench setup (do this before the slow queries)

1. Turn off the result-grid **Limit Rows** option. A `LIMIT` changes the plan and makes these tests meaningless.
2. **Edit → Preferences → SQL Editor** → set **DBMS connection read timeout interval** to `600`.
3. Close Workbench and open it again.

Screenshots 15–17 use `\G`, which only works in the **mysql command-line client**, not Workbench. Use the CLI for those three.

### Grow the table to 8 million rows

Run this **three times**. Each run doubles the table: 1M → 2M → 4M → 8M. Each run is slower than the one before it.

```sql
INSERT INTO lotsofdata.user
  (firstname, lastname, email, birth_date, created_date)
SELECT firstname, lastname, email, birth_date, created_date
FROM lotsofdata.user;
```

If you get `The total number of locks exceeds the lock table size`:

1. Open `my.ini` as Administrator. On Windows it is usually `C:\ProgramData\MySQL\MySQL Server 8.0\my.ini`.
2. Change `innodb_buffer_pool_size=8M` to:

```ini
innodb_buffer_pool_size=512M
```

3. Save, then restart MySQL (service name is often `MySQL80`):

```text
net stop MySQL80
net start MySQL80
```

4. Run the `INSERT ... SELECT` again until `COUNT(*)` is at least 8,000,000.

Confirm:

```sql
SELECT COUNT(*) FROM lotsofdata.user;
```

**SCREENSHOT:** `07_eight_million_rows.jpg` — include the execution time in the status bar.

### Min/max with no usable index

```sql
SELECT MIN(birth_date), MAX(birth_date) FROM lotsofdata.user;
```

**SCREENSHOT:** `08_oldest_to_youngest_slow.jpg` — include the execution time. This is a full scan of 8 million rows.

### Add the `birth_date` index

```sql
ALTER TABLE lotsofdata.user
  ADD INDEX birth_date (birth_date ASC) VISIBLE;
```

**SCREENSHOT:** `09_Creating_birth_date_index.jpg` — the statement and its execution time. This takes a while.

Run the same min/max query again:

```sql
SELECT MIN(birth_date), MAX(birth_date) FROM lotsofdata.user;
```

**SCREENSHOT:** `10_oldest_to_youngest_fast.jpg` — include the execution time. MySQL reads the two ends of the index.

### EXPLAIN, invisible vs visible

If `EXPLAIN` comes back as a tree, switch formats in the CLI:

```sql
SET SESSION explain_format = 'TRADITIONAL';
SELECT @@explain_format;
```

Hide the index and prove the query is slow again:

```sql
ALTER TABLE lotsofdata.user ALTER INDEX birth_date INVISIBLE;
```

```sql
SELECT MIN(birth_date), MAX(birth_date) FROM lotsofdata.user;
```

Then:

```sql
EXPLAIN SELECT MIN(birth_date), MAX(birth_date) FROM lotsofdata.user;
```

**SCREENSHOT:** `11_explain_oldest_to_youngest_slow.jpg`

`type` will be `ALL` (full table scan). On the usual scale that is the worst rank: `system` > `const` > `eq_ref` > `ref` > `range` > `index` > `ALL`.

Turn the index back on and explain again:

```sql
ALTER TABLE lotsofdata.user ALTER INDEX birth_date VISIBLE;
```

```sql
EXPLAIN SELECT MIN(birth_date), MAX(birth_date) FROM lotsofdata.user;
```

**SCREENSHOT:** `12_explain_oldest_to_youngest_fast.jpg`

`key` is `birth_date`. `type` is `index` (or Extra says the min/max was taken from the index). `possible_keys` / `key` are NULL in the slow shot and `birth_date` in the fast shot. `rows` drops from about 8 million to a tiny number.

### Query 1 — primary key

```sql
SELECT lastname, firstname, birth_date, email
FROM lotsofdata.user
WHERE user_id = 1;
```

```sql
EXPLAIN SELECT lastname, firstname, birth_date, email
FROM lotsofdata.user
WHERE user_id = 1;
```

**SCREENSHOT:** `13_query_one.jpg` — execution time of the `SELECT` and the `EXPLAIN` output.

`type` is `const`. That is the best rank on the scale: one primary-key lookup, `rows` = 1.

### Query 2 — equality on the indexed date

```sql
SELECT lastname, firstname, birth_date, email
FROM lotsofdata.user
WHERE birth_date = '1943-04-12 09:33:02';
```

```sql
EXPLAIN SELECT lastname, firstname, birth_date, email
FROM lotsofdata.user
WHERE birth_date = '1943-04-12 09:33:02';
```

**SCREENSHOT:** `14_query_two.jpg` — execution time and `EXPLAIN`.

`type` is `ref`, `key` is `birth_date`. `ref` is worse than `const` because `birth_date` is not unique, and better than `range`, `index`, and `ALL`.

### Query 3 — the index order matters

Run this in the **mysql CLI**. The `\G` replaces the semicolon.

```sql
EXPLAIN SELECT COUNT(*), lastname
FROM lotsofdata.user
WHERE lastname LIKE "A%"
  AND birth_date >= "1977-01-01 0:00:00"
GROUP BY lastname\G
```

**SCREENSHOT:** `15_explain_query_three_birth_date_index.jpg`

`type` is `range` or `ALL`. The `birth_date` index can only help the date predicate. It does nothing for `lastname LIKE "A%"`, so this plan is still a huge read. Rank: `range` if `key` is `birth_date`, otherwise `ALL`.

Run it, and be ready to kill it. Open a **second** CLI session:

```sql
SHOW FULL PROCESSLIST\G
```

If `Time` for that `SELECT` goes past 180, use the `Id` from that row:

```sql
KILL 33;
```

Replace `33` with the real `Id`.

### Composite index, lastname first

```sql
ALTER TABLE lotsofdata.user
  ADD INDEX lastname_birth_date (lastname ASC, birth_date ASC) VISIBLE;
```

```sql
ALTER TABLE lotsofdata.user ALTER INDEX birth_date INVISIBLE;
```

```sql
EXPLAIN SELECT COUNT(*), lastname
FROM lotsofdata.user
WHERE lastname LIKE "A%"
  AND birth_date >= "1977-01-01 0:00:00"
GROUP BY lastname\G
```

**SCREENSHOT:** `16_explain_query_three_lastname_birth_date_index.jpg`

`key` is `lastname_birth_date`, `type` is `range`. Yes, Query 3 uses this index. Then run the real query and let it finish:

```sql
SELECT COUNT(*), lastname
FROM lotsofdata.user
WHERE lastname LIKE "A%"
  AND birth_date >= "1977-01-01 0:00:00"
GROUP BY lastname;
```

Note the execution time. Run 2 is faster than Run 1.

### Same columns, opposite order

```sql
ALTER TABLE lotsofdata.user
  ADD INDEX birth_date_lastname (birth_date ASC, lastname ASC) VISIBLE;
```

```sql
ALTER TABLE lotsofdata.user ALTER INDEX lastname_birth_date INVISIBLE;
```

```sql
EXPLAIN SELECT COUNT(*), lastname
FROM lotsofdata.user
WHERE lastname LIKE "A%"
  AND birth_date >= "1977-01-01 0:00:00"
GROUP BY lastname\G
```

**SCREENSHOT:** `17_explain_query_three_birth_date_lastname_index.jpg`

`key` may be `birth_date_lastname` and `type` `range`, but the leading column is `birth_date`, so MySQL walks every index entry from 1977 onward and checks `lastname` afterward. Then run Query 3 again:

```sql
SELECT COUNT(*), lastname
FROM lotsofdata.user
WHERE lastname LIKE "A%"
  AND birth_date >= "1977-01-01 0:00:00"
GROUP BY lastname;
```

Run 2 (`lastname`, `birth_date`) is faster than Run 3 (`birth_date`, `lastname`).

A composite index is only useful from the left. `lastname LIKE "A%"` is a small slice of the index when `lastname` is the first column, and `birth_date` can still be used inside that slice. With `birth_date` first, `>= "1977-01-01"` matches most of the 8 million rows, and the `lastname` condition is applied only after that large range is read.
