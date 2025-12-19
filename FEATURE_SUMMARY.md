# Secure Driver Management Feature

## Summary
Added secure password management for drivers with a redesigned UI for managing driver accounts.

## Changes Made

### Backend Changes
1. **Models (`backend/app/models.py`)**
   - Added `password_hash` field to User model (NOT plain text)
   - Uses bcrypt hashing with SHA-256 pre-hashing for security

2. **Schemas (`backend/app/schemas.py`)**
   - Added `password` field to `UserCreate` schema
   - Added new `UserUpdate` schema for updating drivers

3. **API Endpoints (`backend/app/main.py`)**
   - Updated `POST /api/users` to hash passwords before storing
   - Added `PUT /api/admin/users/{user_id}` for editing drivers (admin only)
   - Added `DELETE /api/admin/users/{user_id}` for deleting drivers (admin only, soft delete)
   - All passwords are hashed using bcrypt with SHA-256 pre-hashing

### Frontend Changes
1. **New Component (`frontend/src/components/DriverForm.vue`)**
   - Modal form for adding/editing drivers
   - Fields: Name, Color, Password
   - Shows "Add New Driver" or "Edit Driver" based on context
   - Password field optional when editing (only updates if provided)

2. **Settings View (`frontend/src/views/SettingsView.vue`)**
   - Redesigned driver management section
   - Each driver displayed on its own row
   - Edit/Delete buttons visible when admin is authenticated
   - "Add New Driver" button opens modal form
   - Empty state when no drivers exist

3. **Store (`frontend/src/stores/app.js`)**
   - Updated `addUser` to accept password parameter

## Security Features
- **Password Hashing**: All passwords are hashed using bcrypt (with SHA-256 pre-hashing)
- **Never Plain Text**: Passwords are NEVER stored in plain text in the database
- **Admin Protected**: Edit and delete operations require admin authentication
- **Soft Delete**: Drivers are soft-deleted (is_active=false) to maintain data integrity

## UI Features
- Clean row-based layout for drivers
- Color-coded driver identification
- Modal forms for add/edit operations
- Admin-only edit/delete buttons
- Success/error message feedback
- Confirmation dialog for delete operations

## Testing
All features tested and verified:
- ✅ Driver creation with password hashing
- ✅ Password stored as bcrypt hash, not plain text
- ✅ Driver editing (name, color, password)
- ✅ Driver deletion (soft delete)
- ✅ Admin authentication for edit/delete
- ✅ UI displays correctly with multiple drivers
- ✅ Modal forms work properly
- ✅ Success/error messages display

## Branch
`feature/secure-driver-management`

## Database Migration
Note: The database schema changed. Existing databases need to be migrated or recreated.
