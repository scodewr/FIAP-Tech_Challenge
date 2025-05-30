import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, Query, HTTPException, Request, Response, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
import pybreaker
from typing import Optional, Type, List
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import hashlib
import traceback
from collections import defaultdict
from enum import Enum
from processing_entity import ProcessingEntity
from pc_categories_enum import ProcessingCategoryEnum
from production_entity import ProductionEntity
from pd_categories_enum import ProductionCategoryEnum
from pydantic import BaseModel
from marketing_entity import MarketingEntity
from mk_categories_enum import MarketingCategoryEnum
from deep_translator import GoogleTranslator
from importation_entity import ImportationEntity
from exportation_entity import ExportationEntity
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from fastapi.openapi.utils import get_openapi

# Classe para autenticação via HTTP Bearer
security = HTTPBearer()

def validate_token(endpoint_permission: str = None):
    """
    Decorator para validar o token JWT e verificar permissões.

    :param endpoint_permission: Permissão necessária para acessar o endpoint.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extrai o token do cabeçalho Authorization
            request: Request = kwargs.get("request")
            authorization: str = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token não fornecido ou inválido.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            token = authorization.split(" ")[1]

            # Verifica o token JWT
            payload = verify_access_token(token)

            # Verifica se o usuário tem a permissão necessária
            if endpoint_permission and endpoint_permission not in payload.get("permissions", []):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permissão negada para acessar este endpoint.",
                )

            # Apenas valida o token e permite a execução do endpoint
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Configuração do logger
log_handler = logging.StreamHandler()  # Exibe os logs no console
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z"  # Formato ISO 8601
)
log_handler.setFormatter(formatter)

# Configura o logger raiz
logging.basicConfig(
    level=logging.INFO,  # Define o nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    handlers=[log_handler, logging.FileHandler("app.log", encoding="utf-8")]  # Adiciona o handler de arquivo
)

# Configura os loggers do FastAPI e Uvicorn
logging.getLogger("uvicorn.access").handlers = [log_handler]
logging.getLogger("uvicorn.error").handlers = [log_handler]
logging.getLogger("uvicorn").handlers = [log_handler]

# Obtém o logger principal
logger = logging.getLogger("vitivinicultura_api")

# Configuração do FastAPI
app = FastAPI(
    title="Vitivinicultura API",
    version="1.0.0",
    description="API para retorno de dados sobre vitivinicultura do estado do Rio Grande do Sul.",
    openapi_tags=[
        {
            "name": "Autenticação",
            "description": "Endpoints relacionados à autenticação e autorização."
        },
        {
            "name": "Informações de Produção",
            "description": "Endpoints para retornar informações de produção vitivinícola."
        },
        {
            "name": "Informações de Processamento",
            "description": "Endpoints para retornar informações de processamento vitivinícola."
        },
        {
            "name": "Informações de Marketing",
            "description": "Endpoints para retornar informações de marketing vitivinícola."
        },
        {
            "name": "Informações de Importação",
            "description": "Endpoints para retornar informações de importação vitivinícola."
        },
        {
            "name": "Informações de Exportação",
            "description": "Endpoints para retornar informações de exportação vitivinícola."
        }
    ]
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Ambiente de Desenvolvimento"},
        {"url": "https://homologacao.vitivinicultura.com", "description": "Ambiente de Homologação"},
        {"url": "https://api.vitivinicultura.com", "description": "Ambiente de Produção"},
    ]
    app.openapi_schema = openapi_schema
    return openapi_schema

# Substituir o esquema OpenAPI padrão pelo personalizado
app.openapi = custom_openapi

#logger.info("Aplicação FastAPI inicializada.", extra={"module": "main", "status": "running"})

# Configuração do Circuit Breaker
breaker = pybreaker.CircuitBreaker(
    fail_max=3,  # Número máximo de falhas antes de abrir o circuito
    reset_timeout=10  # Tempo em segundos para tentar reabrir o circuito
)
#logger.info("Circuit Breaker configurado.", extra={"fail_max": 3, "reset_timeout": 10})

# Configuração do Rate Limiter
rate_limit = defaultdict(int)  # Dicionário para rastrear requisições por IP
RATE_LIMIT = 10  # Limite de requisições por minuto
#logger.info("Rate Limiter configurado.", extra={"rate_limit": RATE_LIMIT})

# Middleware para rate limiting
@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    client_ip = request.client.host
    rate_limit[client_ip] += 1
    logger.info("Requisição recebida.", extra={"client_ip": client_ip, "total_requests": rate_limit[client_ip]})

    if rate_limit[client_ip] > RATE_LIMIT:
        logger.warning("Rate limit excedido.", extra={"client_ip": client_ip, "rate_limit": RATE_LIMIT})
        return JSONResponse(
            status_code=429,
            content={"error": True, "message": "Rate limit exceeded. Try again later."}
        )

    response = await call_next(request)
    return response

# Manipulador para exceções HTTP
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error("HTTPException capturada.", extra={"detail": exc.detail, "status_code": exc.status_code})
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
        },
    )

# Manipulador para erros de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error("Erro de validação capturado.", extra={"errors": exc.errors()})
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Erro de validação nos dados enviados.",
            "details": exc.errors(),
            "status_code": 422,
        },
    )

# Manipulador para exceções genéricas
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_trace = traceback.format_exc()
    logger.critical("Erro não tratado capturado.", extra={"error_trace": error_trace})
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde.",
            "details": str(exc),
            "status_code": 500,
        },
    )

# Função para baixar o CSV com retries, timeout e circuit breaker
@breaker
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def download_csv(url: str) -> pd.DataFrame:
    logger.info("Iniciando download do CSV.", extra={"url": url})
    response = requests.get(url, timeout=10)  # Timeout de 10 segundos
    if response.status_code != 200:
        logger.error("Falha ao acessar a URL.", extra={"url": url, "status_code": response.status_code})
        raise HTTPException(status_code=503, detail="Falha ao acessar a página da Embrapa.")

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    link_tag = soup.find("a", href=True, text=None, class_="footer_content")
    if not link_tag or not link_tag.find("span", string=lambda s: s and "DOWNLOAD" in s.upper()):
        logger.error("Link de download não encontrado na página.", extra={"url": url})
        raise HTTPException(status_code=404, detail="Download link não encontrado.")

    download_url = link_tag["href"]
    if download_url.startswith("/"):
        download_url = "http://vitibrasil.cnpuv.embrapa.br" + download_url
    elif not download_url.startswith("http"):
        download_url = "http://vitibrasil.cnpuv.embrapa.br/" + download_url.lstrip("/")

    logger.info("Baixando CSV.", extra={"download_url": download_url})
    df = pd.read_csv(download_url, delimiter=";")
    logger.info("Download do CSV concluído.", extra={"download_url": download_url})
    return df

# Função principal para processar os dados
def get_csv_data_from_embrapa(
    url: str,
    model: Type[BaseModel],
    request: Request,
    response: Response,
    page: int = 1,
    page_size: int = 10,
    category_enum: Optional[Enum] = None,
    delimiter_csv: str = ";",
    value_name_column: str = "production"
):
    logger.info("Processando dados do CSV.", extra={"url": url})
    cached_file = get_csv_from_cache(url, request)
    cache_warning = False
    if cached_file:
        logger.info("Arquivo encontrado no cache.", extra={"cached_file": cached_file})
        df = pd.read_csv(cached_file, delimiter=delimiter_csv)
        cache_warning = True
    else:
        try:
            df = download_csv(url)  # Baixa o CSV com retries e circuit breaker
            save_csv_to_cache(url, df)  # Salva no cache
            set_cache_cookie(response, url)  # Define o cookie
        except pybreaker.CircuitBreakerError:
            logger.error("Circuit breaker ativado.", extra={"url": url})
            raise HTTPException(status_code=503, detail="Serviço Embrapa indisponível. Tente novamente mais tarde.")
        except RetryError:
            logger.error("Falha ao acessar a página da Embrapa após múltiplas tentativas.", extra={"url": url})
            raise HTTPException(status_code=503, detail="Falha ao acessar a página da Embrapa após múltiplas tentativas.")

    logger.info("Iniciando processamento do DataFrame.", extra={"url": url})
    start = (page - 1) * page_size
    end = start + page_size

    model_list = preprocess_data(df, model, category_enum, value_name_column)
    paginated_model_list = model_list[start:end]

    result = {
        "page": page,
        "page_size": page_size,
        "total_rows": len(model_list),
        "Dados_Producao": [model.model_dump(exclude={"control"}) for model in paginated_model_list]
    }
    if cache_warning:
        logger.warning("Os dados foram carregados do cache.", extra={"url": url})
        result["Warning"] = "Os dados foram carregados do cache. Para atualizar, limpe o cache ou aguarde a expiração do cookie."
    logger.info("Processamento concluído.", extra={"url": url, "total_rows": len(model_list)})
    return result

# Exemplo para ProductionView, ajuste para outros endpoints conforme o BaseModel de cada um

@app.post("/login", dependencies=[], tags=["Autenticação"])
async def login(username: str, password: str):
    """
    Endpoint para autenticação e geração de token JWT.

    :param username: Nome de usuário.
    :param password: Senha do usuário.
    :return: Token JWT.
    """
    # Valida o usuário (sem verificar o endpoint)
    user = validate_user(username, password)

    # Gera o token JWT com os dados do usuário
    token = create_access_token({"sub": user["username"], "permissions": user["permissions"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get(
    "/info/production",
    tags=["Informações de Produção"],
    dependencies=[Depends(security)],
    response_model=List[ProductionEntity],  # Modelo de resposta
    responses={
        503: {
            "description": "Erro no serviço da Embrapa.",
            "content": {
                "application/json": {
                    "example": {
                        "error": True,
                        "message": "Serviço Embrapa indisponível. Tente novamente mais tarde.",
                        "status_code": 503
                    }
                }
            },
        },
    },
)
@validate_token(endpoint_permission="info_production")
async def info_production(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    """
    Endpoint para retornar informações de produção.
    """
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'
    return get_csv_data_from_embrapa(
        request=request,
        response=response,
        url=url,
        model=ProductionEntity,
        page=page,
        page_size=page_size,
        category_enum=ProductionCategoryEnum,
        delimiter_csv=";",
        value_name_column="production"
    )

@app.get(
    "/info/processing",
    tags=["Informações de Processamento"],
    dependencies=[Depends(security)],
    response_model=List[ProcessingEntity],  
    responses={
        503: {
            "description": "Erro no serviço da Embrapa.",
            "content": {
                "application/json": {
                    "example": {
                        "error": True,
                        "message": "Serviço Embrapa indisponível. Tente novamente mais tarde.",
                        "status_code": 503
                    }
                }
            },
        },
    },
)
@validate_token(endpoint_permission="info_processing")
async def info_processing(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03'
    return get_csv_data_from_embrapa(
        request=request,
        response=response,
        url=url,
        model=ProcessingEntity,
        page=page,
        page_size=page_size,
        category_enum=ProcessingCategoryEnum,
        delimiter_csv=";",
        value_name_column="processing"
    )

# Repita para os outros endpoints, passando o BaseModel correto de cada um.

@app.get(
    "/info/marketing", 
    tags=["Informações de Marketing"],
    dependencies=[Depends(security)],
    response_model=List[MarketingEntity],
    responses={
        503: {
            "description": "Erro no serviço da Embrapa.",
            "content": {
                "application/json": {
                    "example": {
                        "error": True,
                        "message": "Serviço Embrapa indisponível. Tente novamente mais tarde.",
                        "status_code": 503
                    }
                }
            },
        },
    },
)
@validate_token(endpoint_permission="info_marketing")
async def info_marketing(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'
    return get_csv_data_from_embrapa(
        request=request,
        response=response,
        url=url,
        model=MarketingEntity,
        page=page,
        page_size=page_size,
        category_enum=MarketingCategoryEnum,
        delimiter_csv=";",
        value_name_column="marketing"
    )

@app.get(
    "/info/importation", 
    tags=["Informações de Importação"],
    dependencies=[Depends(security)],
    response_model=List[ImportationEntity],
    responses={
        503: {
            "description": "Erro no serviço da Embrapa.",
            "content": {
                "application/json": {
                    "example": {
                        "error": True,
                        "message": "Serviço Embrapa indisponível. Tente novamente mais tarde.",
                        "status_code": 503
                    }
                }
            },
        },
    },
)
@validate_token(endpoint_permission="info_importation")
async def info_importation(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
):
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05'
    return get_csv_data_from_embrapa(
        request=request,
        response=response,
        url=url,
        model=ImportationEntity,
        page=page,
        page_size=page_size,
        delimiter_csv="\t",
        value_name_column="importation"
    )

@app.get(
    "/info/exportation", 
    tags=["Informações de Exportação"],
    dependencies=[Depends(security)],
    response_model=List[ExportationEntity], 
    responses={
        503: {
            "description": "Erro no serviço da Embrapa.",
            "content": {
                "application/json": {
                    "example": {
                        "error": True,
                        "message": "Serviço Embrapa indisponível. Tente novamente mais tarde.",
                        "status_code": 503
                    }
                }
            },
        },
    },
)
@validate_token(endpoint_permission="info_exportation")
async def info_exportation(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06'
    return get_csv_data_from_embrapa(
        request=request,
        response=response,
        url=url,
        model=ExportationEntity,
        page=page,
        page_size=page_size,
        delimiter_csv="\t",
        value_name_column="exportation"
    )

def translate_column_names(df: pd.DataFrame, target_lang: str = "en") -> pd.DataFrame:
    """
    Traduz automaticamente os nomes das colunas do DataFrame para o idioma desejado.

    :param df: DataFrame cujas colunas serão traduzidas.
    :param target_lang: Idioma de destino (padrão: inglês).
    :return: DataFrame com os nomes das colunas traduzidos.
    """
    translator = GoogleTranslator(source="auto", target=target_lang)
    translated_columns = {col: translator.translate(col) for col in df.columns}
    return df.rename(columns=translated_columns)

def preprocess_data(
    df: pd.DataFrame,
    model: Type[BaseModel],
    category_enum: Optional[Enum] = None,
    value_name_column: str = "production"
) -> List[BaseModel]:
    """
    Realiza o tratamento inicial dos dados do DataFrame e retorna uma lista de instâncias do BaseModel.
    - Remove espaços extras das colunas e células.
    - Substitui valores nulos por "N/A".
    - Remove linhas onde todas as colunas numéricas (anos) estão vazias.
    - Remove linhas onde qualquer célula contém um valor igual a algum valor da Enum fornecida.
    - Aplica a transformação "melt" no DataFrame
    - Usa a coluna 'control' para gerar o BaseModel, mas remove-a da exibição final.

    :param df: DataFrame a ser processado.
    :param model: O BaseModel para mapear os dados.
    :param category_enum: Enum opcional para filtrar categorias.
    :return: Lista de instâncias do BaseModel.
    """
    # Remove espaços extras dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Remove espaços extras de todas as células
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Substitui valores nulos por "N/A"
    df.fillna("N/A", inplace=True)

    # Remove linhas onde todas as colunas numéricas (anos) estão vazias ou zero
    numeric_columns = df.select_dtypes(include=["number"]).columns
    if not numeric_columns.empty:
        df = df[df[numeric_columns].sum(axis=1) > 0]

    # Remove linhas onde qualquer célula contém um valor igual a algum valor da Enum
    if category_enum:
        enum_values = set(item.value.upper() for item in category_enum)
        rows_to_remove = df.apply(lambda row: any(str(cell).upper() in enum_values for cell in row), axis=1)
        df = df[~rows_to_remove]

    # Aplica a transformação "melt" no DataFrame, se solicitado
    
    colunas_years = [col for col in df.columns if str(col).isdigit()]
    colunas_info = [col for col in df.columns if col not in colunas_years]
    df = df.melt(id_vars=colunas_info, value_vars=colunas_years, var_name='year', value_name=value_name_column)

    # Gera o field_map automaticamente
    model_fields = model.model_fields.keys()
    field_map = {field: field for field in model_fields if field in df.columns}

    # Converte o DataFrame em uma lista de BaseModel
    base_model_list = []
    for _, row in df.iterrows():
        # Usa a coluna 'control' para gerar o BaseModel
        data = {model_field: row.get(df_field) for model_field, df_field in field_map.items()}
        base_model_list.append(model(**data))

    # Remove a coluna 'control' do DataFrame para exibição final

    return base_model_list


CACHE_FOLDER = "cache"  # Nome da pasta onde os arquivos serão armazenados

def save_csv_to_cache(url: str, df: pd.DataFrame) -> str:
    """
    Salva o DataFrame como um arquivo CSV em uma pasta de cache.
    O nome do arquivo é gerado com base no hash da URL.

    :param url: URL do CSV.
    :param df: DataFrame a ser salvo.
    :return: Caminho completo do arquivo salvo.
    """
    # Gera um hash único para o nome do arquivo com base na URL
    file_hash = hashlib.md5(url.encode()).hexdigest()
    file_path = os.path.join(CACHE_FOLDER, f"{file_hash}.csv")

    # Cria a pasta de cache, se não existir
    os.makedirs(CACHE_FOLDER, exist_ok=True)

    # Salva o DataFrame como CSV
    df.to_csv(file_path, index=False, encoding="utf-8", sep=";")
    return file_path


def get_csv_from_cache(url: str, request: Request) -> Optional[str]:
    """
    Verifica se o arquivo CSV está em cache, usando um cookie ou verificando a pasta de cache.

    :param url: URL do CSV.
    :param request: Objeto Request do FastAPI.
    :return: Caminho completo do arquivo em cache, ou None se não existir.
    """
    # Verifica se o cookie indica que o arquivo está em cache
    file_hash = hashlib.md5(url.encode()).hexdigest()
    cached_file = os.path.join(CACHE_FOLDER, f"{file_hash}.csv")

    if request.cookies.get(file_hash) == "exists":
        # Retorna o caminho do arquivo se o cookie indicar que ele existe
        if os.path.exists(cached_file):
            return cached_file

    # Verifica se o arquivo existe na pasta de cache
    if os.path.exists(cached_file):
        return cached_file

    return None


def set_cache_cookie(response: Response, url: str):
    """
    Define um cookie para indicar que o arquivo CSV está em cache.

    :param response: Objeto Response do FastAPI.
    :param url: URL do CSV.
    """
    file_hash = hashlib.md5(url.encode()).hexdigest()
    response.set_cookie(key=file_hash, value="exists", max_age=3600)  # Cookie válido por 1 hora

# Configurações do JWT
SECRET_KEY = "sua_chave_secreta_super_segura"  # Substitua por uma chave secreta forte
ALGORITHM = "HS256"  # Algoritmo de assinatura
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de expiração do token (em minutos)

# Simulação de um banco de dados de usuários e permissões
USERS_DB = {
    "admin": {"password": "password", "permissions": ["info_production", "info_processing", "info_marketing", "info_importation", "info_exportation"]},
    "info_production": {"password": "info_production", "permissions": ["info_production"]},
    "user1": {"password": "user1pass", "permissions": []},  # Sem permissões
}

def validate_user(username: str, password: str) -> dict:
    """
    Valida as credenciais do usuário.

    :param username: Nome de usuário.
    :param password: Senha do usuário.
    :return: Dados do usuário, se válido.
    :raises HTTPException: Se as credenciais forem inválidas.
    """
    user = USERS_DB.get(username)
    if not user or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"username": username, "permissions": user["permissions"]}

def create_access_token(data: dict) -> str:
    """
    Gera um token JWT com os dados fornecidos.

    :param data: Dados a serem incluídos no token.
    :return: Token JWT assinado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    """
    Valida o token JWT e retorna os dados decodificados.

    :param token: Token JWT a ser validado.
    :return: Dados decodificados do token.
    :raises HTTPException: Se o token for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

