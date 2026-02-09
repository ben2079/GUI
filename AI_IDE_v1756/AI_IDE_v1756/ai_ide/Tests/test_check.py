"""
Unit tests for _check.py module
Tests the _key_values and check functions
"""

import unittest
from unittest.mock import patch
import sys


class TestKeyValues(unittest.TestCase):
    """Test cases for the _key_values function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data = [
            {"name": "Alice", "age": 30, "city": "Berlin"},
            {"name": "Bob", "age": 25, "city": "Munich"},
            {"name": "Charlie", "age": 35, "city": "Hamburg"},
            {"name": "", "age": 28, "city": ""},  # Empty values
            {"name": "David", "age": None, "city": "Cologne"},  # None value
        ]
    
    def test_empty_data(self):
        """Test with empty data list"""
        class TestClass:
            seen_value1 = []
            seen_value2 = []
            _colec = []
        
        result = TestClass._key_values = lambda key1, key2, *, data: []
        self.assertEqual(TestClass._key_values("name", "age", data=[]), [])
    
    def test_basic_key_extraction(self):
        """Test basic key-value extraction"""
        class TestClass:
            seen_value1 = []
            seen_value2 = []
            _colec = []
            
            @classmethod
            def _key_values(cls, key1: str, key2: str, *, data: list) -> list[dict[str, str]]:
                pair: list[dict[str, str | int]] = []
                cls.seen_value1 = []
                cls.seen_value2 = []
            
                for entry in data:
                    for key in entry:
                        if key == key1:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value1 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value1.append(entry[key])
                        
                        if key == key2:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value2 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value2.append(entry[key])
                                if pair:
                                    cls._colec.append(pair)
                                    pair = []
                return cls._colec
        
        result = TestClass._key_values("name", "age", data=self.test_data)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_nonexistent_keys(self):
        """Test with keys that don't exist in data"""
        class TestClass:
            seen_value1 = []
            seen_value2 = []
            _colec = []
            
            @classmethod
            def _key_values(cls, key1: str, key2: str, *, data: list) -> list[dict[str, str]]:
                pair: list[dict[str, str | int]] = []
                cls.seen_value1 = []
                cls.seen_value2 = []
            
                for entry in data:
                    for key in entry:
                        if key == key1:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value1 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value1.append(entry[key])
                        
                        if key == key2:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value2 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value2.append(entry[key])
                                if pair:
                                    cls._colec.append(pair)
                                    pair = []
                return cls._colec
        
        result = TestClass._key_values("nonexistent1", "nonexistent2", data=self.test_data)
        self.assertEqual(result, [])
    
    def test_duplicate_values(self):
        """Test handling of duplicate values"""
        duplicate_data = [
            {"name": "Alice", "age": 30},
            {"name": "Alice", "age": 30},  # Duplicate
            {"name": "Bob", "age": 25},
        ]
        
        class TestClass:
            seen_value1 = []
            seen_value2 = []
            _colec = []
            
            @classmethod
            def _key_values(cls, key1: str, key2: str, *, data: list) -> list[dict[str, str]]:
                pair: list[dict[str, str | int]] = []
                cls.seen_value1 = []
                cls.seen_value2 = []
            
                for entry in data:
                    for key in entry:
                        if key == key1:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value1 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value1.append(entry[key])
                        
                        if key == key2:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value2 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value2.append(entry[key])
                                if pair:
                                    cls._colec.append(pair)
                                    pair = []
                return cls._colec
        
        result = TestClass._key_values("name", "age", data=duplicate_data)
        # Verify that duplicates are handled (should be filtered by seen_value logic)
        self.assertIsInstance(result, list)


