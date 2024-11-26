SELECT employee_id, department, salary
FROM searches
WHERE department = 'Sales'
ORDER BY salary DESC
LIMIT 2;