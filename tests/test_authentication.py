import pytest
import json
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

class MockCredentials:
    """Mock Google OAuth2 Credentials for testing."""
    def __init__(self, token='mock_token', refresh_token='mock_refresh_token', 
                 token_expiry=None, client_id='mock_client_id'):
        self.token = token
        self.refresh_token = refresh_token
        self.token_expiry = token_expiry or datetime.utcnow() + timedelta(hours=1)
        self.client_id = client_id

    def to_json(self):
        """Convert credentials to JSON for testing."""
        return json.dumps({
            'token': self.token,
            'refresh_token': self.refresh_token,
            'token_expiry': self.token_expiry.isoformat(),
            'client_id': self.client_id
        })

class TestAuthentication:
    @pytest.fixture
    def mock_credentials_path(self, tmp_path):
        """Create a temporary credentials file for testing."""
        cred_file = tmp_path / 'credentials.json'
        mock_creds = MockCredentials()
        cred_file.write_text(mock_creds.to_json())
        return str(cred_file)

    def test_credentials_file_creation(self, mock_credentials_path):
        """Test that credentials file can be created and read."""
        assert os.path.exists(mock_credentials_path)
        with open(mock_credentials_path, 'r') as f:
            creds_data = json.load(f)
        
        assert 'token' in creds_data
        assert 'refresh_token' in creds_data
        assert 'token_expiry' in creds_data
        assert 'client_id' in creds_data

    def test_token_expiration(self, mock_credentials_path):
        """Test token expiration handling."""
        with open(mock_credentials_path, 'r') as f:
            creds_data = json.load(f)
        
        expiry = datetime.fromisoformat(creds_data['token_expiry'])
        assert expiry > datetime.utcnow()

    @patch('google.oauth2.credentials.Credentials')
    def test_credentials_refresh(self, mock_credentials_class):
        """Test credentials refresh mechanism."""
        # Create a mock credentials object that is expired
        expired_time = datetime.utcnow() - timedelta(hours=1)
        mock_creds = MockCredentials(token_expiry=expired_time)
        
        # Mock the refresh method
        mock_refresh = Mock()
        mock_credentials_class.from_authorized_user_file.return_value = mock_creds
        mock_credentials_class.return_value.refresh = mock_refresh
        
        # Simulate credentials refresh
        mock_refresh.assert_not_called()

    def test_invalid_credentials(self):
        """Test handling of invalid credentials."""
        with pytest.raises(ValueError):
            invalid_creds = MockCredentials(token=None, refresh_token=None)
            json.loads(invalid_creds.to_json())

    def test_client_credentials_validation(self, mock_credentials_path):
        """Validate client credentials structure."""
        client_id_path = '.auth/client_id.json'
        assert os.path.exists(client_id_path), "Client ID file must exist"
        
        with open(client_id_path, 'r') as f:
            client_data = json.load(f)
        
        assert 'client_id' in client_data, "Client ID must be present"
        assert 'client_secret' in client_data, "Client secret must be present"
        assert len(client_data['client_id']) > 0, "Client ID cannot be empty"
        assert len(client_data['client_secret']) > 0, "Client secret cannot be empty"