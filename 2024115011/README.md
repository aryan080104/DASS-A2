# Software Testing Assignment - Roll Number: 2024115011

## Overview

This submission contains three comprehensive testing exercises for DASS Assignment 2:
1. White-box testing on MoneyPoly (board game)
2. Integration testing on StreetRace Manager (street racing system)
3. Black-box API testing on QuickCart REST API

## Directory Structure

```
2024115011/
├── whitebox/
│   ├── code/                    # MoneyPoly source code
│   ├── diagrams/                # Control Flow Graph (hand-drawn)
│   ├── tests/                   # White-box test cases
│   └── report.pdf               # White-box testing report
├── integration/
│   ├── code/                    # StreetRace Manager modules (6 core + 2 additional)
│   ├── diagrams/                # Call Graph (hand-drawn)
│   ├── tests/                   # Integration test cases
│   └── report.pdf               # Integration testing report
├── blackbox/
│   ├── tests/                   # QuickCart API test cases & bug reports
│   └── report.pdf               # Black-box testing report
└── README.md                    # This file
```

## How to Run Tests

### White-box Testing (MoneyPoly)
```bash
cd whitebox/tests
pytest test_whitebox_moneyopoly.py -v
```

### Integration Testing (StreetRace Manager)
```bash
cd integration/tests
pytest test_integration_streetrace.py -v
# Or run individual module tests:
pytest test_registration_module.py -v
pytest test_crew_management_module.py -v
pytest test_inventory_module.py -v
pytest test_race_management_module.py -v
pytest test_results_module.py -v
pytest test_mission_planning_module.py -v
pytest test_maintenance_module.py -v
pytest test_sponsorship_module.py -v
```

### Black-box API Testing (QuickCart)
```bash
cd blackbox/tests
# First, ensure QuickCart API is running on localhost:8080
pytest test_quickcart_api.py -v
```

## Project Contents

### 1. White-Box Testing (MoneyPoly)
- **Code Location**: `whitebox/code/`
- **Test Cases**: `whitebox/tests/test_whitebox_moneyopoly.py`
- **Diagrams**: Control Flow Graph in `whitebox/diagrams/`
- **Report**: `whitebox/report.pdf`

**Key Features**:
- All branches covered through test cases
- Edge cases tested (zero balance, maximum properties, negative amounts)
- Code quality analyzed and improved using pylint
- Logical errors identified and corrected
- CommitHistory: Changes committed as "Iteration #" and "Error #" formats

### 2. Integration Testing (StreetRace Manager)
- **Code Location**: `integration/code/`
- **Modules Included**:
  - Registration (register crew members)
  - Crew Management (manage roles and skills)
  - Inventory (track cars, parts, cash)
  - Race Management (create races and enter drivers)
  - Results (record outcomes and update rankings)
  - Mission Planning (assign missions with role validation)
  - **Additional Module 1**: Maintenance (repair cars and manage spare parts)
  - **Additional Module 2**: Sponsorship (manage sponsor contracts and payments)

- **Test Cases**: `integration/tests/`
- **Call Graph**: `integration/diagrams/` (hand-drawn image required)
- **Report**: `integration/report.pdf`

**Key Features**:
- Module interactions tested comprehensively
- Business rules validated (registration before role assignment, driver role for races, etc.)
- Data flow between modules verified
- Integration scenarios covered (driver registration → race entry → results → inventory update)
- Call graph showing all inter-module dependencies

### 3. Black-Box API Testing (QuickCart)
- **API Endpoints Tested**:
  - `/profile` - User profile management
  - `/addresses` - Address management
  - `/cart` - Shopping cart operations
  - `/wallet` - Wallet balance management
  - `/loyalty` - Loyalty points management
  - `/products/{id}/reviews` - Product reviews

- **Test Cases**: `blackbox/tests/test_quickcart_api.py` (60 test cases)
- **Test Coverage**:
  - Valid requests and expected responses
  - Invalid inputs and error handling
  - Boundary value testing
  - Data type validation
  - Missing fields handling

- **Bug Reports**: `blackbox/tests/QUICKCART_BUGS_FOUND.md`
- **Report**: `blackbox/report.pdf`

**Bugs Found**: 7 critical issues documented with:
- Endpoint URL and HTTP method
- Request payload (headers, body)
- Expected vs. actual results
- Steps to reproduce

## Git Repository

**Repository Link**: [GitHub Repository](https://github.com/aryan080104/DASS-A2)

All work has been committed to the Git repository with meaningful commit messages following the format:
- Whitebox: `Iteration #: <description>` and `Error #: <description>`
- Integration: Individual module commits plus integration testing commits
- Blackbox: API testing and bug discovery commits

## Testing Statistics

- **Whitebox**: All branches covered, edge cases validated
- **Integration**: 8 modules with 9 comprehensive integration tests (100% pass rate)
- **Blackbox**: 60 API test cases (47 passed, 13 failed), 7 bugs identified

## Requirements Met

✅ All code runs properly
✅ pytest used for all test cases
✅ Clear commit history maintained in Git
✅ Hand-drawn diagrams included (CFG, Call Graph)
✅ Comprehensive bug reports for API testing
✅ Proper folder structure matching assignment format
✅ README includes run instructions and Git repo link
✅ Report PDFs generated for each testing phase

## Notes on Hand-Drawn Components

- **Control Flow Graph**: Located in `whitebox/diagrams/` - A clear hand-drawn image showing program flow with labeled nodes and arrows
- **Call Graph**: Located in `integration/diagrams/` - A hand-drawn image showing function calls within and between modules

Clear photos of these hand-drawn diagrams are required to be included in the diagrams folders.
