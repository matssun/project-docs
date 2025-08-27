# Visma eAccounting API - Swagger Documentation

*Scraped from: https://eaccountingapi.vismaonline.com/swagger/ui/index*

## Key API Endpoints

### Account Management
- **GET** `/v2/accountbalances/{date}` - Get Account balance on a specific date (yyyy-MM-dd)
- **GET** `/v2/accounts` - Get a list of accounts
- **POST** `/v2/accounts` - Add an account
- **GET** `/v2/accounts/standardaccounts` - Get predefined standard accounts
- **GET** `/v2/accounts/{fiscalyearId}` - Get accounts for a given fiscal year
- **GET** `/v2/accounts/{fiscalyearId}/{accountNumber}` - Get account by number from fiscal year
- **PUT** `/v2/accounts/{fiscalyearId}/{accountNumber}` - Replace account in fiscal year
- **GET** `/v2/accountTypes` - Get default account types

### Bank Operations
- **GET** `/v2/bankaccounts` - Get list of bank accounts
- **POST** `/v2/bankaccounts` - Create a bank account
- **GET** `/v2/bankaccounts/{bankAccountId}` - Get specific bank account
- **PUT** `/v2/bankaccounts/{bankAccountId}` - Replace a bank account
- **DELETE** `/v2/bankaccounts/{bankAccountId}` - Delete a bank account
- **GET** `/v2/banktransactions/{bankAccountId}/matched` - Get matched bank transactions
- **GET** `/v2/banktransactions/{bankAccountId}/unmatched` - Get unmatched bank transactions
- **GET** `/v2/banktransactions/{bankAccountId}/{bankTransactionId}` - Get specific bank transaction
- **GET** `/v2/banks` - Get available banks in eAccounting

### Allocation Periods
- **GET** `/v2/allocationperiods` - Get allocation periods
- **POST** `/v2/allocationperiods` - Add allocation periods for voucher or supplier invoice
- **GET** `/v2/allocationperiods/{allocationPeriodId}` - Get single allocation period

### Approvals
- **PUT** `/v2/approval/vatreport/{id}` - Replace approval status of VAT report
- **PUT** `/v2/approval/supplierinvoice/{id}` - Replace approval status of invoice draft

### Company Settings
- **GET** `/v2/companysettings` - Get company settings
- **PUT** `/v2/companysettings` - Replace company settings
- **PUT** `/v2/companysettings/accountinglocksettings` - Update accounting lock interval settings

### App Store
- **GET** `/v2/appstore/status` - Get app store activation status

## Notes

- This is a partial extraction due to the large size of the Swagger documentation
- The API appears to be RESTful with standard HTTP methods
- Most endpoints follow the pattern `/v2/{resource}` or `/v2/{resource}/{id}`
- Date formats appear to use yyyy-MM-dd format
- The API supports CRUD operations for most resources

For complete documentation, visit: https://eaccountingapi.vismaonline.com/swagger/ui/index