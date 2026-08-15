import json
from datetime import date
import os
import tempfile
from notebookutils import mssparkutils
from markitdown import MarkItDown
from pyspark.sql import Row
import uuid
from pyspark.sql.types import (
    StructType, StructField, StringType, BooleanType, DateType
)



def transform_markdown(sourcePath,FileName):
    md = MarkItDown()

    try:
            tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            tmp.close()
            mssparkutils.fs.cp(sourcePath, f"file:{tmp.name}")

            result = md.convert(tmp.name)
            markdown_text = result.text_content

    except Exception as e:
            error_text = f"ERROR converting {FileName}: {e}"
            
            output = { "FileName":FileName,
                "Status": "Failed",
            "ErrorMessage" : error_text}
            return False , output

    if os.path.exists(tmp.name):
            os.remove(tmp.name)
    
    return True , markdown_text

def move_file(sourcePath,destinationPath,FileName):

    try:
        mssparkutils.fs.mv(sourcePath, destinationPath, create_path=True)
        path = destinationPath
    
    except Exception as e:
        error_text = f"ERROR moving {FileName}: {e}"
        output = {"FileName":FileName,
        "Status": "Failed",
        "ErrorMessage" : error_text}

        return False, output

    return True , destinationPath
    