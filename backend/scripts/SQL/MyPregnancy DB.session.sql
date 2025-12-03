SELECT 
    -- Mother Details
    u_mother.email AS mother_email,

    
    -- Calculated Count (Window Function)
    COUNT(apt.id) OVER (PARTITION BY pw.id) AS total_appointment_count,

    -- Appointment Details
    -- apt.id AS appointment_id,
    -- apt.start_time,
    apt.status AS appointment_status,

    -- Doctor Details
    -- u_doc.first_name AS doctor_first_name,
    -- u_doc.last_name AS doctor_last_name,
    u_doc.email as doctor_email
    -- d_qual.qualification_option AS doctor_degree

FROM pregnant_women pw
-- 1. Get the User details for the Mother
JOIN users u_mother ON pw.id = u_mother.id

-- 2. Get Appointments (LEFT JOIN ensures women with 0 appointments still appear)
LEFT JOIN appointments apt ON pw.id = apt.mother_id

-- 3. Get the Doctor details for the specific appointment
LEFT JOIN volunteer_doctors vd ON apt.volunteer_doctor_id = vd.id
LEFT JOIN users u_doc ON vd.id = u_doc.id

-- 4. Get Doctor Qualification (Optional, but useful context)
LEFT JOIN doctor_qualifications d_qual ON vd.qualification_id = d_qual.id

ORDER BY 
    total_appointment_count DESC, -- Primary: Women with most appointments first
    u_mother.last_name ASC,       -- Secondary: Alphabetical by mother
    apt.start_time DESC;          -- Tertiary: Newest appointments first