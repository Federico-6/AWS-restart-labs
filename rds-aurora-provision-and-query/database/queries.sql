-- Show the contents of restart table
SELECT *
FROM restart;

-- Show the contents of cloud_practitioner table
SELECT *
FROM cloud_practitioner;

-- Students that are both in restart and cloud_practitioner table
SELECT r.student_id, r.student_name, cp.certification_date
FROM restart r
INNER JOIN cloud_practitioner cp
USING (student_id);