# Cure Health Platform - API Endpoints Documentation

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**Date:** October 12, 2025

---

## Table of Contents

1. [Authentication Endpoints](#authentication-endpoints)
2. [User Management Endpoints](#user-management-endpoints)
3. [Technician Endpoints](#technician-endpoints)
4. [Booking Management Endpoints](#booking-management-endpoints)
5. [Service Endpoints](#service-endpoints)
6. [Payment Endpoints](#payment-endpoints)
7. [Admin Endpoints](#admin-endpoints)
8. [Analytics & Reports Endpoints](#analytics--reports-endpoints)
9. [Notification Endpoints](#notification-endpoints)
10. [File Upload Endpoints](#file-upload-endpoints)
11. [Emergency Contacts Endpoints](#emergency-contacts-endpoints)
12. [Location Services Endpoints](#location-services-endpoints)
13. [Telemedicine Endpoints](#telemedicine-endpoints)
14. [Medication Management Endpoints](#medication-management-endpoints)
15. [Medical Forms & Questionnaires Endpoints](#medical-forms--questionnaires-endpoints)
16. [Care Plans & Treatment Plans Endpoints](#care-plans--treatment-plans-endpoints)
17. [Patient Education Endpoints](#patient-education-endpoints)
18. [Medical Alerts & Monitoring Endpoints](#medical-alerts--monitoring-endpoints)
19. [Integration APIs Endpoints](#integration-apis-endpoints)
20. [Compliance & Audit Endpoints](#compliance--audit-endpoints)
21. [Family Access Endpoints](#family-access-endpoints)
22. [System Health Endpoints](#system-health-endpoints)

---

## Authentication Endpoints

### POST `/home_cure/auth/register`
**Description:** Register a new user account  
**Access:** Public  
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "role": "user"
}
```
**Response:** User object with tokens  
**Status Codes:** 201 Created, 400 Bad Request, 409 Conflict

---

### POST `/home_cure/auth/login` (alias: `/home_cure/auth/token`)
**Description:** Login user and receive JWT access token  
**Access:** Public  
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": { "id": 1, "email": "...", "role": "user" }
}
```
**Status Codes:** 200 OK, 401 Unauthorized

---

### POST `/home_cure/auth/refresh-token`
**Description:** Refresh access token using refresh token  
**Access:** Public  
**Request Body:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```
**Response:** New access token  
**Status Codes:** 200 OK, 401 Unauthorized

---

### GET `/home_cure/auth/me`
**Description:** Get current authenticated user information  
**Access:** Protected (requires JWT)  
**Response:** Current user object with profile details  
**Status Codes:** 200 OK, 401 Unauthorized

---

## User Management Endpoints

### PUT `/home_cure/users/profile`
**Description:** Update user profile information  
**Access:** Protected (User, Technician, Admin)  
**Request Body:**
```json
{
  "full_name": "Jane Doe",
  "phone_number": "+1987654321",
  "address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "bio": "Healthcare professional"
}
```
**Response:** Updated user object  
**Status Codes:** 200 OK, 400 Bad Request, 404 Not Found

---

### GET `/home_cure/users/health-records`
**Description:** Get user's health records history  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `page`, `limit`, `record_type`, `date_from`, `date_to`  
**Response:** Paginated list of health records  
**Status Codes:** 200 OK, 401 Unauthorized

---

### POST `/home_cure/users/health-records`
**Description:** Create a new health record for the user  
**Access:** Protected (User, Technician, Admin)  
**Request Body:**
```json
{
  "record_type": "checkup",
  "record_date": "2025-10-12",
  "diagnosis": "Routine checkup - healthy",
  "vitals": {
    "blood_pressure": "120/80",
    "temperature": "98.6",
    "heart_rate": "72"
  },
  "medications": ["Vitamin D"],
  "provider_name": "Dr. Smith"
}
```
**Response:** Created health record object  
**Status Codes:** 201 Created, 400 Bad Request

---

### PUT `/home_cure/users/health-records/{record_id}`
**Description:** Update health record details  
**Access:** Protected (User, Technician, Admin)  
**Request Body:**
```json
{
  "diagnosis": "Updated diagnosis",
  "treatment": "Updated treatment plan",
  "medications": ["Updated medication list"],
  "follow_up_required": "yes",
  "follow_up_date": "2025-11-15"
}
```
**Response:** Updated health record object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

---

### DELETE `/home_cure/users/health-records/{record_id}`
**Description:** Delete a health record  
**Access:** Protected (User, Admin)  
**Response:** Success message  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### GET `/home_cure/technicians/health-records`
**Description:** Get health records for technician's assigned bookings  
**Access:** Protected (Technician, Admin)  
**Query Params:** `page`, `limit`, `booking_id`, `user_id`, `date_from`, `date_to`  
**Response:** Paginated list of health records for assigned bookings  
**Status Codes:** 200 OK, 403 Forbidden

---

### POST `/home_cure/health-records/{record_id}/prescriptions`
**Description:** Add prescription to health record  
**Access:** Protected (Technician, Admin)  
**Request Body:**
```json
{
  "medication_name": "Amoxicillin",
  "dosage": "500mg",
  "frequency": "3 times daily",
  "duration_days": 7,
  "instructions": "Take with food"
}
```
**Response:** Created prescription object  
**Status Codes:** 201 Created, 400 Bad Request, 403 Forbidden

---

### GET `/home_cure/health-records/{record_id}/prescriptions`
**Description:** Get prescriptions for a health record  
**Access:** Protected (User, Technician, Admin)  
**Response:** List of prescriptions  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

## Emergency Contacts Endpoints

### POST `/home_cure/users/emergency-contacts`
**Description:** Add emergency contact  
**Access:** Protected (User, Admin)  
**Request Body:**
```json
{
  "name": "John Doe",
  "relationship": "Spouse",
  "phone_number": "+1234567890",
  "email": "john@example.com",
  "address": "123 Emergency St, City, State"
}
```
**Response:** Created emergency contact object  
**Status Codes:** 201 Created, 400 Bad Request

---

### GET `/home_cure/users/emergency-contacts`
**Description:** Get user's emergency contacts  
**Access:** Protected (User, Technician, Admin)  
**Response:** List of emergency contacts  
**Status Codes:** 200 OK

---

### PUT `/home_cure/users/emergency-contacts/{contact_id}`
**Description:** Update emergency contact  
**Access:** Protected (User, Admin)  
**Response:** Updated emergency contact object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

---

### DELETE `/home_cure/users/emergency-contacts/{contact_id}`
**Description:** Delete emergency contact  
**Access:** Protected (User, Admin)  
**Response:** Success message  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

## Location Services Endpoints

### GET `/home_cure/technicians/nearby`
**Description:** Find nearby available technicians  
**Access:** Protected (User, Admin)  
**Query Params:** `latitude`, `longitude`, `radius_km`, `specialization`, `service_id`  
**Response:** List of nearby technicians with distance  
**Status Codes:** 200 OK, 400 Bad Request

---

### GET `/home_cure/services/areas`
**Description:** Get available service areas  
**Access:** Public  
**Response:** List of service areas with coverage info  
**Status Codes:** 200 OK

---

### PUT `/home_cure/technicians/profile`
**Description:** Update technician profile and availability  
**Access:** Protected (Technician, Admin)  
**Request Body:**
```json
{
  "specialization": "Registered Nurse",
  "certifications": ["RN", "CPR", "BLS"],
  "experience_years": 5,
  "license_number": "RN123456",
  "bio": "Experienced healthcare professional...",
  "availability_schedule": {
    "monday": ["09:00-17:00"],
    "tuesday": ["09:00-17:00"],
    "friday": ["09:00-14:00"]
  },
  "service_areas": ["Manhattan", "Brooklyn"],
  "is_available": true
}
```
**Response:** Updated technician profile  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

---

### GET `/home_cure/technicians/earnings`
**Description:** Get technician's earnings history and statistics  
**Access:** Protected (Technician, Admin)  
**Query Params:** `page`, `limit`, `date_from`, `date_to`, `payment_status`  
**Response:**
```json
{
  "total_earnings": 5000.00,
  "pending_earnings": 500.00,
  "paid_earnings": 4500.00,
  "commission_total": 750.00,
  "earnings": [
    {
      "id": 1,
      "booking_id": 123,
      "amount": 100.00,
      "commission_rate": 0.15,
      "net_earnings": 85.00,
      "payment_status": "paid",
      "payment_date": "2025-10-01"
    }
  ],
  "pagination": { "page": 1, "total": 50 }
}
```
**Status Codes:** 200 OK, 403 Forbidden

---

### POST `/home_cure/technicians/earnings/{earning_id}/payout-request`
**Description:** Request payout for earned amount  
**Access:** Protected (Technician)  
**Request Body:**
```json
{
  "payment_method": "bank_transfer",
  "account_details": {
    "bank_name": "Chase Bank",
    "account_number": "****1234",
    "routing_number": "021000021"
  }
}
```
**Response:** Payout request object  
**Status Codes:** 201 Created, 400 Bad Request, 403 Forbidden

---

### GET `/home_cure/admin/earnings`
**Description:** Get all technician earnings for admin management  
**Access:** Protected (Admin)  
**Query Params:** `page`, `limit`, `technician_id`, `payment_status`, `date_from`, `date_to`  
**Response:** Paginated list of all earnings  
**Status Codes:** 200 OK, 403 Forbidden

---

### PUT `/home_cure/admin/earnings/{earning_id}/pay`
**Description:** Mark earning as paid  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "payment_date": "2025-10-12",
  "transaction_id": "TXN_123456",
  "notes": "Paid via bank transfer"
}
```
**Response:** Updated earning object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

### GET `/home_cure/technicians/bookings`
**Description:** Get bookings assigned to the technician  
**Access:** Protected (Technician, Admin)  
**Query Params:** `page`, `limit`, `status`, `date_from`, `date_to`  
**Response:** Paginated list of bookings assigned to technician  
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/technicians/{technician_id}`
**Description:** Get technician public profile (for users to view)  
**Access:** Protected (User, Technician, Admin)  
**Response:** Technician profile with ratings and reviews  
**Status Codes:** 200 OK, 404 Not Found

---

### GET `/home_cure/technicians`
**Description:** List all available technicians  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `page`, `limit`, `specialization`, `service_area`, `min_rating`  
**Response:** Paginated list of technicians  
**Status Codes:** 200 OK

---

### GET `/home_cure/technicians/{technician_id}/availability`
**Description:** Get technician's availability schedule  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `date_from`, `date_to`  
**Response:** Technician's availability slots  
**Status Codes:** 200 OK, 404 Not Found

---

### POST `/home_cure/technicians/availability/slots`
**Description:** Add availability time slot  
**Access:** Protected (Technician, Admin)  
**Request Body:**
```json
{
  "date": "2025-10-15",
  "start_time": "09:00",
  "end_time": "17:00",
  "is_recurring": true,
  "recurring_days": ["monday", "tuesday", "wednesday"]
}
```
**Response:** Created availability slot  
**Status Codes:** 201 Created, 400 Bad Request, 403 Forbidden

---

### PUT `/home_cure/technicians/availability/slots/{slot_id}`
**Description:** Update availability time slot  
**Access:** Protected (Technician, Admin)  
**Request Body:**
```json
{
  "start_time": "10:00",
  "end_time": "16:00",
  "is_available": false
}
```
**Response:** Updated availability slot  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### DELETE `/home_cure/technicians/availability/slots/{slot_id}`
**Description:** Delete availability time slot  
**Access:** Protected (Technician, Admin)  
**Response:** Success message  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

## Booking Management Endpoints

### POST `/home_cure/bookings`
**Description:** Create a new booking (automatically generates QR code)  
**Access:** Protected (User, Admin)  
**Request Body:**
```json
{
  "service_id": 1,
  "scheduled_date": "2025-10-15",
  "scheduled_time": "14:00",
  "service_address": "123 Main St, New York, NY 10001",
  "user_notes": "Please ring doorbell",
  "payment_method": "credit_card"
}
```
**Response:**
```json
{
  "id": 123,
  "status": "pending",
  "qr_code": "data:image/png;base64,iVBORw0KGgo...",
  "qr_code_data": "BOOKING-123-2025-10-15",
  "total_amount": 100.00,
  "created_at": "2025-10-12T10:30:00Z"
}
```
**Status Codes:** 201 Created, 400 Bad Request

---

### GET `/home_cure/bookings`
**Description:** Get bookings filtered by user role  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `page`, `limit`, `status`, `date_from`, `date_to`, `technician_id`, `user_id`  
**Behavior:**
- **User**: Returns only their own bookings
- **Technician**: Returns bookings assigned to them
- **Admin**: Returns all bookings (with filters)  
**Response:** Paginated list of bookings  
**Status Codes:** 200 OK

---

### GET `/home_cure/bookings/{booking_id}`
**Description:** Get specific booking details  
**Access:** Protected (User, Technician, Admin)  
**Response:** Complete booking object with QR code, user, technician, service details  
**Status Codes:** 200 OK, 404 Not Found, 403 Forbidden

---

### PUT `/home_cure/bookings/{booking_id}`
**Description:** Update booking status/details  
**Access:** Protected (User, Technician, Admin)  
**Request Body:**
```json
{
  "status": "confirmed",
  "technician_notes": "Will arrive 10 minutes early",
  "scheduled_date": "2025-10-16"
}
```
**Response:** Updated booking object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

---

### POST `/home_cure/bookings/{booking_id}/rate`
**Description:** Rate and review a completed booking  
**Access:** Protected (User)  
**Request Body:**
```json
{
  "rating": 5,
  "review": "Excellent service! Very professional."
}
```
**Response:** Updated booking with rating  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

---

### GET `/home_cure/technicians/{technician_id}/reviews`
**Description:** Get all reviews for a technician  
**Access:** Public  
**Query Params:** `page`, `limit`, `min_rating`, `sort_by` (newest/rating)  
**Response:** Paginated list of reviews with booking details  
**Status Codes:** 200 OK, 404 Not Found

---

### PUT `/home_cure/bookings/{booking_id}/review`
**Description:** Update existing review  
**Access:** Protected (User)  
**Request Body:**
```json
{
  "rating": 4,
  "review": "Updated review text"
}
```
**Response:** Updated review object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

---

### DELETE `/home_cure/admin/reviews/{review_id}`
**Description:** Delete inappropriate review (Admin only)  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "reason": "Inappropriate content"
}
```
**Response:** Success message  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

### POST `/home_cure/bookings/{booking_id}/cancel`
**Description:** Cancel a booking  
**Access:** Protected (User, Admin)  
**Request Body:**
```json
{
  "reason": "Schedule conflict"
}
```
**Response:** Cancelled booking object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

---

### POST `/home_cure/bookings/{booking_id}/regenerate-qr`
**Description:** Regenerate QR code for booking  
**Access:** Protected (User, Technician, Admin)  
**Response:**
```json
{
  "qr_code": "data:image/png;base64,new_qr_code...",
  "qr_code_data": "BOOKING-123-2025-10-15"
}
```
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### POST `/home_cure/bookings/scan-qr`
**Description:** Scan and validate QR code for check-in  
**Access:** Protected (Technician, Admin)  
**Request Body:**
```json
{
  "qr_code_data": "BOOKING-123-2025-10-15",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  }
}
```
**Response:** Booking details with check-in confirmation  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

---

### GET `/home_cure/bookings/{booking_id}/validate-qr`
**Description:** Validate QR code data without check-in  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `qr_code_data`  
**Response:** Validation result with booking info  
**Status Codes:** 200 OK, 400 Bad Request, 404 Not Found

## Service Endpoints

### GET `/home_cure/services`
**Description:** Get available services  
**Access:** Public  
**Query Params:** `category`, `is_active`, `page`, `limit`  
**Response:** List of available services  
**Status Codes:** 200 OK

---

### GET `/home_cure/services/{service_id}`
**Description:** Get service details  
**Access:** Public  
**Response:** Service object with description, price, duration  
**Status Codes:** 200 OK, 404 Not Found

---

### POST `/home_cure/services`
**Description:** Create a new service (Admin only)  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "name": "Home Nursing Care",
  "description": "Professional nursing care at home",
  "price": 100.00,
  "duration_minutes": 60,
  "category": "nursing",
  "is_active": true
}
```
**Response:** Created service object  
**Status Codes:** 201 Created, 400 Bad Request, 403 Forbidden

---

### PUT `/home_cure/services/{service_id}`
**Description:** Update service details (Admin only)  
**Access:** Protected (Admin)  
**Response:** Updated service object  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### GET `/home_cure/services/categories`
**Description:** Get all service categories  
**Access:** Public  
**Response:** List of available categories  
**Status Codes:** 200 OK

---

### POST `/home_cure/admin/services/categories`
**Description:** Create new service category  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "name": "Nursing Care",
  "description": "Professional nursing services",
  "is_active": true
}
```
**Response:** Created category object  
**Status Codes:** 201 Created, 400 Bad Request, 403 Forbidden

---

### PUT `/home_cure/admin/services/categories/{category_id}`
**Description:** Update service category  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "name": "Updated Category Name",
  "description": "Updated description",
  "is_active": false
}
```
**Response:** Updated category object  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### DELETE `/home_cure/admin/services/categories/{category_id}`
**Description:** Delete service category  
**Access:** Protected (Admin)  
**Response:** Success message  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

## Admin Endpoints

### GET `/home_cure/admin/users`
**Description:** Get all users for admin management  
**Access:** Protected (Admin)  
**Query Params:** `page`, `limit`, `role`, `is_active`, `search`  
**Response:** Paginated list of users with filters  
**Status Codes:** 200 OK, 403 Forbidden

---

### PUT `/home_cure/admin/users/{user_id}`
**Description:** Update user status/role  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "is_active": false,
  "role": "technician",
  "is_verified": true
}
```
**Response:** Updated user object  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### GET `/home_cure/admin/technicians`
**Description:** Get all technicians for admin management  
**Access:** Protected (Admin)  
**Query Params:** `page`, `limit`, `is_verified`, `is_active`, `specialization`  
**Response:** Paginated list of technicians  
**Status Codes:** 200 OK, 403 Forbidden

---

### PUT `/home_cure/admin/technicians/{technician_id}`
**Description:** Update technician status (verify, activate/deactivate)  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "is_verified": true,
  "is_active": true
}
```
**Response:** Updated technician object  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### POST `/home_cure/technicians/apply`
**Description:** Apply to become a technician  
**Access:** Protected (User)  
**Request Body:**
```json
{
  "specialization": "Registered Nurse",
  "experience_years": 5,
  "license_number": "RN123456",
  "certifications": ["RN", "CPR", "BLS"],
  "service_areas": ["Manhattan", "Brooklyn"],
  "bio": "Experienced healthcare professional...",
  "documents": ["license_url", "certification_url"]
}
```
**Response:** Application submitted confirmation  
**Status Codes:** 201 Created, 400 Bad Request, 409 Conflict

---

### GET `/home_cure/admin/technicians/applications`
**Description:** Get technician applications for review  
**Access:** Protected (Admin)  
**Query Params:** `page`, `limit`, `status` (pending/approved/rejected)  
**Response:** Paginated list of technician applications  
**Status Codes:** 200 OK, 403 Forbidden

---

### PUT `/home_cure/admin/technicians/{technician_id}/approve`
**Description:** Approve technician application  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "review_notes": "Application approved - all documents verified"
}
```
**Response:** Approved technician object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

### GET `/home_cure/admin/bookings`
**Description:** Get all bookings for admin management  
**Access:** Protected (Admin)  
**Query Params:** `page`, `limit`, `status`, `date_from`, `date_to`, `user_id`, `technician_id`  
**Response:** Paginated list of all bookings  
**Status Codes:** 200 OK, 403 Forbidden

---

### PUT `/home_cure/admin/bookings/{booking_id}/assign`
**Description:** Assign booking to technician  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "technician_id": 5
}
```
**Response:** Updated booking with assigned technician  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found

---

### PUT `/home_cure/admin/bookings/{booking_id}/status`
**Description:** Update booking status  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "status": "confirmed",
  "admin_notes": "Manually confirmed by admin"
}
```
**Response:** Updated booking object  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### POST `/home_cure/admin/bookings/bulk-assign`
**Description:** Bulk assign bookings to technicians  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "assignments": [
    { "booking_id": 123, "technician_id": 5 },
    { "booking_id": 124, "technician_id": 7 }
  ]
}
```
**Response:** Bulk assignment results  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

---

### POST `/home_cure/admin/notifications/bulk-send`
**Description:** Send bulk notifications  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "user_ids": [1, 2, 3],
  "title": "System Maintenance",
  "message": "Scheduled maintenance tonight",
  "notification_type": "system",
  "priority": "high"
}
```
**Response:** Bulk send results with success/failure counts  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

### GET `/home_cure/admin/logs`
**Description:** Get admin activity logs  
**Access:** Protected (Admin)  
**Query Params:** `page`, `limit`, `action`, `entity_type`, `date_from`, `date_to`, `admin_user_id`  
**Response:** Paginated list of admin logs  
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/admin/settings`
**Description:** Get system settings  
**Access:** Protected (Admin)  
**Query Params:** `category`  
**Response:** List of system settings  
**Status Codes:** 200 OK, 403 Forbidden

---

### PUT `/home_cure/admin/settings/{setting_id}`
**Description:** Update system settings  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "value": "24",
  "description": "Hours before booking can be cancelled"
}
```
**Response:** Updated setting object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

---

## Payment Endpoints

### POST `/home_cure/payments/process`
**Description:** Process payment for booking  
**Access:** Protected (User, Admin)  
**Request Body:**
```json
{
  "booking_id": 123,
  "payment_method": "credit_card",
  "card_details": {
    "number": "4111111111111111",
    "expiry_month": "12",
    "expiry_year": "2025",
    "cvv": "123"
  },
  "billing_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001"
  }
}
```
**Response:** Payment confirmation object  
**Status Codes:** 200 OK, 400 Bad Request, 402 Payment Required

---

### GET `/home_cure/payments/{payment_id}`
**Description:** Get payment details  
**Access:** Protected (User, Admin)  
**Response:** Payment object with transaction details  
**Status Codes:** 200 OK, 403 Forbidden, 404 Not Found

---

### POST `/home_cure/payments/{payment_id}/refund`
**Description:** Process refund for payment  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "amount": 50.00,
  "reason": "Service cancelled"
}
```
**Response:** Refund confirmation object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

---

### GET `/home_cure/users/payments`
**Description:** Get user's payment history  
**Access:** Protected (User, Admin)  
**Query Params:** `page`, `limit`, `status`, `date_from`, `date_to`  
**Response:** Paginated list of payments  
**Status Codes:** 200 OK, 403 Forbidden

## Analytics & Reports Endpoints

### GET `/home_cure/admin/reports/bookings`
**Description:** Get booking analytics data  
**Access:** Protected (Admin)  
**Query Params:** `date_from`, `date_to`, `group_by` (day/week/month)  
**Response:**
```json
{
  "total_bookings": 500,
  "completed_bookings": 450,
  "cancelled_bookings": 30,
  "pending_bookings": 20,
  "bookings_by_date": [
    { "date": "2025-10-01", "count": 15 },
    { "date": "2025-10-02", "count": 18 }
  ]
}
```
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/admin/reports/revenue`
**Description:** Get revenue analytics  
**Access:** Protected (Admin)  
**Query Params:** `date_from`, `date_to`, `group_by`  
**Response:**
```json
{
  "total_revenue": 50000.00,
  "platform_commission": 7500.00,
  "technician_earnings": 42500.00,
  "revenue_by_date": [
    { "date": "2025-10-01", "amount": 1500.00 }
  ]
}
```
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/admin/reports/technicians`
**Description:** Get technician performance data  
**Access:** Protected (Admin)  
**Query Params:** `date_from`, `date_to`, `limit`  
**Response:**
```json
{
  "top_technicians": [
    {
      "technician_id": 5,
      "name": "Jane Smith",
      "total_bookings": 50,
      "average_rating": 4.8,
      "total_earnings": 5000.00
    }
  ]
}
```
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/admin/reports/export`
**Description:** Export data as CSV  
**Access:** Protected (Admin)  
**Query Params:** `report_type` (bookings/revenue/technicians), `date_from`, `date_to`  
**Response:** CSV file download  
**Status Codes:** 200 OK, 403 Forbidden

---

### POST `/home_cure/admin/data/import`
**Description:** Import data from CSV  
**Access:** Protected (Admin)  
**Request:** Multipart form data with CSV file  
**Validation:** CSV format validation, data integrity checks  
**Response:** Import results with success/error counts  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

---

### GET `/home_cure/users/data/export`
**Description:** Export user's personal data  
**Access:** Protected (User)  
**Query Params:** `data_type` (all/health_records/bookings)  
**Response:** JSON data export  
**Status Codes:** 200 OK

---

## Telemedicine Endpoints

### POST `/home_cure/telemedicine/sessions`
**Description:** Create a telemedicine session (video call)  
**Access:** Protected (User, Technician)  
**Request Body:**
```json
{
  "booking_id": 123,
  "session_type": "video",
  "scheduled_start": "2025-10-15T14:00:00Z",
  "duration_minutes": 30,
  "notes": "Follow-up consultation"
}
```
**Response:** Session details with connection info  
**Status Codes:** 201 Created, 400 Bad Request

---

### GET `/home_cure/telemedicine/sessions/{session_id}`
**Description:** Get telemedicine session details  
**Access:** Protected (User, Technician, Admin)  
**Response:** Session information with status and recordings  
**Status Codes:** 200 OK, 404 Not Found

---

### PUT `/home_cure/telemedicine/sessions/{session_id}/status`
**Description:** Update session status (start/end/cancel)  
**Access:** Protected (User, Technician)  
**Request Body:**
```json
{
  "status": "started",
  "notes": "Session completed successfully"
}
```
**Response:** Updated session object  
**Status Codes:** 200 OK, 400 Bad Request, 403 Forbidden

---

## Medication Management Endpoints

### POST `/home_cure/medications`
**Description:** Add medication to user's profile  
**Access:** Protected (User, Technician, Admin)  
**Request Body:**
```json
{
  "name": "Lisinopril",
  "dosage": "10mg",
  "frequency": "once daily",
  "start_date": "2025-10-12",
  "end_date": "2025-12-12",
  "prescribing_doctor": "Dr. Smith",
  "reminders_enabled": true
}
```
**Response:** Created medication object  
**Status Codes:** 201 Created, 400 Bad Request

---

### GET `/home_cure/medications`
**Description:** Get user's medications  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `active_only`, `page`, `limit`  
**Response:** List of medications with adherence tracking  
**Status Codes:** 200 OK

---

### POST `/home_cure/medications/{medication_id}/taken`
**Description:** Log medication taken  
**Access:** Protected (User)  
**Request Body:**
```json
{
  "taken_at": "2025-10-12T08:00:00Z",
  "notes": "Taken with breakfast"
}
```
**Response:** Medication adherence record  
**Status Codes:** 201 Created, 400 Bad Request

---

## Medical Forms & Questionnaires Endpoints

### GET `/home_cure/forms/templates`
**Description:** Get available form templates  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `category` (intake/feedback/followup)  
**Response:** List of form templates  
**Status Codes:** 200 OK

---

### POST `/home_cure/forms/submissions`
**Description:** Submit a completed form  
**Access:** Protected (User, Technician, Admin)  
**Request Body:**
```json
{
  "template_id": "intake_form_v1",
  "booking_id": 123,
  "responses": {
    "question_1": "Yes",
    "question_2": "Mild pain"
  }
}
```
**Response:** Form submission confirmation  
**Status Codes:** 201 Created, 400 Bad Request

---

## Care Plans & Treatment Plans Endpoints

### POST `/home_cure/care-plans`
**Description:** Create a care plan  
**Access:** Protected (Technician, Admin)  
**Request Body:**
```json
{
  "user_id": 123,
  "title": "Post-Surgery Recovery Plan",
  "start_date": "2025-10-12",
  "end_date": "2025-11-23",
  "goals": ["Improve mobility", "Reduce pain"],
  "assigned_technician_id": 5
}
```
**Response:** Created care plan object  
**Status Codes:** 201 Created, 400 Bad Request, 403 Forbidden

---

### GET `/home_cure/care-plans`
**Description:** Get care plans  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `user_id`, `status`, `page`, `limit`  
**Response:** Paginated list of care plans  
**Status Codes:** 200 OK

---

## Patient Education Endpoints

### GET `/home_cure/education/content`
**Description:** Get educational content  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `category`, `condition`, `page`, `limit`  
**Response:** List of educational articles/videos  
**Status Codes:** 200 OK

---

### POST `/home_cure/education/content/{content_id}/view`
**Description:** Track content view for analytics  
**Access:** Protected (User, Technician, Admin)  
**Request Body:**
```json
{
  "view_duration_seconds": 300,
  "completed": true,
  "rating": 5
}
```
**Response:** View tracking confirmation  
**Status Codes:** 201 Created

---

## Medical Alerts & Monitoring Endpoints

### POST `/home_cure/alerts`
**Description:** Create a medical alert  
**Access:** Protected (Technician, Admin)  
**Request Body:**
```json
{
  "user_id": 123,
  "alert_type": "vital_signs",
  "severity": "high",
  "title": "High Blood Pressure Alert",
  "message": "Blood pressure reading: 180/110",
  "notification_channels": ["email", "sms", "push"]
}
```
**Response:** Created alert configuration  
**Status Codes:** 201 Created, 400 Bad Request

---

### GET `/home_cure/alerts`
**Description:** Get active alerts  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `user_id`, `status`, `severity`  
**Response:** List of alerts and triggered notifications  
**Status Codes:** 200 OK

---

## Integration APIs Endpoints

### POST `/home_cure/integrations/lab-results`
**Description:** Receive lab results from external labs  
**Access:** Protected (Admin) - API Key required  
**Request Body:**
```json
{
  "user_id": 123,
  "lab_order_id": "LAB_12345",
  "test_type": "blood_panel",
  "results": {
    "glucose": { "value": 95, "unit": "mg/dL", "status": "normal" }
  }
}
```
**Response:** Lab results processing confirmation  
**Status Codes:** 200 OK, 400 Bad Request

---

### GET `/home_cure/integrations/insurance/eligibility`
**Description:** Check insurance eligibility  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `user_id`, `service_id`  
**Response:** Insurance coverage information  
**Status Codes:** 200 OK, 400 Bad Request

---

## Compliance & Audit Endpoints

### GET `/home_cure/audit/logs`
**Description:** Get detailed audit logs for compliance  
**Access:** Protected (Admin)  
**Query Params:** `user_id`, `entity_type`, `action`, `date_from`, `date_to`  
**Response:** Detailed audit trail  
**Status Codes:** 200 OK, 403 Forbidden

---

## Family Access Endpoints

### POST `/home_cure/family/access-request`
**Description:** Request family access to patient data  
**Access:** Public (with verification)  
**Request Body:**
```json
{
  "patient_email": "patient@example.com",
  "relationship": "spouse",
  "requester_name": "John Doe",
  "requester_email": "john@example.com"
}
```
**Response:** Access request submitted  
**Status Codes:** 201 Created, 400 Bad Request

---

### GET `/home_cure/family/patient-data`
**Description:** Access patient's data as family member  
**Access:** Protected (Family)  
**Query Params:** `patient_id`, `data_type`  
**Response:** Authorized patient data  
**Status Codes:** 200 OK, 403 Forbidden

---
**Description:** Get key performance indicators for dashboard  
**Access:** Protected (Admin)  
**Response:**
```json
{
  "total_users": 1000,
  "total_technicians": 50,
  "active_bookings": 25,
  "total_revenue": 50000.00,
  "average_rating": 4.7,
  "bookings_today": 5,
  "new_users_this_month": 100
}
```
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/admin/analytics/user-retention`
**Description:** Get user retention analytics  
**Access:** Protected (Admin)  
**Query Params:** `date_from`, `date_to`, `cohort_period` (monthly/weekly)  
**Response:** User retention metrics and charts  
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/admin/analytics/service-popularity`
**Description:** Get service popularity analytics  
**Access:** Protected (Admin)  
**Query Params:** `date_from`, `date_to`, `group_by` (service/category)  
**Response:** Service usage statistics  
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/admin/analytics/geographic-distribution`
**Description:** Get geographic distribution of users and bookings  
**Access:** Protected (Admin)  
**Query Params:** `date_from`, `date_to`, `region`  
**Response:** Geographic analytics data  
**Status Codes:** 200 OK, 403 Forbidden

## Notification Endpoints

### GET `/home_cure/notifications`
**Description:** Get user notifications  
**Access:** Protected (User, Technician, Admin)  
**Query Params:** `page`, `limit`, `is_read`, `notification_type`  
**Response:** Paginated list of notifications  
**Status Codes:** 200 OK

---

### PUT `/home_cure/notifications/{notification_id}/read`
**Description:** Mark notification as read  
**Access:** Protected (User, Technician, Admin)  
**Response:** Updated notification object  
**Status Codes:** 200 OK, 404 Not Found

---

### PUT `/home_cure/notifications/read-all`
**Description:** Mark all notifications as read  
**Access:** Protected (User, Technician, Admin)  
**Response:** Success message with count  
**Status Codes:** 200 OK

---

### GET `/home_cure/notifications/unread-count`
**Description:** Get count of unread notifications  
**Access:** Protected (User, Technician, Admin)  
**Response:**
```json
{
  "unread_count": 5
}
```
**Status Codes:** 200 OK

---

## File Upload Endpoints

### POST `/home_cure/upload/profile-picture`
**Description:** Upload user profile picture  
**Access:** Protected (User, Technician, Admin)  
**Request:** Multipart form data with image file  
**Validation:** Max 5MB, formats: JPG, PNG, WebP  
**Response:**
```json
{
  "url": "/uploads/profile/user_123_profile.jpg",
  "size": 2048576,
  "format": "jpg"
}
```
**Status Codes:** 200 OK, 400 Bad Request, 413 Payload Too Large

---

### POST `/home_cure/upload/documents`
**Description:** Upload health documents  
**Access:** Protected (User, Technician, Admin)  
**Request:** Multipart form data with document file  
**Validation:** Max 10MB, formats: PDF, JPG, PNG  
**Response:**
```json
{
  "url": "/uploads/documents/doc_456_healthrecord.pdf",
  "size": 5242880,
  "format": "pdf",
  "filename": "lab_results.pdf"
}
```
**Status Codes:** 200 OK, 400 Bad Request, 413 Payload Too Large

---

## System Health Endpoints

### GET `/home_cure/health`
**Description:** System health check  
**Access:** Public  
**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0",
  "timestamp": "2025-10-12T10:30:00Z"
}
```
**Status Codes:** 200 OK, 503 Service Unavailable

---

### POST `/home_cure/admin/system/backup`
**Description:** Create system backup  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "backup_type": "full", // full/incremental
  "include_files": true,
  "description": "Monthly backup"
}
```
**Response:** Backup job status  
**Status Codes:** 202 Accepted, 403 Forbidden

---

### POST `/home_cure/admin/system/cache/clear`
**Description:** Clear system cache  
**Access:** Protected (Admin)  
**Request Body:**
```json
{
  "cache_type": "all", // all/database/api
  "reason": "Performance optimization"
}
```
**Response:** Cache clear confirmation  
**Status Codes:** 200 OK, 403 Forbidden

---

### GET `/home_cure/admin/system/logs`
**Description:** Get system logs  
**Access:** Protected (Admin)  
**Query Params:** `level` (error/warn/info), `date_from`, `date_to`, `limit`  
**Response:** System logs  
**Status Codes:** 200 OK, 403 Forbidden

### GET `/home_cure/`
**Description:** API root information  
**Access:** Public  
**Response:**
```json
{
  "message": "Welcome to Home Cure API",
  "version": "1.0.0",
  "endpoints": "/home_cure/docs"
}
```
**Status Codes:** 200 OK

---

## Response Format Standards

### Success Response
```json
{
  "data": { /* response data */ },
  "message": "Success"
}
```

### Error Response
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Paginated Response
```json
{
  "data": [ /* array of items */ ],
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 10,
    "pages": 10
  }
}
```

---

## Authentication Requirements

### JWT Bearer Token
Required for all endpoints except:
- `POST /home_cure/auth/register`
- `POST /home_cure/auth/login`
- `POST /home_cure/auth/token`
- `POST /home_cure/auth/refresh-token`
- `GET /home_cure/services`
- `GET /home_cure/services/{id}`
- `GET /home_cure/health`
- `GET /home_cure/`

**Header Format:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Role-Based Access Control

| Role | Access Level |
|------|-------------|
| **user** | Own bookings, health records, profile |
| **technician** | Assigned bookings, earnings, technician profile |
| **admin** | All endpoints, user management, reports |

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 413 | Payload Too Large - File size exceeded |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## CORS Configuration

Allowed origins:
- `http://localhost:3000`
- `http://localhost:3001`
- `https://momin-mohasin.vercel.app`
- `https://kar-lo.vercel.app`

---

## Rate Limiting

- **Public endpoints:** 100 requests/minute
- **Authenticated endpoints:** 1000 requests/minute
- **File uploads:** 10 requests/minute

---

## Documentation

- **Swagger UI:** http://localhost:8000/home_cure/docs
- **ReDoc:** http://localhost:8000/home_cure/redoc
- **OpenAPI JSON:** http://localhost:8000/home_cure/openapi.json

---

## Summary

**Total Endpoints:** 120+

**Categories:**
- Authentication: 4 endpoints
- User Management: 6 endpoints
- Technician: 8 endpoints
- Booking Management: 10 endpoints
- Services: 6 endpoints
- Payment: 4 endpoints
- Admin: 15 endpoints
- Analytics & Reports: 8 endpoints
- Notifications: 4 endpoints
- File Upload: 2 endpoints
- Emergency Contacts: 4 endpoints
- Location Services: 2 endpoints
- Telemedicine: 3 endpoints
- Medication Management: 3 endpoints
- Medical Forms & Questionnaires: 2 endpoints
- Care Plans & Treatment Plans: 2 endpoints
- Patient Education: 2 endpoints
- Medical Alerts & Monitoring: 2 endpoints
- Integration APIs: 2 endpoints
- Compliance & Audit: 1 endpoint
- Family Access: 2 endpoints
- System Health: 5 endpoints

---

**Last Updated:** October 12, 2025  
**API Version:** 1.0.0  
**Status:** Comprehensive API Specification - Enterprise Healthcare Platform Ready
