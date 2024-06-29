import os
from databases.google_sheets import GoogleSheet
from model.states import Analisis
from model.utils import get_current_spanish_date_iso,get_id


def main():
    
    FILE_NAME = os.path.join(".secrets","recruiter-427908-67769637005a.json")
    DOCUMENT_NAME = "bbdd_recruiter"
    SHEET_NAME = "analisis"

    bbdd = GoogleSheet(file_name=FILE_NAME, document=DOCUMENT_NAME, sheet_name=SHEET_NAME)
    analisis = Analisis(
        id=get_id(),
        fecha=get_current_spanish_date_iso(),
        puntuacion=33,
        experiencias=[{
            "experiencia":"Abogado",
            "puesto":"Abogado",
            "empresa":"PWC",
            "duracion":"Mayo 2022 / Enero 2023"
            
        }],
        descripcion="Ejemplo desscripcion",
        status="OK"
        )
    values = [atrb for atrb in analisis.model_dump().values()]
    values = ["cnujf","edfme"]
    print("Num fields" ,len(bbdd.sheet.get_all_values()[0]))
    print("Num total record" ,len(bbdd.sheet.get_all_values()))
    print("First record" ,(bbdd.sheet.get_all_values()[0]))
    bbdd.write_data(range=bbdd.get_last_row_range(), values=list(values))


    

if __name__  == "__main__":
    main()
    