#!/usr/bin/env python
"""
Test script to verify Alembic migrations work correctly.

This script tests:
1. Migration upgrade (creating tables)
2. Migration downgrade (dropping tables)
3. Migration upgrade again (recreating tables)
4. Database schema integrity
"""

import os
import sqlite3
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def get_tables(db_path):
    """Get list of tables in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'alembic_version'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


def get_schema(db_path, table_name):
    """Get schema for a specific table."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    conn.close()
    return columns


def test_migrations():
    """Test Alembic migrations."""
    backend_dir = Path(__file__).parent
    db_path = backend_dir / "biotecpredict.db"
    
    print("=" * 80)
    print("ALEMBIC MIGRATION TEST")
    print("=" * 80)
    
    # Test 1: Upgrade to head
    print("\n[TEST 1] Running migration upgrade to head...")
    returncode, stdout, stderr = run_command(
        "python -m alembic upgrade head",
        cwd=str(backend_dir)
    )
    
    if returncode != 0:
        print(f"❌ FAILED: {stderr}")
        return False
    
    print("✅ PASSED: Migration upgrade successful")
    
    # Verify tables exist
    tables = get_tables(str(db_path))
    expected_tables = {'batches', 'sensor_readings', 'predictions'}
    
    if not expected_tables.issubset(set(tables)):
        print(f"❌ FAILED: Expected tables {expected_tables}, got {set(tables)}")
        return False
    
    print(f"✅ PASSED: All expected tables created: {expected_tables}")
    
    # Test 2: Verify schema
    print("\n[TEST 2] Verifying database schema...")
    
    # Check batches table
    batches_schema = get_schema(str(db_path), 'batches')
    batches_columns = {col[1] for col in batches_schema}
    expected_batches_columns = {'id', 'upload_date', 'status', 'compliance_score', 'risk_prediction'}
    
    if not expected_batches_columns.issubset(batches_columns):
        print(f"❌ FAILED: Batches table missing columns. Expected {expected_batches_columns}, got {batches_columns}")
        return False
    
    print("✅ PASSED: Batches table schema correct")
    
    # Check sensor_readings table
    sensor_schema = get_schema(str(db_path), 'sensor_readings')
    sensor_columns = {col[1] for col in sensor_schema}
    expected_sensor_columns = {'id', 'batch_id', 'temperature', 'ph', 'dissolved_oxygen', 'pressure', 'agitator_speed', 'timestamp'}
    
    if not expected_sensor_columns.issubset(sensor_columns):
        print(f"❌ FAILED: SensorReading table missing columns. Expected {expected_sensor_columns}, got {sensor_columns}")
        return False
    
    print("✅ PASSED: SensorReading table schema correct")
    
    # Check predictions table
    pred_schema = get_schema(str(db_path), 'predictions')
    pred_columns = {col[1] for col in pred_schema}
    expected_pred_columns = {'id', 'batch_id', 'model_version', 'prediction_timestamp', 'confidence_score', 'risk_level'}
    
    if not expected_pred_columns.issubset(pred_columns):
        print(f"❌ FAILED: Predictions table missing columns. Expected {expected_pred_columns}, got {pred_columns}")
        return False
    
    print("✅ PASSED: Predictions table schema correct")
    
    # Test 3: Downgrade to base
    print("\n[TEST 3] Running migration downgrade to base...")
    returncode, stdout, stderr = run_command(
        "python -m alembic downgrade base",
        cwd=str(backend_dir)
    )
    
    if returncode != 0:
        print(f"❌ FAILED: {stderr}")
        return False
    
    print("✅ PASSED: Migration downgrade successful")
    
    # Verify tables are dropped
    tables = get_tables(str(db_path))
    
    if len(tables) > 0:
        print(f"❌ FAILED: Expected no tables after downgrade, got {tables}")
        return False
    
    print("✅ PASSED: All tables dropped after downgrade")
    
    # Test 4: Upgrade again
    print("\n[TEST 4] Running migration upgrade again...")
    returncode, stdout, stderr = run_command(
        "python -m alembic upgrade head",
        cwd=str(backend_dir)
    )
    
    if returncode != 0:
        print(f"❌ FAILED: {stderr}")
        return False
    
    print("✅ PASSED: Migration upgrade successful (second time)")
    
    # Verify tables exist again
    tables = get_tables(str(db_path))
    
    if not expected_tables.issubset(set(tables)):
        print(f"❌ FAILED: Expected tables {expected_tables}, got {set(tables)}")
        return False
    
    print(f"✅ PASSED: All expected tables recreated: {expected_tables}")
    
    # Test 5: Check migration history
    print("\n[TEST 5] Checking migration history...")
    returncode, stdout, stderr = run_command(
        "python -m alembic history",
        cwd=str(backend_dir)
    )
    
    if returncode != 0:
        print(f"❌ FAILED: {stderr}")
        return False
    
    print("✅ PASSED: Migration history retrieved")
    print(f"Migration history:\n{stdout}")
    
    # Test 6: Check current revision
    print("\n[TEST 6] Checking current revision...")
    returncode, stdout, stderr = run_command(
        "python -m alembic current",
        cwd=str(backend_dir)
    )
    
    if returncode != 0:
        print(f"❌ FAILED: {stderr}")
        return False
    
    print("✅ PASSED: Current revision retrieved")
    print(f"Current revision: {stdout.strip()}")
    
    print("\n" + "=" * 80)
    print("ALL TESTS PASSED! ✅")
    print("=" * 80)
    
    return True


if __name__ == '__main__':
    success = test_migrations()
    sys.exit(0 if success else 1)
