"""
Test suite for the Spool-Coder application
"""
import unittest
import sys

try:
    # Try to import model tests
    from tests.unit.test_filament_model import TestFilamentSpool
    filament_model_available = True
except ImportError:
    filament_model_available = False
    print("Skipping FilamentSpool tests - module not available", file=sys.stderr)

try:
    # Try to import service tests
    from tests.unit.test_nfc_device import TestNFCDevice
    nfc_device_available = True
except ImportError:
    nfc_device_available = False
    print("Skipping NFCDevice tests - module not available", file=sys.stderr)

try:
    # Try to import UI tests
    from tests.unit.test_main_window import TestMainWindow
    main_window_available = True
except ImportError:
    main_window_available = False
    print("Skipping MainWindow tests - module not available", file=sys.stderr)

try:
    from tests.unit.test_filament_detail_widget import TestFilamentDetailWidget
    filament_detail_widget_available = True
except ImportError:
    filament_detail_widget_available = False
    print("Skipping FilamentDetailWidget tests - module not available", file=sys.stderr)

try:
    from tests.unit.test_read_view import TestReadView
    read_view_available = True
except ImportError:
    read_view_available = False
    print("Skipping ReadView tests - module not available", file=sys.stderr)

try:
    from tests.unit.test_write_view import TestWriteView
    write_view_available = True
except ImportError:
    write_view_available = False
    print("Skipping WriteView tests - module not available", file=sys.stderr)


def create_test_suite():
    """Create a test suite with all tests"""
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add model tests
    if filament_model_available:
        test_suite.addTest(loader.loadTestsFromTestCase(TestFilamentSpool))
    
    # Add service tests
    if nfc_device_available:
        test_suite.addTest(loader.loadTestsFromTestCase(TestNFCDevice))
    
    # Add UI component tests
    if filament_detail_widget_available:
        test_suite.addTest(loader.loadTestsFromTestCase(TestFilamentDetailWidget))
    
    # Add UI view tests
    if main_window_available:
        test_suite.addTest(loader.loadTestsFromTestCase(TestMainWindow))
        
    if read_view_available:
        test_suite.addTest(loader.loadTestsFromTestCase(TestReadView))
        
    if write_view_available:
        test_suite.addTest(loader.loadTestsFromTestCase(TestWriteView))
    
    return test_suite

if __name__ == "__main__":
    # Create test suite
    suite = create_test_suite()
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
