import gspread
import pandas as pd
import logging
from model.utils import get_current_spanish_date_iso


# Logger initializer
logger = logging.getLogger(__name__)


class GoogleSheet:
    COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    def __init__(self, file_name : str , document : str , sheet_name :str):
        self.gc = gspread.service_account(filename=file_name)
        self.sh = self.gc.open(document)
        self.sheet = self.sh.worksheet(sheet_name)

    def read_data(self, range): #range = "A1:E1". Data devolvera un array de la fila 1 desde la columna A hasta la E
        data = self.sheet.get(range)
        return data

    def read_data_by_uid(self, uid):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        print(df)
        filtered_data = df[df['id'] == uid]
        return filtered_data #devuelve un data frame de una tabla, de dos filas siendo la primera las cabeceras de las columnas y la segunda los valores filtrados para acceder a un valor en concreto df["nombre"].to_string()
    
    def write_data(self, range : str, values: list[list]): #range ej "A1:V1". values must be a list of list
        tst_insertion = get_current_spanish_date_iso()
        total_fields = self.get_total_fields()
        validated_values = self.validate_records(values=values)
        for record in validated_values:
            for field_index , _ in enumerate(record):
                if field_index + 1 == total_fields:
                        record.append(tst_insertion)
        print(validated_values)
        self.sheet.update(range, validated_values)

    def write_data_by_uid(self, uid, values): 
        # Find the row index based on the UID
        cell = self.sheet.find(uid)
        row_index = cell.row
        # Update the row with the specified values
        self.sheet.update(f"A{row_index}:E{row_index}", values)

    def get_last_row_range(self):   
        last_row = len(self.sheet.get_all_values()) + 1
        deta = self.sheet.get_values()
        range_start = f"A{last_row}"
        range_end = f"{chr(ord('A') + len(deta[0]) - 1)}{last_row}"
        return f"{range_start}:{range_end}"
    
    def get_all_values(self):
        #self.sheet.get_all_values () # this return a list of list, so the get all records is easier to get values filtering
        return self.sheet.get_all_records() # this return a list of dictioraies so the key is the name column and the value is the value for that particular column
    
    def get_total_fields(self) -> int:
        return len(self.sheet.get_all_values()[0])
    
    def get_field_names(self) -> list[str]:
        return self.sheet.get_all_values()[0]
    
    def get_total_records(self) -> int:
        return len(self.sheet.get_all_values())
    
    def validate_records(self,  values: list[list]) -> list[list]:
        total_fields = self.get_total_fields()
        if isinstance(values,list):
            for record in values:
                if isinstance(record,list):
                    if len(record) < total_fields:
                        extension_length = total_fields - len(record)
                        record.extend([""] * extension_length)
                    elif len(record) < total_fields:
                        logger.warning("Warning: The current record fields are greater than the actual BBDD fields.")
                else:
                    logger.error(f"Record not a list type -> {record}")
            return values
        else:
            logger.error(f"Trying inserting not a list[list] type -> {values}")
        