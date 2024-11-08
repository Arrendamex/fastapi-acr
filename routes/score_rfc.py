from models.procesador import ProcesadorRFC
from fastapi import APIRouter
from fastapi import HTTPException

from enum import Enum
class ModelVersion(str, Enum):    
    v1 = "modelo_credit_scoring.joblib"

score = APIRouter()

@score.post("/score") 
def calcular_score(rfc: str, version: ModelVersion):
    """ 
    Obtiene el score del RFC 
    """
    
    procesador = ProcesadorRFC(rfc, version)
    
    print("\nObteniendo datos...")
    if not procesador.fetch_balance_sheet() or \
        not procesador.fetch_income_statement() or \
        not procesador.fetch_employees() or \
        not procesador.fetch_risks():
        print(f"\nNo se puede continuar: No hay datos suficientes para el RFC {rfc}")
        raise HTTPException(status_code=404, detail=f"No hay registro del RFC {rfc}")

    resultado = procesador.procesar_datos_financieros()
    
    if resultado.get('score') is None:
        print(f"\n{resultado.get('mensaje', 'Error desconocido al procesar datos')}")
        raise HTTPException(status_code=404, detail=f"No se pudo procesar el RFC {rfc}")

    print("\nProcesando variables categóricas...")
    variables_categoricas = procesador.procesar_variables_categoricas()
    
    print("Procesando datos financieros...")
    variables_financieras = procesador.procesar_datos_financieros()
    
    if variables_categoricas and variables_financieras:
        print("\nVariables procesadas exitosamente:\n")
        print("Variables categóricas:")
        for k, v in variables_categoricas.items():
            print(f"{k}: {v}")
        
        print("\nVariables financieras:")
        for k, v in variables_financieras.items():
            if k != 'score':  # Mostrar el score al final
                print(f"{k}: {v}")
        
        if variables_financieras.get('score') is not None:
            score = variables_financieras['score']
            print(f"\nScore final: {score:.4f}")

            # Interpretar el score
            if score >= 0.8:
                print("Calificación: Excelente")
                variables_financieras["calificacion"] = "Excelente"
            elif score >= 0.6:
                print("Calificación: Bueno")
                variables_financieras["calificacion"] = "Bueno"    
            elif score >= 0.4:
                print("Calificación: Regular")
                variables_financieras["calificacion"] = "Regular"
            else:
                print("Calificación: Riesgo alto")
                variables_financieras["calificacion"] = "Alto"

            # Retornar el objeto completo
        return variables_financieras    
        


