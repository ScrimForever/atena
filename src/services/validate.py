import os.path
from dataclasses import dataclass
from utils.settings_config import settings
from loguru import logger
from schemas.validation import ValidationSchemaClientes, ValidationSchemaPedidos
from pydantic import ValidationError
import json
from json.decoder import JSONDecodeError
from fastapi.responses import JSONResponse

@dataclass
class ValidateJSON:

    @staticmethod
    async def _validate_pedidos():
        try:
            with open(os.path.join(os.getcwd(), settings.upload_files_bucket, "pedidos.json"), 'r') as f:
                pedidos = json.load(f)
                logger.success(pedidos)
                error_pedidos = []
                for index, cliente in enumerate(pedidos):
                    logger.info("Verifying schemas.")
                    try:
                        _validate = ValidationSchemaPedidos(**cliente)
                    except ValidationError as e:
                        logger.debug("Validation error")
                        error_pedidos.append([{"line on file": index + 1}, e.errors()])
                    except Exception as e:
                        logger.error(e)
                if len(error_pedidos) > 0:
                    return error_pedidos
                return True
        except FileNotFoundError:
            logger.error("File pedidos.json not found.")

    @staticmethod
    async def _validate_client():
        try:
            with open(os.path.join(os.getcwd(), settings.upload_files_bucket, "clientes.json"), 'r') as f:
                clientes = json.load(f)
                logger.success(clientes)
                error_cliente = []
                for index, cliente in enumerate(clientes):
                    logger.info("Verifying schemas.")
                    try:
                        _validate = ValidationSchemaClientes(**cliente)
                    except ValidationError as e:
                        logger.debug("Validation error")
                        error_cliente.append([{"line on file": index+1}, e.errors()])
                    except Exception as e:
                        logger.error(e)
                if len(error_cliente) > 0:
                    return error_cliente
                return True
        except FileNotFoundError:
            logger.error("File clientes.json not found.")

    async def validate_input_jsons(self):
        _content_files_error = {}
        try:
            _is_valid_cliente = await self._validate_client()
            _is_valid_pedidos = await self._validate_pedidos()
            if _is_valid_cliente is not True:
                _content_files_error.update({"cliente.json": _is_valid_cliente})
            if _is_valid_pedidos is not True:
                _content_files_error.update({"pedidos.json": _is_valid_pedidos})
            if bool(_content_files_error):
                return JSONResponse(content={"message": _content_files_error})
            else:
                return True
        except JSONDecodeError as e:
            logger.error(f"Error: file {e}")
            return JSONResponse(content={"message": f"{e}"})

