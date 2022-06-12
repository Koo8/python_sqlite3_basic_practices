
import sqlite3
import random

con = sqlite3.connect('student.db')
cursor = con.cursor()

# CREATE a student table with columns id, name, age, major
cursor.execute('''
    create table student (
        id integer primary key autoincrement not null unique , # 'integer primary key autoincrement' fixed format
        name text not null, 
        age integer not null, 
        major text not null);
''')

# INSERT records 
cursor.execute('''
insert into student (name, age, major) values ('john smith', 22, 'cs'), ('hello kitty', 30, 'ee');
''')

for _ in range(10):
    name = random.choice(['nancy', 'josh', 'peter', 'medline', 'kuma', 'ying'])
    major = random.choice(['cs', 'nurse', 'education', 'economy', 'music'])
    age  = random.randint(16, 80)
    cursor.execute('''
    insert into student (name, age, major) values (?,?,?);
    ''', (name, age, major  )) 

# UPDATE records
cursor.execute('''
UPDATE student SET major = 'cs' WHERE name = 'ying' AND age = 24;
''')

# DELETE records
cursor.execute('''
DELETE from student where name= 'ying' and age = 24;
''')

# SELECT some records
cursor.execute('''
select name from student;
''')
students = cursor.fetchall()
# print(students) #[('john smith',), ('nancy',), ('ying',), ('peter',), ('peter',), ('kuma',), ('ying',), ('medline',), ('nancy',), ('nancy',), ('nancy',), ('ying',), ('john smith',), ('hello kitty',)]

# SELECT DISTICT records
cursor.execute('''
select distinct name from student order by name;
''')
students = cursor.fetchall()
# print(students) #[('hello kitty',), ('john smith',), ('kuma',), ('medline',), ('nancy',), ('peter',), ('ying',)]

# alter table - add column
cursor.execute('''
alter table student add column country; 
''')

# update country column of id 15 row
# cursor.execute('select id from student')
# print(cursor.fetchall()) # output: [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (13,), (14,), (15,)]
cursor.execute('update student set country = "India" where id = 15')

# # check if updated
# cursor.execute('select * from student where id = 15')
# print(cursor.fetchall())  #[(15, 'hello kitty', 30, 'ee', 'India')]


'''sqlite operators: https://www.tutorialspoint.com/sqlite/sqlite_operators.htm'''
# BETWEEN operator
cursor.execute('select name from student where age between 20 and 30 ')
print(cursor.fetchall())

# LIKE operator - find student with 'm' in the name, % is the wildcard
cursor.execute('select name from student where name like "%m%";')
print(cursor.fetchall())# [('john smith',), ('kuma',), ('medline',), ('john smith',)]

# IN operator - used when match multiple criteria
cursor.execute('select name,major from student where major in ("cs", "ee")')
print(cursor.fetchall()) #('john smith', 'cs'), ('medline', 'cs'), ('nancy', 'cs'), ('john smith', 'cs'), ('hello kitty', 'ee')]


# create tables that has relationship with student
# First check how many majors in the student table
cursor.execute('select distinct major from student')
print(cursor.fetchall()) #[('cs',), ('economy',), ('music',), ('education',), ('nurse',), ('ee',)]
# Second create a major table (id, major )
cursor.executescript('''
create table major (id integer primary key autoincrement not null unique, majorName text);
insert into major (majorName) values ('cs'), ('economy'), ('music'), ('education'), ('nurse'), ('ee');
''')

# update student majoy column to corresponding major id integers
# since originally the student table has a TEXT datatype for 'major' column, I used 
# DB Browser -> database structure -> modify table to update the datatype from TEXT to INTEGER
# Another way to modify the majoy column in student is to create a new table and copy the original 
# table to the new one with modification, then drop the old table 
cursor.executescript('''
update student set major = 1 where major == "cs";
update student set major = 2 where major = "economy"; 
update student set major = 3 where major = "music";
update student set major = 4 where major = "education";
update student set major = 5 where major = "nurse";
update student set major = 6 where major = "ee";''')

