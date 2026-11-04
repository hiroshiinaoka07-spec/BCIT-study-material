#Verify Users and Roles in school
use school;
select * from information_schema.table_privileges where table_schema = 'school' order by grantee, table_schema, table_name, privilege_type;
select * from information_schema.schema_privileges where table_schema = 'school' order by grantee, table_schema, privilege_type;
select * from information_schema.user_privileges where grantee regexp 'ally|evangelica|ema|zed|tulio|collyn|linnea|jayson|duston|chen' order by grantee;
SELECT DISTINCT User 'Role Name', if(from_user is NULL,0, 1) Active 
       FROM mysql.user LEFT JOIN mysql.role_edges ON from_user=user 
       WHERE account_locked='Y' AND password_expired='Y' AND authentication_string=''
         and user IN ('instructor', 'student');
select uuid(), utc_timestamp();
show procedure status where db='school';
SELECT ROUTINE_NAME, ROUTINE_DEFINITION
    FROM information_schema.ROUTINES
    WHERE ROUTINE_TYPE = 'PROCEDURE'
    AND ROUTINE_SCHEMA = 'school';
show grants for 'Ally';
show grants for 'Evangelica';
show grants for 'Ema';
show grants for 'Zed';
show grants for 'Tulio';
show grants for 'Collyn';
show grants for 'Linnea';
show grants for 'Jayson';
show grants for 'Duston';
show grants for 'Chen';

