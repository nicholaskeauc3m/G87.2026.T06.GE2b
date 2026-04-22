"""class for testing the register_document method"""
import os
import json
import unittest
from uc3m_consulting import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterDocument(unittest.TestCase):
    """Test cases for register_document - Syntactic Analysis"""

    def setUp(self):
        """Create test environment before each test"""
        self.manager = EnterpriseManager()
        self.test_json_path = "mytest.json"
        self.valid_project_id = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
        for f in ["mytest.json", "all_documents.json", "corporate_operations.json"]:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
        """Clean up files after each test"""
        for f in ["mytest.json", "all_documents.json", "corporate_operations.json"]:
            if os.path.exists(f):
                os.remove(f)

    def write_json(self, content):
        """Helper to write raw content to test json file"""
        with open(self.test_json_path, "w", encoding="utf-8") as f:
            f.write(content)

    def write_json_dict(self, data: dict):
        """Helper to write a dict to test json file"""
        with open(self.test_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def test_tc01_valid_input(self):
        """TC01 - Valid PROJECT_ID and FILENAME should return 64-char SHA-256 string"""
        self.write_json_dict({
            "PROJECT_ID": self.valid_project_id,
            "FILENAME": "abcd1234.pdf"
        })
        result = self.manager.register_document(self.test_json_path)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)

    def test_tc02_file_not_found(self):
        """TC02 - Non-existent file path should raise exception"""
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document("nonexistent.json")
        self.assertEqual(ctx.exception.message, "Input file not found")

    def test_tc03_file_not_valid_json(self):
        """TC03 - Plain text file should raise exception"""
        self.write_json("this is not json at all")
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "File is not valid JSON")

    def test_tc04_missing_keys(self):
        """TC04 - Empty JSON object should raise exception"""
        self.write_json_dict({})
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "JSON does not have expected structure")

    def test_tc05_missing_filename_key(self):
        """TC05 - JSON with only PROJECT_ID should raise exception"""
        self.write_json_dict({"PROJECT_ID": self.valid_project_id})
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "JSON does not have expected structure")

    def test_tc06_missing_project_id_key(self):
        """TC06 - JSON with only FILENAME should raise exception"""
        self.write_json_dict({"FILENAME": "abcd1234.pdf"})
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "JSON does not have expected structure")

    def test_tc07_extra_key(self):
        """TC07 - Extra unexpected key should raise exception"""
        self.write_json_dict({
            "PROJECT_ID": self.valid_project_id,
            "FILENAME": "abcd1234.pdf",
            "EXTRA": "data"
        })
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "JSON does not have expected structure")

    def test_tc08_invalid_project_id_wrong_length(self):
        """TC08 - PROJECT_ID with wrong length should raise exception"""
        self.write_json_dict({
            "PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d",
            "FILENAME": "abcd1234.pdf"
        })
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "Invalid PROJECT_ID")

    def test_tc09_invalid_project_id_non_hex(self):
        """TC09 - PROJECT_ID with non-hex character should raise exception"""
        self.write_json_dict({
            "PROJECT_ID": "G1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
            "FILENAME": "abcd1234.pdf"
        })
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "Invalid PROJECT_ID")

    def test_tc10_valid_docx(self):
        """TC10 - Valid .docx extension should return SHA-256 string"""
        self.write_json_dict({
            "PROJECT_ID": self.valid_project_id,
            "FILENAME": "abcd1234.docx"
        })
        result = self.manager.register_document(self.test_json_path)
        self.assertEqual(len(result), 64)

    def test_tc11_invalid_extension(self):
        """TC11 - Invalid extension should raise exception"""
        self.write_json_dict({
            "PROJECT_ID": self.valid_project_id,
            "FILENAME": "abcd1234.txt"
        })
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "Invalid FILENAME")

    def test_tc12_filename_wrong_name_length(self):
        """TC12 - Filename NAME with wrong length should raise exception"""
        self.write_json_dict({
            "PROJECT_ID": self.valid_project_id,
            "FILENAME": "abcd123.pdf"
        })
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "Invalid FILENAME")

    def test_tc13_filename_invalid_chars(self):
        """TC13 - Invalid characters in filename NAME should raise exception"""
        self.write_json_dict({
            "PROJECT_ID": self.valid_project_id,
            "FILENAME": "abcd_123.pdf"
        })
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "Invalid FILENAME")

    def test_tc14_filename_no_extension(self):
        """TC14 - FILENAME with no extension should raise exception"""
        self.write_json_dict({
            "PROJECT_ID": self.valid_project_id,
            "FILENAME": "abcd1234"
        })
        with self.assertRaises(EnterpriseManagementException) as ctx:
            self.manager.register_document(self.test_json_path)
        self.assertEqual(ctx.exception.message, "Invalid FILENAME")

    def test_tc15_all_documents_saved(self):
        """TC15 - Valid input should save document to all_documents.json"""
        self.write_json_dict({
            "PROJECT_ID": self.valid_project_id,
            "FILENAME": "abcd1234.pdf"
        })
        self.manager.register_document(self.test_json_path)
        self.assertTrue(os.path.exists("all_documents.json"))


if __name__ == '__main__':
    unittest.main()