# add a new column 'professor' for table major 
cursor.execute('alter table major add column professor text ')

# add  professors name to major table
cursor.executescript('''
update major set professor = 'Mr. Johnson' where id ==1 ;
update major set professor = 'Mrs. Alice' where id ==2 ;
update major set professor = 'Mr. Chen' where id ==3 ;
update major set professor = 'Mr. Smith' where id ==4 ;
update major set professor = 'Mr. Doe' where id ==5 ;
update major set professor = 'Miss. Lopez' where id ==6 ;
''')

# join two tables
cursor.execute('''
select student.name, student.age, major.majorName, major.professor 
from student join major 
ON student.major == major.id;''')
print(len(cursor.fetchall()))
# [('john smith', 22, 'cs', 'Mr. Johnson'), 
# ('nancy', 70, 'economy', 'Mrs. Alice'), 
# ('ying', 74, 'music', 'Mr. Chen'), 
# ('peter', 32, 'music', 'Mr. Chen'), 
# ('peter', 65, 'education', 'Mr. Smith'), 
# ('kuma', 67, 'nurse', 'Mr. Doe'), 
# ('ying', 51, 'education', 'Mr. Smith'), 
# ('medline', 23, 'cs', 'Mr. Johnson'), 
# ('nancy', 38, 'cs', 'Mr. Johnson'), 
# ('nancy', 29, 'economy', 'Mrs. Alice'), 
# ('nancy', 35, 'music', 'Mr. Chen'), 
# ('ying', 32, 'music', 'Mr. Chen'), 
# ('john smith', 22, 'cs', 'Mr. Johnson'), 
# ('hello kitty', 30, 'ee', 'Miss. Lopez')]

# add foreign key to  an existing table
'''You can not use the ALTER TABLE statement to add a foreign key in SQLite. 
Instead you will need to 1. rename the table, 2.create a new table with the foreign key, 
and then 3. copy the data into the new table.'''

cursor.executescript('''
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
ALTER TABLE student RENAME TO _student_old;
CREATE TABLE student (
    id integer primary key autoincrement not null unique,
    name text not null,
    age integer not null,
    major integer not null,
    country text ,
    foreign key (major) references major (id)
);
INSERT INTO student SELECT * from _student_old;
COMMIT;
PRAGMA foreign_keys=ON;
''')

# test foreign key constraits NOTE: each time the foreign key should be turned on first
cursor.executescript('''
PRAGMA foreign_keys=ON;
INSERT into student (name, age, major, country) values ('Fred', 25, 10, 'Italy');
''')

# use CONCAT and AS (alias) in statement, alias can also be used for table name
# SQLite does not support the CONCAT() function from SQL. 
# Instead, it uses the concatenate operator (||) to join two strings into one.
cursor.execute('''
SELECT s.name || '-' || s.age AS "NAME/AGE", m.majorName as MAJOR, m.professor as PROF 
FROM student as s
JOIN major as m
ON s.major = m.id;
''')

# aggregate functions (AVG, MIN, MAX, SUM, COUNT, UPPER, LOWER)
cursor.execute('select avg(s.age) from student as s')
print(cursor.fetchall())  # output [(40.625, )]
cursor.execute('select min(s.age) from student as s')
print(cursor.fetchall()) # output: [(22,)]

# combine aggregate functions with GROUP BY
cursor.execute('select age, count(age) from student group by age ')
print(cursor.fetchall()) 
# output: [(22, 2), (23, 1), (25, 1), (29, 1), (30, 1), 
# (32, 2), (35, 2), (38, 1), (51, 1), (65, 1), (67, 1), (70, 1), (74, 1)]

# IF only need value of count to be more than 1, use HAVING for condition after group by
cursor.execute('select age, count(age) from student group by age Having count(age) >=2 ')
print(cursor.fetchall()) 
# output: [(22, 2), (32, 2), (35, 2)]

# remove old table
cursor.execute('DROP Table if exists _student_old;')


con.commit()
con.close()
