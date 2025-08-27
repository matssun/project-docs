# Visma eAccounting API - Missing Endpoints Analysis

## Current Documented Endpoints

From our extraction, we have documented:
- Account Management (8 endpoints)
- Bank Operations (8 endpoints) 
- Allocation Periods (3 endpoints)
- Approvals (2 endpoints)
- Company Settings (3 endpoints)
- App Store (1 endpoint)

**Total: 25 endpoints**

## Likely Missing Endpoint Categories

Based on typical accounting API patterns and Visma eAccounting's described functionality:

### Customer Management
- GET `/v2/customers` - List customers
- POST `/v2/customers` - Create customer
- GET `/v2/customers/{id}` - Get specific customer
- PUT `/v2/customers/{id}` - Update customer
- DELETE `/v2/customers/{id}` - Delete customer

### Customer Invoices
- GET `/v2/customerinvoices` - List customer invoices
- POST `/v2/customerinvoices` - Create customer invoice
- GET `/v2/customerinvoices/{id}` - Get specific invoice
- PUT `/v2/customerinvoices/{id}` - Update invoice
- DELETE `/v2/customerinvoices/{id}` - Delete invoice
- POST `/v2/customerinvoices/{id}/send` - Send invoice

### Supplier Management
- GET `/v2/suppliers` - List suppliers
- POST `/v2/suppliers` - Create supplier
- GET `/v2/suppliers/{id}` - Get specific supplier
- PUT `/v2/suppliers/{id}` - Update supplier
- DELETE `/v2/suppliers/{id}` - Delete supplier

### Supplier Invoices
- GET `/v2/supplierinvoices` - List supplier invoices
- POST `/v2/supplierinvoices` - Create supplier invoice
- GET `/v2/supplierinvoices/{id}` - Get specific supplier invoice
- PUT `/v2/supplierinvoices/{id}` - Update supplier invoice
- DELETE `/v2/supplierinvoices/{id}` - Delete supplier invoice

### Products/Articles
- GET `/v2/articles` - List products/articles
- POST `/v2/articles` - Create article
- GET `/v2/articles/{id}` - Get specific article
- PUT `/v2/articles/{id}` - Update article
- DELETE `/v2/articles/{id}` - Delete article

### Vouchers/Journal Entries
- GET `/v2/vouchers` - List vouchers
- POST `/v2/vouchers` - Create voucher
- GET `/v2/vouchers/{id}` - Get specific voucher
- PUT `/v2/vouchers/{id}` - Update voucher
- DELETE `/v2/vouchers/{id}` - Delete voucher

### VAT/Tax
- GET `/v2/vatreports` - List VAT reports
- POST `/v2/vatreports` - Create VAT report
- GET `/v2/vatreports/{id}` - Get specific VAT report
- GET `/v2/vattypes` - List VAT types

### Financial Reports
- GET `/v2/reports/balancesheet` - Balance sheet
- GET `/v2/reports/incomestatement` - Income statement
- GET `/v2/reports/trialbalance` - Trial balance
- GET `/v2/reports/generalledger` - General ledger

### Fiscal Years
- GET `/v2/fiscalyears` - List fiscal years
- POST `/v2/fiscalyears` - Create fiscal year
- GET `/v2/fiscalyears/{id}` - Get specific fiscal year

### Projects/Cost Centers
- GET `/v2/projects` - List projects
- POST `/v2/projects` - Create project
- GET `/v2/projects/{id}` - Get specific project
- PUT `/v2/projects/{id}` - Update project

### Currencies
- GET `/v2/currencies` - List currencies
- GET `/v2/exchangerates` - Exchange rates

## Estimated Missing Endpoints: ~50-60

This would bring the total API to approximately 75-85 endpoints, which is typical for a comprehensive accounting API.

## Limitation

This analysis is based on common accounting API patterns and cannot provide an exact list without access to the complete Swagger specification.