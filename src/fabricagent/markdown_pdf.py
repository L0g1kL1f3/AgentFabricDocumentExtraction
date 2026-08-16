
import json
from datetime import date
import os
import tempfile
from notebookutils import mssparkutils
from markitdown import MarkItDown
from pyspark.sql import Row
import uuid
from pyspark.sql import SparkSession
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


def Markdown_file(SourceFolder,FileName,DocumentType,sourcePath,destinationPath,schema):
    md = MarkItDown()
    row=[]
    try:
            tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            tmp.close()
            mssparkutils.fs.cp(sourcePath, f"file:{tmp.name}")

            result = md.convert(tmp.name)
            markdown_text = result.text_content
    
    except Exception as e:

            if os.path.exists(tmp.name):
                os.remove(tmp.name)

            error_text = f"ERROR converting {FileName}: {e}"
            
            output = { "FileName":FileName,
                "Status": "Failed",
            "ErrorMessage" : error_text}

            return output
    
    try:
        mssparkutils.fs.mv(sourcePath, destinationPath, create_path=True)
    
    except Exception as e:
        
        error_text = f"ERROR moving {FileName}: {e}"
        
        output = {"FileName":FileName,
        "Status": "Failed",
        "ErrorMessage" : error_text}
        
        return output

    row.append(
        Row(
            ID=str(uuid.uuid4()),
            NameOfFile=FileName,
            Markdown=markdown_text,
            ExtractedMetadata=False,     
            Path = destinationPath,    
            ExtractionDate=date.today()
        )
    )
    spark = SparkSession.builder.getOrCreate()
   
    df = spark.createDataFrame(row, schema=schema)

    df.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable(f"bronze.{DocumentType}")

    output={"FileName":FileName,
        "Status": "Succeess"}

    return output