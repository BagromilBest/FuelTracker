# Secure Driver Management Feature

## Summary
Added secure password management for drivers with a redesigned UI for managing driver accounts. Supports username reuse after deletion.

## Changes Made

### Backend Changes
1. **Models (`backend/app/models.py`)**
   - Added `password_hash` field to User model (NOT plain text)
   - Uses bcrypt hashing with SHA-256 pre-hashing for security
   - Removed UNIQUE constraint on `name` field to allow username reuse

2. **Schemas (`backend/app/schemas.py`)**
   - Added `password` field to `UserCreate` schema
   - Added new `UserUpdate` schema for updating drivers

3. **API Endpoints (`backend/app/main.py`)**
   - Updated `POST /api/users` to hash passwords before storing
   - Modified user creation to check only for active users with same name
   - Added `PUT /api/admin/users/{user_id}` for editing drivers (admin only)
   - Modified user update to check only for active users when validating name
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
- **Username Reuse**: Deleted usernames can be reused (new driver with same name can be created)
- **Active Username Protection**: Cannot create duplicate active usernames

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
- ✅ Username reuse after deletion works
- ✅ Cannot create duplicate active usernames (400 error)
- ✅ Database shows inactive and active users correctly

## Branch
`feature/secure-driver-management`

## Database Migration
Note: The database schema changed. Existing databases need to be migrated or recreated.
Changes:
- Added `password_hash` column to `users` table
- Removed UNIQUE constraint on `name` column
