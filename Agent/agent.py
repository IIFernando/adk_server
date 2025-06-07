from google.adk.agents import Agent
from google.adk.tools import google_search
import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

def consulta_cnpj(cnpj: str):
    """Esta função atende as requisições de consuta para CNPJ, 
    ela só é chamado quando o usuário digitar por cnpj"""
    
    browser = requests.get('https://www.receitaws.com.br/v1/cnpj/' + cnpj, verify=False)
    resp = json.loads(browser.text)
    nome = resp['nome']
    porte = resp['porte']
    cep = resp['cep']
    logradouro = resp['logradouro']
    numero = resp['numero']
    bairro = resp['bairro']
    municipio = resp['municipio']
    uf = resp['uf']
    cnae = resp['atividade_principal']
    email = resp['email']
    situacao = resp['situacao']
    data = resp['data_situacao']
    motivo_situacao = resp['motivo_situacao']
    simples = resp['simples']
    
    return (str(nome) + '|' + str(porte) + '|' + str(cep) + '|' + str(logradouro) + '|' + 
                    str(numero) + '|' + str(bairro) + '|' + str(municipio) + '|' + str(uf) + '|' + str(cnae)
                    + '|' + email + '|' + situacao + '|' + data + '|' + motivo_situacao + '|' + str(simples))

def consulta_ncm(ncm: str):
    """Esta função atende as requisições de consuta NCM (NCMs (Nomenclatura Comum do Mercosul) Convenção entre os 
    países membros do Mercosul para reconhecer facilmente os bens, serviços e fatores produtivos negociados entre si. 
    Com o alinhamento da obrigatoriedade de emissão de NF-e (Nota Fiscal eletrônica) e a possível validação de dados 
    pelas SEFAZ, não demorou para o governo obrigar essa nomenclatura nos cadastros de produtos."""
    
    browser = requests.get(f'https://brasilapi.com.br/api/ncm/v1?search={ncm}', verify=False)
    resp = json.loads(browser.text)
    
    return resp

def consulta_cep(cep: str):
    """Esta função atende as requisições de consuta  CEP (Código de Endereçamento Postal) é um sistema
    de códigos que visa racionalizar o processo de encaminhamento e entrega de correspondências através 
    da divisão do país em regiões postais. ... Atualmente, o CEP é composto por oito dígitos, cinco de um 
    lado e três de outro. Cada algarismo do CEP possui um significado"""
    
    browser = requests.get(f'https://brasilapi.com.br/api/cep/v2/{cep}', verify=False)
    resp = json.loads(browser.text)
    
    return resp

def fatura_imposto(cnpj:str , valorPagar: str, dataEmissao: str, dataVencimento: str):
    """Está função será responsável por enviar guias de pagamentos de todos os layouts para o SAP"""
    data_brEmissao = dataEmissao
    diaEmissao, mesEmissao, anoEmissao = data_brEmissao.split("/")
    data_usEmissao = f"{anoEmissao}{mesEmissao}{diaEmissao}"
    
    data_brEmissao = dataVencimento
    diaVencimento, mesVencimento, anoVencimento = data_brEmissao.split("/")
    data_usVencimento = f"{anoVencimento}{mesVencimento}{diaVencimento}"
    
    load_dotenv()

    # URL da API
    url = "https://loggi-dev-qa.it-cpi003-rt.cfapps.us10.hana.ondemand.com/http/v1/getfatura"

    # Lendo as variáveis de ambiente
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    
    payload = {
                "CNPJ": cnpj,
                "DOCUMENT_TYPE": "TESTEISS",
                "COMPANY_CODE": "LL4B",
                "AMOUNT": valorPagar,
                "ID": "ISS",
                "DOCUMENT_DATE": data_usEmissao,
                "DUE_DATE": data_usVencimento,
                "CURRENCY": "BRL"
            }
    
    response = requests.get(
                url,
                json=payload,
                auth=HTTPBasicAuth(username, password)
            )

root_agent = Agent(
    name="agent",
    model="gemini-2.0-flash",
    description="Especialista no ERP SAP e na area tributária",
    instruction="""Você é um especialista no sistima SAP assim como tambem dominá o sistema tributário brasileiro
                fazendo pesquisas assim como consultas que sejam solicitadas. Em alguns casos será necessario
                utilizar sua ferramenta de busca que é a tool:
                - google_search""",
                
    tools=[consulta_cnpj, consulta_ncm, consulta_cep, fatura_imposto]
)
