# Sample Tracking Database System
**By: Oluwaseun Ajayi**  
**Date: December 17, 2025**

## Overview
Database-backed sample tracking system demonstrating LIMS (Laboratory Information Management System) concepts used in pharmaceutical laboratories.
I built it to understand how samples, metadata, and experimental status are managed to support traceability, data integrity, and reproducible analytical workflows.

## What It Does
Tracks samples as they move through an automated lab workflow:
- Registers new samples with unique IDs
- Records every movement between devices
- Stores analysis results (cell count, viability, titer)
- Maintains complete audit trail (required for GMP compliance)

## Features
✅ Sample registration with metadata  
✅ Movement tracking (who moved what, when, where)  
✅ Analysis results recording  
✅ Query capabilities (find samples by location or ID)  
✅ Complete history for every sample  
✅ GMP-compliant logging  

## Database Schema

### Tables
**samples** - Master list of all samples
- sample_id (unique identifier)
- sample_type (cell_culture, reagent, etc.)
- created_date (when registered)
- current_location (where it is now)
- status (registered, in_transit, analyzed)
- metadata (additional info as JSON)

**movements** - Every time a sample moves
- sample_id (which sample)
- timestamp (when it moved)
- from_location (starting location)
- to_location (ending location)
- robot_id (which robot moved it)

**results** - Analysis data
- sample_id (which sample)
- timestamp (when analyzed)
- assay_type (cell_count, titer, viability)
- result_value (the measurement)
- units (cells/mL, g/L, percent)
- instrument (which device measured it)

## Sample Output
```
SAMPLE HISTORY: PLATE_001
======================================================================
Type: cell_culture
Created: 2025-12-17
Current Location: Storage_A1
Status: analyzed

📦 MOVEMENT HISTORY:
Time                 From                 To                   Robot
----------------------------------------------------------------------
2025-12-17 17:07:02  Storage_A1           LiquidHandler_1      Robot_ARM1
2025-12-17 17:07:03  LiquidHandler_1      Incubator_37C        Robot_ARM1
2025-12-17 17:07:04  Incubator_37C        PlateReader_1        Robot_ARM1
2025-12-17 17:07:05  PlateReader_1        Storage_A1           Robot_ARM1

📊 ANALYSIS RESULTS:
Time                 Assay                Value           Instrument
----------------------------------------------------------------------
2025-12-17 17:07:02  cell_count           3200000.00 cells/mL Vi-CELL
2025-12-17 17:07:02  viability            94.50 percent   Vi-CELL
2025-12-17 17:07:04  titer_ELISA          3.80 g/L        PlateReader_1
```

## Technologies
- **Python 3.x**
- **SQLite3** - Lightweight database (no server needed)
- **JSON** - For flexible metadata storage

## How to Run
```bash
python "SQLite Demo.py"
```

The script will:
1. Create a database file (`demo_lab.db`)
2. Register sample plates
3. Simulate automated workflow (movements and analyses)
4. Display complete sample history
5. Show all samples summary

## Why This Matters

### Real-World Applications
In pharmaceutical labs:
- Every sample must be tracked (regulatory requirement)
- Complete audit trail for GMP compliance
- Can't rely on memory - need permanent records
- Must answer: "Where is sample X right now?"
- Must prove: "What happened to sample Y?"

### At J&J
This demonstrates understanding of:
- LIMS integration concepts
- Data persistence (survives program restarts)
- Relational database design
- Audit trail requirements
- Sample tracking workflows

The automation systems I'll work on must integrate with databases like this to maintain traceability.

## Key Concepts Demonstrated
✅ Database creation and schema design  
✅ CRUD operations (Create, Read, Update, Delete)  
✅ Relational data (linking tables with foreign keys)  
✅ Transaction management  
✅ Query optimization  
✅ Data integrity  
✅ Audit logging  

## Future Enhancements
- Web interface for querying samples
- Barcode integration for scanning
- Export to CSV/Excel for reporting
- Integration with robot control systems
- Real-time location tracking
- Alert system for sample expiration

---

*Part of my lab automation portfolio for J&J Cell Engineering co-op*  
*See also: API Automation System, Robot Workcell Simulator, Cell Line Screening Simulator*