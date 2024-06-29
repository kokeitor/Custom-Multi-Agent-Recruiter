import os
from databases.google_sheets import GoogleSheet
from model.states import Analisis
from model.utils import get_current_spanish_date_iso,get_id,setup_logging
import logging
import pandas as pd


# Logger initializer
logger = logging.getLogger(__name__)


def main():
    
    setup_logging()
    FILE_NAME = os.path.join(".secrets","recruiter-427908-67769637005a.json")
    DOCUMENT_NAME = "bbdd_recruiter"
    SHEET_NAME = "analisis"

    bbdd = GoogleSheet(file_name=FILE_NAME, document=DOCUMENT_NAME, sheet_name=SHEET_NAME)
    analisis = Analisis(
        id=get_id(),
        fecha=get_current_spanish_date_iso(),
        puntuacion=33,
        experiencias=[
            {
            "experiencia":"Abogado",
            "puesto":"Abogado",
            "empresa":"PWC",
            "duracion":"Mayo 2022 / Enero 2023"  
        },
        {
            "experiencia":"furbol",
            "puesto":"furbol",
            "empresa":"barcelona",
            "duracion":"Mayo 2022 / Enero 2023"  
        }
                      ],
        descripcion="Ejemplo desscripcion",
        status="OK"
        )
    

    print("Num fields" ,len(bbdd.sheet.get_all_values()[0]))
    print("Num total record" ,len(bbdd.sheet.get_all_values()))
    print("First record" ,(bbdd.sheet.get_all_values()[0]))
    bbdd.write_data(range=bbdd.get_last_row_range(), values=[GoogleSheet.get_analisis_format_record(analisis=analisis)])

    """ 
    bbdd.write_data(range=bbdd.get_last_row_range(), values=[analisis_bbdd])
    
    values = [["d92113c5-b456-4294-addc-ccd7f9a17212","perdon, Te amo"]]
    print(bbdd.read_data_by_uid(uid="d92113c5-b456-4294-addc-ccd7f9a17212"))
    bbdd.write_data_by_uid(uid="d92113c5-b456-4294-addc-ccd7f9a17212", values=values)
    print(bbdd.read_data_by_uid(uid="d92113c5-b456-4294-addc-ccd7f9a17212"))
    
    """


if __name__  == "__main__":
    main()
    