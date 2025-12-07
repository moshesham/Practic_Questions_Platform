SELECT employee_id, department, salary
FROM employees
WHERE department = 'Sales'
ORDER BY salary DESC
LIMIT 10;