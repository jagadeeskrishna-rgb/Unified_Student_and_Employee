# Unified Students & Employment Lifecycle Portal

## Single Window Solution

## 1. Abstract

The **Unified Students & Employment Lifecycle Portal** is a web-based academic application developed to manage student and employee lifecycle information in a single platform. The system helps students maintain their education, skills, certifications, internship status, placement details, career status, and current employment information. It also helps employees maintain employment records, company mapping, salary details, and salary-related queries.

In the current system, student career details, employee profile details, company records, salary records, and verification details are usually maintained separately. Because of this, it becomes difficult to identify fake profiles, duplicate records, multiple active employment records, salary mismatch issues, and unresolved employee complaints.

This project provides a centralized portal where Admin, Student, Employee, and Company/HR users can manage and verify records through simple role-based access. The system supports student profile management, employee profile management, company management, employment verification, salary record management, salary query management, dashboards, and reports.

For student-level implementation, real government, bank, GST, Aadhaar, or PAN verification APIs will not be used. Instead, the system will use sample data and rule-based verification logic to demonstrate the concept.

This project is suitable for a B.Sc. Computer Science final year project because it includes real-time web application concepts such as authentication, CRUD operations, database design, role-based access control, verification logic, dashboards, reports, and query management.

## 2. Problem Statement

Students, employees, companies, and administrators need a common platform to manage education details, career status, employment details, salary records, company details, and verification information. In many cases, these records are maintained using separate systems, spreadsheets, or manual files. This creates difficulty in tracking correct information and verifying whether a profile or employment record is genuine.

Some employees may create duplicate profiles or may show active employment in more than one company at the same time. Salary records may also have mismatches, such as salary not being paid, incorrect salary amount, wrong deductions, or pending salary details. Employees need a proper system to raise salary-related queries and track their status.

The main problem is the lack of a simple single-window portal that connects student career tracking, employee management, company management, salary details, and verification logic in one system.

## 3. Existing Problem

In the existing manual or separate system approach, the following problems are commonly found:

- Student career details are not maintained in one centralized system.
- Employee details and company employment records are stored separately.
- Duplicate employee profiles are difficult to identify.
- Fake or suspicious profiles cannot be checked easily.
- Multiple active employment records are difficult to detect manually.
- Salary paid details and expected salary details are not compared properly.
- Employees do not have a proper portal to raise salary-related queries.
- Companies do not have a simple common platform to update employee and salary details.
- Admin users find it difficult to generate consolidated reports.
- Manual records can lead to data loss, duplicate records, and tracking issues.

## 4. Proposed Solution

The proposed system is a **Unified Students & Employment Lifecycle Portal** that acts as a single-window solution for managing student, employee, company, employment, salary, verification, and query details.

The system provides separate login access for Admin, Student, Employee, and Company users. Students can maintain their profile, education, skills, internship, placement, and career status. Employees can maintain their employment details, view salary records, and raise salary-related queries. Companies can manage employee records and upload salary details. Admin users can verify records, check duplicate profiles, identify multiple active employment records, manage queries, and generate reports.

For academic implementation, the verification process will be rule-based. For example, the system can check duplicate email, duplicate mobile number, duplicate demo identity number, and multiple active employment records for the same employee. Salary mismatch can be identified by comparing expected salary and paid salary.

This solution reduces manual work, improves record management, supports basic verification, and provides useful reports for academic demonstration.

## 5. Module Details

### 5.1 Authentication and User Management Module

The **Authentication and User Management Module** is responsible for managing secure access to the system. It allows different types of users to register, log in, log out, and access only the features assigned to their role. Since the portal contains sensitive student, employee, company, and salary-related information, this module ensures that every user is properly authenticated before using the system.

The system provides separate access for Admin, Student, Employee, and Company/HR users. Role-based authentication ensures that students can manage only their own academic and career information, companies can manage employee and salary records, employees can view their own employment and salary details, and admins can monitor, verify, and generate reports.

This module also supports password management features such as password reset and password change, which improve account security and usability.

#### Features

- User registration
- Employer registration
- Login and logout
- Password management
- Role-based authentication
- Role-based authorization
- User account activation and deactivation
- Permission management for different user roles

#### Users

- Admin
- Student
- Employee
- Company/HR

#### Main Responsibilities

- Maintain user account details.
- Validate user login credentials.
- Restrict access based on user role.
- Protect sensitive information from unauthorized access.
- Allow users to manage their password securely.

### 5.2 Student Management Module

The **Student Management Module** manages all student-related academic, personal, and career information. Through this module, students can create and update their profile, add education details, mention skills, upload certification information, and maintain internship and placement status.

This module helps track the complete student lifecycle from education to employment. Students can update their current career status, such as studying, searching for a job, placed, doing an internship, or currently employed. The module can also store salary-related details for students who have been placed or employed.

For academic demonstration, this module is useful because it connects student education data with employment outcomes. Admin users can use this information to generate reports such as course completion counts, employment ratios, and degree-wise placement analysis.

#### Features

- Student profile creation
- Education details management
- Skills details management
- Certification details management
- Internship status tracking
- Placement status tracking
- Career status tracking
- Current employment status
- Salary details for placed or employed students

#### Main Responsibilities

- Store student personal and academic information.
- Maintain education history such as SSLC, HSC, diploma, degree, or other qualifications.
- Record student skills and certifications.
- Track internship and placement progress.
- Maintain current employment and salary details.
- Support reports related to student career growth and employment status.