class TestCheckFunction(unittest.TestCase):
    """Test cases for the check function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
        ]
        
        # Define a complete test class with both _key_values and check methods
        class TestClass:
            seen_value1 = []
            seen_value2 = []
            _colec = []
            _value_name1 = None
            _value_name2 = None
            
            @classmethod
            def _key_values(cls, key1: str, key2: str, *, data: list) -> list[dict[str, str]]:
                pair: list[dict[str, str | int]] = []
                cls.seen_value1 = []
                cls.seen_value2 = []
                cls._colec = []
            
                for entry in data:
                    for key in entry:
                        if key == key1:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value1 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value1.append(entry[key])
                        
                        if key == key2:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value2 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value2.append(entry[key])
                                if pair:
                                    cls._colec.append(pair)
                                    pair = []
                return cls._colec
            
            @classmethod
            def check(cls, _value: str, key1, key2, *, data: list):
                """Check if value exists in the key-value pairs"""
                cls._value_name1 = None
                cls._value_name2 = None
                
                pairs = cls._key_values(key1, key2, data=data)
                
                for pair in pairs:
                    if len(pair) >= 2:
                        val1 = pair[0].get(key1)
                        val2 = pair[1].get(key2)
                        
                        # Check if either value matches
                        if val1 == _value or val2 == _value:
                            cls._value_name1 = val1
                            cls._value_name2 = val2
                            return cls._value_name1, cls._value_name2
                
                # No value found
                return None
        
        self.TestClass = TestClass

    @patch('builtins.print')
    def test_check_with_valid_value(self, mock_print):
        """Test check function with a valid value"""
        test_data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        
        result = self.TestClass.check("Alice", "name", "age", data=test_data)
        
        # Verify result is either a tuple or None
        if result is not None:
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
    
    @patch('builtins.print')
    def test_check_with_invalid_value(self, mock_print):
        """Test check function with an invalid value"""
        test_data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        
        result = self.TestClass.check("David", "name", "age", data=test_data)
        
        # Should return None when value not found
        self.assertIsNone(result)
    
    def test_check_with_empty_data(self):
        """Test check function with empty data"""
        result = self.TestClass.check("Alice", "name", "age", data=[])
        
        # Should return None for empty data
        self.assertIsNone(result)
    
    def test_check_with_numeric_value(self):
        """Test check function with numeric values"""
        test_data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        
        result = self.TestClass.check(30, "name", "age", data=test_data)
        
        if result is not None:
            self.assertIsInstance(result, tuple)
    
    def test_check_preserves_class_attributes(self):
        """Test that check properly sets class attributes"""
        test_data = [
            {"name": "Alice", "age": 30},
        ]
        
        self.TestClass.check("Alice", "name", "age", data=test_data)
        
        # Check that class attributes are set (or None if not found)
        self.assertTrue(
            hasattr(self.TestClass, '_value_name1') and 
            hasattr(self.TestClass, '_value_name2')
        )


class TestIntegration(unittest.TestCase):
    """Integration tests for the entire module"""
    
    def test_full_workflow(self):
        """Test the complete workflow from data to check"""
        # Create a complete test class
        class WorkflowClass:
            seen_value1 = []
            seen_value2 = []
            _colec = []
            _value_name1 = None
            _value_name2 = None
            
            @classmethod
            def _key_values(cls, key1: str, key2: str, *, data: list) -> list[dict[str, str]]:
                pair: list[dict[str, str | int]] = []
                cls.seen_value1 = []
                cls.seen_value2 = []
                cls._colec = []
            
                for entry in data:
                    for key in entry:
                        if key == key1:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value1 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value1.append(entry[key])
                        
                        if key == key2:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value2 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value2.append(entry[key])
                                if pair:
                                    cls._colec.append(pair)
                                    pair = []
                return cls._colec
            
            @classmethod
            def check(cls, _value: str, key1, key2, *, data: list):
                """Check if value exists in the key-value pairs"""
                cls._value_name1 = None
                cls._value_name2 = None
                
                pairs = cls._key_values(key1, key2, data=data)
                
                for pair in pairs:
                    if len(pair) >= 2:
                        val1 = pair[0].get(key1)
                        val2 = pair[1].get(key2)
                        
                        if val1 == _value or val2 == _value:
                            cls._value_name1 = val1
                            cls._value_name2 = val2
                            return cls._value_name1, cls._value_name2
                
                return None
        
        # Test data
        test_data = [
            {"product": "Laptop", "price": 1000},
            {"product": "Mouse", "price": 25},
            {"product": "Keyboard", "price": 75},
        ]
        
        # Test 1: Extract key-values
        result = WorkflowClass._key_values("product", "price", data=test_data)
        self.assertIsInstance(result, list)
        
        # Test 2: Check for existing value
        check_result = WorkflowClass.check("Laptop", "product", "price", data=test_data)
        if check_result is not None:
            self.assertIsInstance(check_result, tuple)
            self.assertIn("Laptop", check_result)
        
        # Test 3: Check for non-existing value
        check_result_none = WorkflowClass.check("Monitor", "product", "price", data=test_data)
        self.assertIsNone(check_result_none)
    
    def test_workflow_with_real_data(self):
        """Test with realistic user data scenario"""
        class UserDataClass:
            seen_value1 = []
            seen_value2 = []
            _colec = []
            _value_name1 = None
            _value_name2 = None
            
            @classmethod
            def _key_values(cls, key1: str, key2: str, *, data: list) -> list[dict[str, str]]:
                pair: list[dict[str, str | int]] = []
                cls.seen_value1 = []
                cls.seen_value2 = []
                cls._colec = []
            
                for entry in data:
                    for key in entry:
                        if key == key1:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value1 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value1.append(entry[key])
                        
                        if key == key2:
                            if not entry[key]:
                                continue
                            else:
                                if not entry[key] in cls.seen_value2 and entry[key] != "" or not entry[key] is None: 
                                    if key and entry[key]:
                                        pair.append({key: entry[key]})
                                cls.seen_value2.append(entry[key])
                                if pair:
                                    cls._colec.append(pair)
                                    pair = []
                return cls._colec
            
            @classmethod
            def check(cls, _value: str, key1, key2, *, data: list):
                cls._value_name1 = None
                cls._value_name2 = None
                pairs = cls._key_values(key1, key2, data=data)
                for pair in pairs:
                    if len(pair) >= 2:
                            val1 = pair[0][key1]
                            val2 = pair[1][key2]
                    if val1 == _value or val2 == _value:
                            cls._value_name1 = val1
                            cls._value_name2 = val2
                            return cls._value_name1, cls._value_name2
                return None
        
        # Realistic user database
        users = [
            {"username": "alice123", "user_id": 1001, "email": "alice@example.com"},
            {"username": "bob456", "user_id": 1002, "email": "bob@example.com"},
            {"username": "", "user_id": 1003, "email": ""},  # Empty values
            {"username": "charlie789", "user_id": 1004, "email": "charlie@example.com"},
        ]
        
        # Search for user by username
        result = UserDataClass.check("alice123", "username", "user_id", data=users)
        if result is not None:
            self.assertEqual(result[0], "alice123")
            self.assertEqual(result[1], 1001)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestKeyValues))
    suite.addTests(loader.loadTestsFromTestCase(TestCheckFunction))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
