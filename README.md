# Chocoholics Anonymous Data Processing System

A comprehensive data management system for Chocoholics Anonymous, built with Python and PySide6 (Qt).

## Features

### User Management
- **Role-based Authentication**: Manager and Provider roles with secure login
- **User Management**: Add, modify, and manage user accounts

### Member Management
- **Member Registration**: Add new members with auto-generated 9-digit IDs
- **Member Verification**: Check member status (Valid/Expired)
- **Member Renewal**: Renew expired members
- **Member Modification**: Update member information
- **Member Removal**: Delete members from the system

### Provider Management
- **Provider Registration**: Add new providers with auto-generated 9-digit IDs
- **Provider Modification**: Update provider information
- **Provider Deletion**: Remove providers from the system

### Service Claims
- **Service Claim Submission**: Submit new service claims with validation
- **Service Code Verification**: Real-time service code lookup
- **Claim Tracking**: Track claim status and history

### Service Directory
- **Service Lookup**: Search services by code or name
- **Provider Directory**: Email service directory to providers
- **Service Management**: Add, modify, and delete services

## Data Management

### Persistent Storage
The system now uses a robust data management system that stores all data in JSON files:

- **`data/users.json`**: User accounts and authentication data
- **`data/members.json`**: Member information and status
- **`data/providers.json`**: Provider information
- **`data/service_claims.json`**: Service claim records
- **`data/service_directory.json`**: Service directory data

### Key Features
- **Automatic ID Generation**: 9-digit IDs for members and providers
- **Data Persistence**: All changes are automatically saved to files
- **Data Validation**: Comprehensive input validation and error handling
- **Backup System**: Built-in data backup functionality
- **Default Data**: System initializes with sample data if no files exist

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Required Files**:
   - `banner.png` - Chocolate-themed banner image
   - `choco.png` - Chocolate bar icon
   - `Pacifico-Regular.ttf` - Custom font file

3. **Run the Application**:
   ```bash
   python chocan_database.py
   ```

## Default Login Credentials

### Manager Accounts
- **Username**: `manager`, **Password**: `manager123`
- **Username**: `Mjin`, **Password**: `Mjin123`

### Provider Account
- **Username**: `quinn`, **Password**: `quinn123`

## Workflow

### Manager Workflow
1. **Login as Manager** using the default credentials
2. **Add Providers** through the "Manage Providers" menu
3. **View Provider Directory** to see all available services
4. **Generate Reports** (placeholder feature)

### Provider Workflow
1. **Login as Provider** using credentials provided by manager
2. **Add Members** through the "Manage Members" menu
3. **Verify Member Status** before providing services
4. **Submit Service Claims** for services provided
5. **Request Provider Directory** for service information

### New Provider Setup
When a manager adds a new provider:
- **Provider ID**: Auto-generated 9-digit number
- **Username**: Provider's name (lowercase, no spaces)
- **Password**: Provider ID (can be changed later)
- **Example**: Dr. Sarah Johnson → Username: `drsarahjohnson`, Password: `123456789`

## System Architecture

### DataManager Class
The `DataManager` class handles all data operations:

- **File Management**: Automatic creation and management of data files
- **ID Generation**: Unique ID generation for members and providers
- **CRUD Operations**: Create, Read, Update, Delete operations for all entities
- **Data Validation**: Input validation and error handling
- **Backup System**: Automatic backup creation

### Key Methods
- `add_member()` / `add_provider()`: Add new entities with auto-generated IDs
- `get_member()` / `get_provider()`: Retrieve entity information
- `update_member()` / `update_provider()`: Update entity information
- `delete_member()` / `delete_provider()`: Remove entities
- `authenticate_user()`: User authentication
- `add_service_claim()`: Submit new service claims
- `search_services()`: Search service directory

## Data Structure

### Member Data
```json
{
  "member_id": "123456789",
  "name": "Diana Vazquez",
  "status": "Valid",
  "address": "123 Main St",
  "city": "Anytown",
  "state": "CA",
  "zip": "12345"
}
```

### Provider Data
```json
{
  "provider_id": "987654321",
  "name": "Dr. Smith",
  "address": "456 Oak Ave",
  "city": "Somewhere",
  "state": "NY",
  "zip": "67890"
}
```

### Service Claim Data
```json
{
  "Claim ID": "1000001",
  "Current Date/Time": "12-01-2024 14:30:00",
  "Date of Service": "11-30-2024",
  "Provider Number": "987654321",
  "Member ID": "123456789",
  "Service Code": "100001",
  "Service Name": "Therapy Session",
  "Fee": 100.00,
  "Comments": "Initial session",
  "Status": "Pending"
}
```

## Error Handling

The system includes comprehensive error handling:
- **Input Validation**: All user inputs are validated
- **Data Integrity**: Ensures data consistency
- **User Feedback**: Clear error messages and success confirmations
- **Graceful Degradation**: System continues to function even with data errors

## Security Features

- **Password Protection**: Secure user authentication
- **Role-based Access**: Different permissions for managers and providers
- **Data Validation**: Prevents invalid data entry
- **Audit Trail**: Service claims include timestamps and user tracking

## Future Enhancements

- **Database Integration**: SQLite or PostgreSQL database support
- **Encryption**: Data encryption for sensitive information
- **Reporting**: Advanced reporting and analytics
- **API Integration**: REST API for external system integration
- **Multi-user Support**: Concurrent user access
- **Audit Logging**: Comprehensive audit trail

## Support

For technical support or questions about the system, please contact the development team.

---

**Note**: This is a prototype system for educational purposes. In a production environment, additional security measures and data validation would be implemented. 