import json
import os
import random
from datetime import datetime
from typing import Dict, List, Optional

class DataManager:
    def __init__(self, data_dir="data"):
        """Initialize the data manager with a data directory."""
        self.data_dir = data_dir
        self.ensure_data_directory()
        
        # File paths for different data types
        self.users_file = os.path.join(data_dir, "users.json")
        self.members_file = os.path.join(data_dir, "members.json")
        self.providers_file = os.path.join(data_dir, "providers.json")
        self.service_claims_file = os.path.join(data_dir, "service_claims.json")
        self.service_directory_file = os.path.join(data_dir, "service_directory.json")
        
        # Initialize data structures
        self.users = self.load_users()
        self.members = self.load_members()
        self.providers = self.load_providers()
        self.service_claims = self.load_service_claims()
        self.service_directory = self.load_service_directory()
        
        # Initialize with default data if files don't exist
        self.initialize_default_data()
    
    def ensure_data_directory(self):
        """Create the data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def generate_provider_id(self) -> str:
        """Generate a unique 9-digit provider ID."""
        while True:
            provider_id = str(random.randint(100000000, 999999999))
            # Check if this ID already exists
            if not any(p.get('provider_id') == provider_id for p in self.providers):
                return provider_id
    
    def generate_member_id(self) -> str:
        """Generate a unique 9-digit member ID."""
        while True:
            member_id = str(random.randint(100000000, 999999999))
            # Check if this ID already exists
            if not any(m.get('member_id') == member_id for m in self.members):
                return member_id
    
    def generate_claim_id(self) -> str:
        """Generate a unique claim ID."""
        return str(1000000 + len(self.service_claims) + 1)
    
    def initialize_default_data(self):
        """Initialize with default data if the system is empty."""
        # Initialize default users if none exist
        if not self.users:
            self.users = {
                'manager': {'username': 'manager', 'password': 'manager123', 'role': 'manager'},
                'provider': {'username': 'quinn', 'password': 'quinn123', 'role': 'provider'},
                'mjin': {'username': 'Mjin', 'password': 'Mjin123', 'role': 'manager'}
            }
            self.save_users()
        
        # Initialize default members if none exist
        if not self.members:
            self.members = [
                {'member_id': '123456789', 'name': 'John Doe', 'status': 'Valid', 'address': '123 Main St', 'city': 'Anytown', 'state': 'CA', 'zip': '12345'},
                {'member_id': '543210987', 'name': 'Jane Smith', 'status': 'Expired', 'address': '456 Elm St', 'city': 'Othertown', 'state': 'NY', 'zip': '67890'},
                {'member_id': '333333333', 'name': 'Bob Johnson', 'status': 'Valid', 'address': '789 Oak St', 'city': 'Smalltown', 'state': 'TX', 'zip': '34567'},
            ]
            self.save_members()
        
        # Initialize default service directory if none exists
        if not self.service_directory:
            self.service_directory = [
                {'code': '100001', 'name': 'Therapy Session', 'fee': 100.00},
                {'code': '100002', 'name': 'Dental Cleaning', 'fee': 80.00},
                {'code': '100003', 'name': 'Vision Exam', 'fee': 60.00},
                {'code': '100004', 'name': 'Physical Therapy', 'fee': 120.00},
                {'code': '100005', 'name': 'Nutrition Counseling', 'fee': 75.00},
                {'code': '100006', 'name': 'Psychological Therapy', 'fee': 150.00},
                {'code': '100007', 'name': 'Occupational Therapy', 'fee': 110.00},
                {'code': '100008', 'name': 'Speech Therapy', 'fee': 95.00},
                {'code': '100009', 'name': 'Massage Therapy', 'fee': 85.00},
                {'code': '100010', 'name': 'Chiropractic Adjustment', 'fee': 90.00},
                {'code': '100011', 'name': 'Acupuncture Session', 'fee': 70.00},
                {'code': '100012', 'name': 'Dental X-Ray', 'fee': 45.00},
                {'code': '100013', 'name': 'Eye Glasses Fitting', 'fee': 55.00},
                {'code': '100014', 'name': 'Hearing Test', 'fee': 65.00},
                {'code': '100015', 'name': 'Blood Pressure Check', 'fee': 25.00},
                {'code': '100016', 'name': 'Diabetes Screening', 'fee': 40.00},
                {'code': '100017', 'name': 'Flu Shot', 'fee': 30.00},
                {'code': '100018', 'name': 'Smoking Cessation Program', 'fee': 200.00},
                {'code': '100019', 'name': 'Weight Loss Consultation', 'fee': 85.00},
                {'code': '100020', 'name': 'Stress Management Session', 'fee': 95.00},
            ]
            self.save_service_directory()
    
    # User management methods
    def load_users(self) -> Dict:
        """Load users from JSON file."""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return {}
    
    def save_users(self):
        """Save users to JSON file."""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def add_user(self, username: str, password: str, role: str) -> bool:
        """Add a new user."""
        if username in self.users:
            return False  # User already exists
        
        self.users[username] = {
            'username': username,
            'password': password,
            'role': role
        }
        self.save_users()
        return True
    
    def authenticate_user(self, username: str, password: str, role: str) -> bool:
        """Authenticate a user."""
        # Find user by username (case-sensitive)
        user = next((u for u in self.users.values() if u['username'] == username), None)
        if user and user['password'] == password and user['role'] == role:
            return True
        return False
    
    # Member management methods
    def load_members(self) -> List[Dict]:
        """Load members from JSON file."""
        try:
            if os.path.exists(self.members_file):
                with open(self.members_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return []
    
    def save_members(self):
        """Save members to JSON file."""
        with open(self.members_file, 'w') as f:
            json.dump(self.members, f, indent=2)
    
    def add_member(self, name: str, address: str, city: str, state: str, zip_code: str) -> str:
        """Add a new member and return the generated member ID."""
        member_id = self.generate_member_id()
        member = {
            'member_id': member_id,
            'name': name,
            'address': address,
            'city': city,
            'state': state.upper(),
            'zip': zip_code,
            'status': 'Valid'
        }
        self.members.append(member)
        self.save_members()
        return member_id
    
    def get_member(self, member_id: str) -> Optional[Dict]:
        """Get a member by ID."""
        return next((m for m in self.members if m['member_id'] == member_id), None)
    
    def update_member(self, member_id: str, **kwargs) -> bool:
        """Update member information."""
        member = self.get_member(member_id)
        if member:
            member.update(kwargs)
            self.save_members()
            return True
        return False
    
    def delete_member(self, member_id: str) -> bool:
        """Delete a member."""
        member = self.get_member(member_id)
        if member:
            self.members.remove(member)
            self.save_members()
            return True
        return False
    
    def renew_member(self, member_id: str) -> bool:
        """Renew an expired member."""
        member = self.get_member(member_id)
        if member and member['status'] == 'Expired':
            member['status'] = 'Valid'
            self.save_members()
            return True
        return False
    
    # Provider management methods
    def load_providers(self) -> List[Dict]:
        """Load providers from JSON file."""
        try:
            if os.path.exists(self.providers_file):
                with open(self.providers_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return []
    
    def save_providers(self):
        """Save providers to JSON file."""
        with open(self.providers_file, 'w') as f:
            json.dump(self.providers, f, indent=2)
    
    def add_provider(self, name: str, address: str, city: str, state: str, zip_code: str) -> str:
        """Add a new provider and return the generated provider ID."""
        provider_id = self.generate_provider_id()
        provider = {
            'provider_id': provider_id,
            'name': name,
            'address': address,
            'city': city,
            'state': state.upper(),
            'zip': zip_code
        }
        self.providers.append(provider)
        self.save_providers()
        
        # Create a user account for the provider
        username = name.lower().replace(' ', '')  # Create username from name
        password = f"{provider_id}"  # Use provider ID as initial password
        self.add_user(username, password, 'provider')
        
        return provider_id
    
    def get_provider(self, provider_id: str) -> Optional[Dict]:
        """Get a provider by ID."""
        return next((p for p in self.providers if p.get('provider_id') == provider_id), None)
    
    def get_provider_by_username(self, username: str) -> Optional[Dict]:
        """Get a provider by username."""
        # Find the user first
        user = next((u for u in self.users.values() if u['username'] == username), None)
        if user and user['role'] == 'provider':
            # Find the provider by name (assuming username is derived from name)
            provider_name = username.replace('', ' ').title()  # Convert username back to name
            return next((p for p in self.providers if p['name'].lower().replace(' ', '') == username), None)
        return None
    
    def update_provider(self, provider_id: str, **kwargs) -> bool:
        """Update provider information."""
        provider = self.get_provider(provider_id)
        if provider:
            provider.update(kwargs)
            self.save_providers()
            return True
        return False
    
    def delete_provider(self, provider_id: str) -> bool:
        """Delete a provider."""
        provider = self.get_provider(provider_id)
        if provider:
            self.providers.remove(provider)
            self.save_providers()
            return True
        return False
    
    # Service claims management methods
    def load_service_claims(self) -> List[Dict]:
        """Load service claims from JSON file."""
        try:
            if os.path.exists(self.service_claims_file):
                with open(self.service_claims_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return []
    
    def save_service_claims(self):
        """Save service claims to JSON file."""
        with open(self.service_claims_file, 'w') as f:
            json.dump(self.service_claims, f, indent=2)
    
    def add_service_claim(self, member_id: str, date_of_service: str, provider_number: str, 
                         service_code: str, comments: str = "") -> str:
        """Add a new service claim and return the claim ID."""
        # Get service information
        service = self.get_service(service_code)
        if not service:
            raise ValueError(f"Service code {service_code} not found")
        
        claim_id = self.generate_claim_id()
        current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        
        claim = {
            'Claim ID': claim_id,
            'Current Date/Time': current_datetime,
            'Date of Service': date_of_service,
            'Provider Number': provider_number,
            'Member ID': member_id,
            'Service Code': service_code,
            'Service Name': service['name'],
            'Fee': service['fee'],
            'Comments': comments,
            'Status': 'Pending'
        }
        
        self.service_claims.append(claim)
        self.save_service_claims()
        return claim_id
    
    # Service directory management methods
    def load_service_directory(self) -> List[Dict]:
        """Load service directory from JSON file."""
        try:
            if os.path.exists(self.service_directory_file):
                with open(self.service_directory_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return []
    
    def save_service_directory(self):
        """Save service directory to JSON file."""
        with open(self.service_directory_file, 'w') as f:
            json.dump(self.service_directory, f, indent=2)
    
    def get_service(self, service_code: str) -> Optional[Dict]:
        """Get a service by code."""
        return next((s for s in self.service_directory if s['code'] == service_code), None)
    
    def search_services(self, search_term: str) -> List[Dict]:
        """Search services by code or name."""
        search_term = search_term.lower()
        return [
            s for s in self.service_directory
            if search_term in s['code'].lower() or search_term in s['name'].lower()
        ]
    
    def add_service(self, code: str, name: str, fee: float) -> bool:
        """Add a new service to the directory."""
        if self.get_service(code):
            return False  # Service code already exists
        
        service = {
            'code': code,
            'name': name,
            'fee': fee
        }
        self.service_directory.append(service)
        self.save_service_directory()
        return True
    
    def update_service(self, code: str, **kwargs) -> bool:
        """Update service information."""
        service = self.get_service(code)
        if service:
            service.update(kwargs)
            self.save_service_directory()
            return True
        return False
    
    def delete_service(self, code: str) -> bool:
        """Delete a service from the directory."""
        service = self.get_service(code)
        if service:
            self.service_directory.remove(service)
            self.save_service_directory()
            return True
        return False
    
    # Utility methods
    def get_expired_members(self) -> List[Dict]:
        """Get all expired members."""
        return [m for m in self.members if m['status'] == 'Expired']
    
    def get_valid_members(self) -> List[Dict]:
        """Get all valid members."""
        return [m for m in self.members if m['status'] == 'Valid']
    
    def get_pending_claims(self) -> List[Dict]:
        """Get all pending service claims."""
        return [c for c in self.service_claims if c['Status'] == 'Pending']
    
    def get_approved_claims(self) -> List[Dict]:
        """Get all approved service claims."""
        return [c for c in self.service_claims if c['Status'] == 'Approved']
    
    def backup_data(self, backup_dir: str = "backup"):
        """Create a backup of all data files."""
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
        os.makedirs(backup_path)
        
        # Copy all data files
        files_to_backup = [
            self.users_file,
            self.members_file,
            self.providers_file,
            self.service_claims_file,
            self.service_directory_file
        ]
        
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                backup_file = os.path.join(backup_path, filename)
                with open(file_path, 'r') as src, open(backup_file, 'w') as dst:
                    dst.write(src.read())
        
        return backup_path 