### 5.3 Employee Management Module

The **Employee Management Module** manages employee records and employment-related details. It allows employee profiles to be created and maintained either by the employee or by the company/HR user. Companies can add employees using a unique identification value such as ULIN, which helps avoid duplicate or incorrect employee records.

This module maintains the employment roster of a company. It records whether an employee is currently active, resigned, terminated, or serving a notice period. These employment statuses help the admin verify whether an employee has multiple active employment records across different companies.

The module is important for maintaining accurate employment history and supporting verification. It also helps companies keep structured records of their workforce.

#### Features

- Employee profile creation
- Add employees by ULIN
- Maintain employee roster
- Employment history management
- Company and employee mapping
- Employment status tracking

#### Sample Employment Status

- Active
- Resigned
- Terminated
- Notice Period

#### Main Responsibilities

- Store employee profile details.
- Link employees with companies.
- Maintain employment records and work status.
- Track active and inactive employment.
- Support verification of duplicate or multiple active records.
- Help companies maintain an organized employee list.

### 5.4 Salary Management Module

The **Salary Management Module** manages salary-related information for employees. Companies or HR users can upload salary details, generate monthly salary slips, and maintain payment records. Employees can view their salary records and raise salary-related queries if they find any mismatch or issue.

This module can compare expected salary and paid salary to identify salary mismatch. For example, if an employee's expected salary is 30000 but the uploaded paid salary is 25000, the system can flag it for review.

The module may also expose an API so that other applications can consume salary-related data. This makes the system more flexible and useful for integration with external HR, payroll, or verification systems.

#### Features

- Monthly salary slip generation
- Salary details upload by company/HR
- Salary history maintenance
- Expected salary and paid salary comparison
- Salary mismatch identification
- Salary-related query support
- API support for other applications

#### Main Responsibilities

- Store employee salary records.
- Generate monthly salary slips.
- Allow employees to view salary details.
- Identify salary mismatch cases.
- Help admin verify salary-related issues.
- Allow integration with other applications through APIs.

### 5.5 Resume Generation Module

The **Resume Generation Module** automatically generates a formatted and printable resume for students or employees using the information already available in the portal. This reduces the need for users to manually enter resume data again.

The system can collect details such as personal information, education, skills, certifications, internships, placements, and employment history from existing records and arrange them into a professional resume format. This feature is especially useful for students applying for internships, placements, or jobs.

Since the resume is generated from verified or structured system data, it improves consistency and reduces mistakes.

#### Features

- Automatic resume generation
- Formatted resume layout
- Printable resume output
- Resume generation without repeated manual input
- Resume content based on profile, education, skill, and employment data

#### Main Responsibilities

- Collect required details from student or employee records.
- Arrange details in a professional resume format.
- Generate a printable resume.
- Reduce manual resume preparation work.
- Support students and employees in career development.

### 5.6 Admin / Registry Analytics Module

The **Admin / Registry Analytics Module** provides administrative control, verification, monitoring, and reporting features. Admin users can verify student, employee, company, employment, and salary records. The module also supports rule-based verification for academic implementation.

For example, the system can detect duplicate email addresses, duplicate mobile numbers, duplicate demo identity numbers, and multiple active employment records for the same employee. It can also identify salary mismatches by comparing expected salary with actual paid salary.

This module includes dashboards and reports that help admins understand the overall status of the system. Reports may include total users, number of students who completed SSLC/HSC, employer count, employed versus unemployed ratio, and degree-wise course completion breakdown.

#### Features

- Admin dashboard
- Total users count
- SSLC/HSC completion counts
- Employer count
- Employment ratio donut chart
- Employed vs. unemployed report
- Degree-wise course completion breakdown
- Duplicate profile checking
- Multiple active employment checking
- Salary mismatch checking
- Query management
- Report generation

#### Main Responsibilities

- Monitor the complete portal.
- Verify user, student, employee, company, employment, and salary records.
- Detect duplicate email, mobile number, and demo identity number.
- Identify employees with multiple active employment records.
- Identify salary mismatch cases.
- Manage employee salary-related queries.
- Generate useful reports for academic demonstration.

## 6. Rule-Based Verification

For academic implementation, the system uses simple rule-based verification instead of real-time government or banking APIs. This makes the project easier to implement while still demonstrating verification logic.

### Sample Verification Rules

- Check duplicate email address.
- Check duplicate mobile number.
- Check duplicate demo identity number.
- Check whether one employee has multiple active employment records.
- Compare expected salary and paid salary.
- Mark suspicious records for admin review.

## 7. Expected Outcome

The expected outcome of this project is a centralized web portal that manages student, employee, company, salary, verification, and query details in a structured way. The system reduces manual work, improves record accuracy, helps detect duplicate and suspicious records, and provides meaningful reports for admin users.

This project demonstrates important academic software development concepts such as authentication, role-based access, CRUD operations, database design, verification logic, dashboards, reports, and query handling.

## 8. Conclusion

The **Unified Students & Employment Lifecycle Portal** provides a complete student-to-employment lifecycle management system. It brings students, employees, companies, and administrators into one platform and supports basic verification, salary tracking, query management, and analytics.

By using this system, manual record handling can be reduced, duplicate records can be identified, employment status can be tracked, salary mismatches can be checked, and useful reports can be generated. Therefore, this portal is a practical and suitable academic project for demonstrating a real-time web-based management system.
