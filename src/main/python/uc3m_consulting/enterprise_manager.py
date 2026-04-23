"""Module """
import json
import os
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.project_document import ProjectDocument


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """Returns True if the CIF received is valid, False otherwise"""
        _ = cif
        return True

    def register_document(self, input_file: str):
        """Registers a document for a project"""
        if not os.path.exists(input_file):
            raise EnterpriseManagementException("Input file not found")
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException("File is not valid JSON") from exc
        if not isinstance(data, dict):
            raise EnterpriseManagementException("JSON does not have expected structure")
        if set(data.keys()) != {"PROJECT_ID", "FILENAME"}:
            raise EnterpriseManagementException("JSON does not have expected structure")
        project_id = data["PROJECT_ID"]
        if not re.match(r'^[0-9a-fA-F]{32}$', project_id):
            raise EnterpriseManagementException("Invalid PROJECT_ID")
        filename = data["FILENAME"]
        name = filename.split(".")[0] if "." in filename else filename
        if len(name) != 8:
            raise EnterpriseManagementException("Invalid FILENAME")
        ext = "." + filename.split(".")[1] if "." in filename else ""
        if ext not in (".pdf", ".docx", ".xlsx"):
            raise EnterpriseManagementException("Invalid FILENAME")
        if not re.match(r'^[a-zA-Z0-9]+$', name):
            raise EnterpriseManagementException("Invalid FILENAME")
        corp_file = "corporate_operations.json"
        if not os.path.exists(corp_file):
            raise EnterpriseManagementException("PROJECT_ID not registered")
        with open(corp_file, "r", encoding="utf-8") as f:
            projects = json.load(f)
        registered_ids = [p["project_id"] for p in projects]
        if project_id.lower() not in [pid.lower() for pid in registered_ids]:
            raise EnterpriseManagementException("PROJECT_ID not registered")
        doc = ProjectDocument(project_id, filename)
        docs_file = "all_documents.json"
        if os.path.exists(docs_file):
            with open(docs_file, "r", encoding="utf-8") as f:
                docs = json.load(f)
        else:
            docs = []
        docs.append(doc.to_json())
        with open(docs_file, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2)
        return doc.document_signature
