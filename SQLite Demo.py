import sqlite3
from datetime import datetime
import json

class SampleTracker:
    """Database-backed sample tracking system"""
    
    def __init__(self, db_path='lab_samples.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Initialize database schema"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS samples (
                sample_id TEXT PRIMARY KEY,
                sample_type TEXT,
                created_date TEXT,
                current_location TEXT,
                status TEXT,
                metadata TEXT
            )
        ''')
        

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id TEXT,
                timestamp TEXT,
                from_location TEXT,
                to_location TEXT,
                robot_id TEXT,
                FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
            )
        ''')
        

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id TEXT,
                timestamp TEXT,
                assay_type TEXT,
                result_value REAL,
                units TEXT,
                instrument TEXT,
                FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
            )
        ''')
        
        self.conn.commit()
        print("✅ Database tables created")
    
    def register_sample(self, sample_id, sample_type, location, metadata=None):
        """Register a new sample in the system"""
        cursor = self.conn.cursor()
        
        timestamp = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute('''
            INSERT INTO samples (sample_id, sample_type, created_date, 
                               current_location, status, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sample_id, sample_type, timestamp, location, 'registered', metadata_json))
        
        self.conn.commit()
        print(f"✅ Sample {sample_id} registered at {location}")
    
    def move_sample(self, sample_id, from_location, to_location, robot_id):
        """Record sample movement"""
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        

        cursor.execute('''
            INSERT INTO movements (sample_id, timestamp, from_location, 
                                 to_location, robot_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (sample_id, timestamp, from_location, to_location, robot_id))
        

        cursor.execute('''
            UPDATE samples 
            SET current_location = ?, status = 'in_transit'
            WHERE sample_id = ?
        ''', (to_location, sample_id))
        
        self.conn.commit()
        print(f"📦 {sample_id}: {from_location} → {to_location}")
    
    def record_result(self, sample_id, assay_type, value, units, instrument):
        """Record an analysis result"""
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO results (sample_id, timestamp, assay_type, 
                               result_value, units, instrument)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sample_id, timestamp, assay_type, value, units, instrument))
        

        cursor.execute('''
            UPDATE samples 
            SET status = 'analyzed'
            WHERE sample_id = ?
        ''', (sample_id,))
        
        self.conn.commit()
        print(f"📊 Result recorded: {sample_id} - {assay_type}: {value} {units}")
    
    def get_sample_history(self, sample_id):
        """Get complete history of a sample"""
        cursor = self.conn.cursor()
        
   
        cursor.execute('SELECT * FROM samples WHERE sample_id = ?', (sample_id,))
        sample = cursor.fetchone()
        
        if not sample:
            print(f"❌ Sample {sample_id} not found")
            return None
        

        cursor.execute('''
            SELECT timestamp, from_location, to_location, robot_id
            FROM movements
            WHERE sample_id = ?
            ORDER BY timestamp
        ''', (sample_id,))
        movements = cursor.fetchall()
        
 
        cursor.execute('''
            SELECT timestamp, assay_type, result_value, units, instrument
            FROM results
            WHERE sample_id = ?
            ORDER BY timestamp
        ''', (sample_id,))
        results = cursor.fetchall()
        
        return {
            'sample_info': sample,
            'movements': movements,
            'results': results
        }
    
    def print_sample_history(self, sample_id):
        """Print formatted sample history"""
        history = self.get_sample_history(sample_id)
        
        if not history:
            return
        
        print("\n" + "=" * 70)
        print(f"SAMPLE HISTORY: {sample_id}")
        print("=" * 70)
        

        sample = history['sample_info']
        print(f"\nType: {sample[1]}")
        print(f"Created: {sample[2]}")
        print(f"Current Location: {sample[3]}")
        print(f"Status: {sample[4]}")
        

        if history['movements']:
            print(f"\n📦 MOVEMENT HISTORY:")
            print(f"{'Time':<20} {'From':<20} {'To':<20} {'Robot':<15}")
            print("-" * 70)
            for m in history['movements']:
                timestamp = m[0][:19]  
                print(f"{timestamp:<20} {m[1]:<20} {m[2]:<20} {m[3]:<15}")
        

        if history['results']:
            print(f"\n📊 ANALYSIS RESULTS:")
            print(f"{'Time':<20} {'Assay':<20} {'Value':<15} {'Instrument':<15}")
            print("-" * 70)
            for r in history['results']:
                timestamp = r[0][:19]
                value_str = f"{r[2]:.2f} {r[3]}"
                print(f"{timestamp:<20} {r[1]:<20} {value_str:<15} {r[4]:<15}")
        
        print("=" * 70)
    
    def get_samples_at_location(self, location):
        """Find all samples at a given location"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT sample_id, sample_type, status
            FROM samples
            WHERE current_location = ?
        ''', (location,))
        
        samples = cursor.fetchall()
        return samples
    
    def get_all_samples_summary(self):
        """Get summary of all samples"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT sample_id, sample_type, current_location, status
            FROM samples
        ''')
        
        samples = cursor.fetchall()
        
        print("\n" + "=" * 70)
        print("ALL SAMPLES SUMMARY")
        print("=" * 70)
        print(f"{'Sample ID':<20} {'Type':<15} {'Location':<20} {'Status':<15}")
        print("-" * 70)
        
        for s in samples:
            print(f"{s[0]:<20} {s[1]:<15} {s[2]:<20} {s[3]:<15}")
        
        print("=" * 70)
    
    def close(self):
        """Close database connection"""
        self.conn.close()


def demo_workflow():
    """Demonstrate sample tracking in action"""
    
    print("\n" + "=" * 70)
    print("🧪 SAMPLE TRACKING SYSTEM DEMO")
    print("=" * 70)
    

    tracker = SampleTracker('demo_lab.db')
    

    print("\n📋 REGISTERING SAMPLES...")
    tracker.register_sample(
        'PLATE_001', 
        'cell_culture', 
        'Storage_A1',
        metadata={'clone_id': 'CHO_042', 'passage': 5}
    )
    
    tracker.register_sample(
        'PLATE_002', 
        'cell_culture', 
        'Storage_A2',
        metadata={'clone_id': 'CHO_018', 'passage': 5}
    )
    
    print("\n🤖 AUTOMATED WORKFLOW...")
    

    tracker.move_sample('PLATE_001', 'Storage_A1', 'LiquidHandler_1', 'Robot_ARM1')
    
  
    tracker.record_result('PLATE_001', 'cell_count', 3.2e6, 'cells/mL', 'Vi-CELL')
    tracker.record_result('PLATE_001', 'viability', 94.5, 'percent', 'Vi-CELL')
    
 
    tracker.move_sample('PLATE_001', 'LiquidHandler_1', 'Incubator_37C', 'Robot_ARM1')
    
   
    tracker.move_sample('PLATE_001', 'Incubator_37C', 'PlateReader_1', 'Robot_ARM1')
    

    tracker.record_result('PLATE_001', 'titer_ELISA', 3.8, 'g/L', 'PlateReader_1')
    

    tracker.move_sample('PLATE_001', 'PlateReader_1', 'Storage_A1', 'Robot_ARM1')
    

    tracker.print_sample_history('PLATE_001')
    

    tracker.get_all_samples_summary()
    

    print("\n📍 Samples at Storage:")
    samples_in_storage = tracker.get_samples_at_location('Storage_A1')
    for s in samples_in_storage:
        print(f"  {s[0]} - {s[1]} - {s[2]}")
    
    tracker.close()
    
    print("\n" + "=" * 70)
    print("🎓 KEY CONCEPTS DEMONSTRATED:")
    print("=" * 70)
    print("✅ Database creation and schema design")
    print("✅ Sample registration and tracking")
    print("✅ Movement history logging")
    print("✅ Results recording")
    print("✅ Query capabilities (by ID, by location)")
    print("✅ Complete audit trail (GMP requirement!)")
    print("\n💡 This is how real LIMS systems work!")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    demo_workflow()