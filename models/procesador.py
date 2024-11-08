import os
import sys
import requests
import json
import pandas as pd
from datetime import datetime
from joblib import load
from dotenv import load_dotenv
import numpy as np
from sklearn.preprocessing import StandardScaler

# Agregar este código temporalmente al inicio del script para inspeccionar el modelo
#modelo = load('ml_models/modelo_credit_scoring.joblib')
#print("Tipo de modelo:", type(modelo))
#print("Parámetros del modelo:", modelo.get_params())

class ProcesadorRFC:
    def __init__(self, rfc, version):
        modelo = load(f"ml_models/{version.value}")
        # Cargar variables de entorno

        env_path = '.env'
        if not os.path.exists(env_path):
            raise ValueError(f"No se encontró el archivo .env en: {env_path}")
            
        load_dotenv(env_path)
        self.api_key = os.getenv('API_KEY')
        
        if not self.api_key:
            raise ValueError(f"No se encontró la API key en el archivo {env_path}")
            
        self.rfc = rfc
        self.datos_balance = {}
        self.datos_income = {}
        self.datos_employees = {}
        self.datos_risks = {}
        self.tax_regime = None
        self.rfc_valido = None
        
        print(f"Procesando RFC: {self.rfc}")
        print(f"API Key encontrada: {self.api_key[:5]}...")

    def fetch_balance_sheet(self):
        """Obtiene datos del balance sheet"""
        print("Obteniendo balance sheet...")
        url = f"https://api.syntage.com/taxpayers/{self.rfc}/insights/metrics/balance-sheet"
        
        for formato in ["2014", "2022"]:
            headers = {
                "X-API-Key": self.api_key,
                "X-Insight-Format": formato
            }
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200 and response.json():
                    data = response.json()
                    self.datos_balance[f'format_{formato}'] = data
            except Exception as e:
                print(f"Error obteniendo balance sheet formato {formato}: {e}")
        
        return bool(self.datos_balance)

    def fetch_income_statement(self):
        """Obtiene datos del estado de resultados"""
        print("Obteniendo income statement...")
        url = f"https://api.syntage.com/taxpayers/{self.rfc}/insights/metrics/income-statement"
        
        for formato in ["2014", "2022"]:
            headers = {
                "X-API-Key": self.api_key,
                "X-Insight-Format": formato
            }
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200 and response.json():
                    data = response.json()
                    self.datos_income[f'format_{formato}'] = data
                    if not self.tax_regime:
                        tax_regime_id = data.get('taxRegime', {}).get('id') if data.get('taxRegime') else None
                        self.tax_regime = "PF" if tax_regime_id == 612 else "PM" if tax_regime_id == 601 else None
            except Exception as e:
                print(f"Error obteniendo income statement formato {formato}: {e}")
        
        return bool(self.datos_income)

    def fetch_employees(self):
        """Obtiene datos de empleados"""
        print("Obteniendo datos de empleados...")
        url = f"https://api.syntage.com/taxpayers/{self.rfc}/insights/employees"
        
        headers = {
            "X-API-Key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200 and response.json():
                self.datos_employees = response.json()
        except Exception as e:
            print(f"Error obteniendo datos de empleados: {e}")
        
        return bool(self.datos_employees)

    def fetch_risks(self):
        """Obtiene datos de riesgos"""
        print("Obteniendo datos de riesgos...")
        url = f"https://api.syntage.com/taxpayers/{self.rfc}/insights/risks"
        
        headers = {
            "X-API-Key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 404:
                print(f"\nError: El RFC {self.rfc} no existe en Syntage o no hay datos disponibles")
                self.rfc_valido = False
                return False
            elif response.status_code == 200:
                self.datos_risks = response.json()
                self.rfc_valido = True
                return True
            else:
                print(f"Error obteniendo datos de riesgos: {response.status_code}")
                print(f"Respuesta: {response.text}")
                self.rfc_valido = False
                return False
        except Exception as e:
            print(f"Error obteniendo datos de riesgos: {e}")
            self.rfc_valido = False
            return False

    def procesar_variables_categoricas(self):
        """Procesa las variables categóricas para el modelo"""
        try:
            variables = {
                'datos_employees': 0,
                'tax_compliance': False,
                'blacklist_status': False,
                'blacklisted_counterparties': False,
                'intercompany_transactions': False,
                'customer_concentration': False,
                'supplier_concentration': False,
                'foreign_exchange_risk': False,
                'cash_transaction_risk': False,
                'accounting_insolvency': False,
                'canceled_issued_invoices': False,
                'canceled_received_invoices': False,
                'tax_regime': 'Unknown'
            }

            # Procesar datos de empleados
            if self.datos_employees and 'data' in self.datos_employees:
                variables['datos_employees'] = len(self.datos_employees['data'])

            # Procesar datos de riesgos
            if self.datos_risks and 'data' in self.datos_risks:
                risk_data = self.datos_risks['data']
                
                # Procesar cada tipo de riesgo
                risk_mappings = {
                    'tax_compliance': 'taxCompliance',
                    'blacklist_status': 'blacklistStatus',
                    'blacklisted_counterparties': 'blacklistedCounterparties',
                    'intercompany_transactions': 'intercompanyTransactions',
                    'customer_concentration': 'customerConcentration',
                    'supplier_concentration': 'supplierConcentration',
                    'foreign_exchange_risk': 'foreignExchangeRisk',
                    'cash_transaction_risk': 'cashTransactionRisk',
                    'accounting_insolvency': 'accountingInsolvency',
                    'canceled_issued_invoices': 'canceledIssuedInvoices',
                    'canceled_received_invoices': 'canceledReceivedInvoices'
                }
                
                for var_name, api_name in risk_mappings.items():
                    risk_info = risk_data.get(api_name, {})
                    variables[var_name] = risk_info.get('risky', False) if isinstance(risk_info, dict) else False
                    print(f"Procesando {api_name}: {variables[var_name]}")

            # Procesar régimen fiscal
            variables['tax_regime'] = self.tax_regime if self.tax_regime else 'Unknown'

            return variables
        except Exception as e:
            print(f"Error en procesar_variables_categoricas: {e}")
            return None

    def obtener_valor_balance(self, categoria, año):
        """Obtiene un valor específico del balance sheet"""
        try:
            if not self.datos_balance:
                return 0
                
            # Mapeo de categorías
            categoria_mapping = {
                'Activo total': 'Activo',
                'Pasivo fijo': 'Pasivo',
                'Pasivo circulante': 'Pasivo',
                'Utilidades acumuladas': 'Capital'
            }
            
            categoria_buscar = categoria_mapping.get(categoria, categoria)
                
            # Intentar primero con format_2022
            if 'format_2022' in self.datos_balance:
                data = self.datos_balance['format_2022'].get('data', {}).get('hydra:member', [])
                for item in data:
                    if item.get('category') == categoria_buscar:
                        return item.get(str(año), {}).get('Total', 0) or 0
                        
            # Si no se encuentra en format_2022, intentar con format_2014
            if 'format_2014' in self.datos_balance:
                data = self.datos_balance['format_2014'].get('data', {}).get('hydra:member', [])
                for item in data:
                    if item.get('category') == categoria:
                        return item.get(str(año), {}).get('Total', 0) or 0
                        
            return 0
        except Exception as e:
            print(f"Error obteniendo valor de balance {categoria}: {e}")
            return 0

    def obtener_valor_income(self, categoria, año):
        """Obtiene un valor específico del income statement"""
        try:
            if not self.datos_income:
                return 0
                
            # Mapeo de categorías
            categoria_mapping = {
                'Ingresos': 'Ingresos Netos',
                'Costo de ventas': 'Costo de ventas',
                'Utilidad bruta': 'Utilidad Bruta',
                'Pérdida bruta': 'Pérdida Bruta',
                'Utilidad neta': 'Utilidad neta',
                'Pérdida neta': 'Pérdida neta'
            }
            
            categoria_buscar = categoria_mapping.get(categoria, categoria)
                
            # Intentar primero con format_2022
            if 'format_2022' in self.datos_income:
                data = self.datos_income['format_2022'].get('data', {}).get('hydra:member', [])
                for item in data:
                    if item.get('category') == categoria_buscar:
                        return item.get(str(año), {}).get('Total', 0) or 0
                        
            # Si no se encuentra en format_2022, intentar con format_2014
            if 'format_2014' in self.datos_income:
                data = self.datos_income['format_2014'].get('data', {}).get('hydra:member', [])
                categoria_2014 = categoria_buscar.lower()
                for item in data:
                    if item.get('category').lower() == categoria_2014:
                        return item.get(str(año), {}).get('Total', 0) or 0
                        
            return 0
        except Exception as e:
            print(f"Error obteniendo valor de income {categoria}: {e}")
            return 0

    def procesar_datos_financieros(self):
        try:
            # Verificar si el RFC es válido
            if not hasattr(self, 'rfc_valido') or not self.rfc_valido:
                print(f"\nNo se puede calcular el score: El RFC {self.rfc} no existe en Syntage o no hay datos disponibles")
                return {
                    'score': None,
                    'mensaje': f"RFC {self.rfc} no encontrado o sin datos disponibles en Syntage"
                }

            variables = {}
            
            # Obtener primero las variables categóricas
            variables_categoricas = self.procesar_variables_categoricas()
            if not variables_categoricas:
                raise ValueError("No se pudieron procesar las variables categóricas")
            
            # Procesar datos financieros
            variables.update({
                # Datos 2022
                'activo_total_2022': self.obtener_valor_balance('Activo total', '2022'),
                'pasivo_fijo_2022': self.obtener_valor_balance('Pasivo fijo', '2022'),
                'pasivo_circulante_2022': self.obtener_valor_balance('Pasivo circulante', '2022'),
                'utilidades_acumuladas_2022': self.obtener_valor_balance('Utilidades acumuladas', '2022'),
                'ingresos_2022': self.obtener_valor_income('Ingresos', '2022'),
                'costo_venta_2022': self.obtener_valor_income('Costo de ventas', '2022'),
                'utilidad_bruta_2022': self.obtener_valor_income('Utilidad bruta', '2022'),
                'perdida_bruta_2022': self.obtener_valor_income('Pérdida bruta', '2022'),
                'utilidad_neta_2022': self.obtener_valor_income('Utilidad neta', '2022'),
                'perdida_neta_2022': self.obtener_valor_income('Pérdida neta', '2022'),
                
                # Datos 2023
                'activo_total_2023': self.obtener_valor_balance('Activo total', '2023'),
                'pasivo_fijo_2023': self.obtener_valor_balance('Pasivo fijo', '2023'),
                'pasivo_circulante_2023': self.obtener_valor_balance('Pasivo circulante', '2023'),
                'utilidades_acumuladas_2023': self.obtener_valor_balance('Utilidades acumuladas', '2023'),
                'ingresos_2023': self.obtener_valor_income('Ingresos', '2023'),
                'costo_venta_2023': self.obtener_valor_income('Costo de ventas', '2023'),
                'utilidad_bruta_2023': self.obtener_valor_income('Utilidad bruta', '2023'),
                'perdida_bruta_2023': self.obtener_valor_income('Pérdida bruta', '2023'),
                'utilidad_neta_2023': self.obtener_valor_income('Utilidad neta', '2023'),
                'perdida_neta_2023': self.obtener_valor_income('Pérdida neta', '2023')
            })
            
            # Calcular ratios financieros
            if variables['activo_total_2022'] != 0:
                variables['roa_2022'] = variables['utilidad_neta_2022'] / variables['activo_total_2022']
            else:
                variables['roa_2022'] = 0

            if variables['pasivo_circulante_2022'] != 0:
                variables['razon_liquidez_2022'] = variables['activo_total_2022'] / variables['pasivo_circulante_2022']
            else:
                variables['razon_liquidez_2022'] = 0
                
            if variables['activo_total_2023'] != 0:
                variables['roa_2023'] = variables['utilidad_neta_2023'] / variables['activo_total_2023']
            else:
                variables['roa_2023'] = 0
                
            if variables['pasivo_circulante_2023'] != 0:
                variables['razon_liquidez_2023'] = variables['activo_total_2023'] / variables['pasivo_circulante_2023']
            else:
                variables['razon_liquidez_2023'] = 0

            # Verificar si hay datos financieros
            tiene_datos_financieros = any([
                variables['activo_total_2022'] != 0,
                variables['ingresos_2022'] != 0,
                variables['utilidad_neta_2022'] != 0,
                variables['activo_total_2023'] != 0,
                variables['ingresos_2023'] != 0,
                variables['utilidad_neta_2023'] != 0
            ])
            
            if not tiene_datos_financieros:
                print("\nAdvertencia: No se encontraron datos financieros.")
            
            # Inicializar score
            score = 0.0
            crecimiento_ingresos = 0.0
            
            try:
                # Factor 1: Crecimiento en ingresos (20%)
                if variables['ingresos_2022'] > 0:
                    crecimiento_ingresos = (variables['ingresos_2023'] - variables['ingresos_2022']) / variables['ingresos_2022']
                    score += min(max(crecimiento_ingresos, 0), 1) * 0.20
                
                # Factor 2: ROA promedio (20%)
                roa_promedio = (variables['roa_2022'] + variables['roa_2023']) / 2
                score += min(max(roa_promedio * 5, 0), 1) * 0.20
                
                # Factor 3: Razón de liquidez promedio (20%)
                liquidez_promedio = (variables['razon_liquidez_2022'] + variables['razon_liquidez_2023']) / 2
                score += min(max(liquidez_promedio - 0.5, 0), 1) * 0.20
                
                # Factor 4: Variables categóricas (40%)
                score_categorico = 1.0
                
                # Definir los riesgos a evaluar
                riesgos = {
                    'tax_compliance': variables_categoricas['tax_compliance'],
                    'blacklist_status': variables_categoricas['blacklist_status'],
                    'blacklisted_counterparties': variables_categoricas['blacklisted_counterparties'],
                    'intercompany_transactions': variables_categoricas['intercompany_transactions'],
                    'customer_concentration': variables_categoricas['customer_concentration'],
                    'supplier_concentration': variables_categoricas['supplier_concentration'],
                    'foreign_exchange_risk': variables_categoricas['foreign_exchange_risk'],
                    'cash_transaction_risk': variables_categoricas['cash_transaction_risk'],
                    'accounting_insolvency': variables_categoricas['accounting_insolvency'],
                    'canceled_issued_invoices': variables_categoricas['canceled_issued_invoices'],
                    'canceled_received_invoices': variables_categoricas['canceled_received_invoices']
                }
                
                # Debug de riesgos
                print("\nVerificando riesgos:")
                print("\nProcesando cada riesgo:")
                for nombre_riesgo, valor in riesgos.items():
                    print(f"{nombre_riesgo}: {valor} (tipo: {type(valor)})")
                    if valor:
                        score_categorico -= 0.1
                        print(f"Penalización aplicada, score_categorico ahora: {score_categorico}")
                
                # Debug de empleados
                print(f"\nEmpleados: {variables_categoricas['datos_employees']}")
                if variables_categoricas['datos_employees'] > 50:
                    score_categorico = min(score_categorico + 0.1, 1.0)
                    print(f"Bonus por empleados aplicado, score_categorico ahora: {score_categorico}")
                
                # Debug de régimen fiscal
                print(f"\nRégimen fiscal: {variables_categoricas['tax_regime']}")
                if variables_categoricas['tax_regime'] == 'PM':
                    score_categorico = min(score_categorico + 0.1, 1.0)
                    print(f"Bonus por PM aplicado, score_categorico ahora: {score_categorico}")
                
                score_categorico = max(score_categorico, 0)
                print(f"\nScore categórico final: {score_categorico}")
                
                # Agregar el componente categórico al score final
                score += score_categorico * 0.40
                
                # Si no hay datos financieros recientes (2023), penalizar el score
                if variables['ingresos_2023'] == 0 and variables['activo_total_2023'] == 0:
                    print("\nAdvertencia: No se encontraron datos financieros de 2023. Aplicando penalización.")
                    score = score * 0.7  # Reducir el score en 30%
                
                variables['score'] = score
                print(f"\nScore calculado: {score:.4f}")
                
                # Debug de los componentes del score
                print("\nComponentes del score:")
                print(f"- Crecimiento en ingresos: {min(max(crecimiento_ingresos if variables['ingresos_2022'] > 0 else 0, 0), 1):.4f}")
                print(f"- ROA promedio: {min(max(roa_promedio * 5, 0), 1):.4f}")
                print(f"- Liquidez promedio: {min(max(liquidez_promedio - 0.5, 0), 1):.4f}")
                print(f"- Score categórico: {score_categorico:.4f}")
                
            except Exception as e:
                print(f"Error al calcular el score: {e}")
                variables['score'] = None

            return variables
        except Exception as e:
            print(f"Error en procesar_datos_financieros: {e}")
            return None