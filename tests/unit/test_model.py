from iebank_api.models import Account
import pytest

def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    account = Account('John Doe', '€', 'Italy')
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.country == 'Italy'
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == 'Active'

def test_get_account_by_id(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is requested (GET)
    THEN check the response is valid
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Beatrice',
        'currency': '€',
        'country': 'France'
    })
    assert create_response.status_code == 200
    account_data = create_response.get_json()
    account_id = account_data['id']

    # Now, get the account by id
    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Beatrice'
    assert data['currency'] == '€'
    assert data['country'] == 'France'
    assert data['id'] == account_id

def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT)
    THEN check the response is valid
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Alvise',
        'currency': '£',
        'country': 'UK'
    })
    assert create_response.status_code == 200
    account_data = create_response.get_json()
    account_id = account_data['id']

    # Now, update the account
    update_response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'Marco'
    })
    assert update_response.status_code == 200
    updated_data = update_response.get_json()
    assert updated_data['name'] == 'Marco'
    assert updated_data['currency'] == '£'
    assert updated_data['country'] == 'Romania'
    assert updated_data['id'] == account_id

    # Verify that the account was updated
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 200
    get_data = get_response.get_json()
    assert get_data['name'] == 'Marco'

def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is deleted (DELETE)
    THEN check the response is valid and the account no longer exists
    """
    create_response = testing_client.post('/accounts', json={
        'name': 'Massimissimo',
        'currency': '$',
        'country': 'Sri Lanka'
    })
    assert create_response.status_code == 200, (
        f"Failed to create account. Status: {create_response.status_code}, "
        f"Response: {create_response.data.decode('utf-8')}"
    )
    account_data = create_response.get_json()
    assert account_data is not None, "Create response didn't return JSON data"
    assert 'id' in account_data, f"'id' not found in create response. Data: {account_data}"
    account_id = account_data['id']

    delete_response = testing_client.delete(f'/accounts/{account_id}')
    assert delete_response.status_code == 200, (
        f"Failed to delete account. Status: {delete_response.status_code}, "
        f"Response: {delete_response.data.decode('utf-8')}"
    )

    get_all_response = testing_client.get('/accounts')
    assert get_all_response.status_code == 200, (
        f"Failed to get all accounts. Status: {get_all_response.status_code}, "
        f"Response: {get_all_response.data.decode('utf-8')}"
    )

    accounts_data = get_all_response.get_json()
    assert accounts_data is not None, "Get all accounts response didn't return JSON data"
    account_ids = [account['id'] for account in accounts_data.get('accounts', [])]
    assert account_id not in account_ids, "Deleted account still present in accounts list"