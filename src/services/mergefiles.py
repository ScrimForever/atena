from dataclasses import dataclass
import os
from utils.settings_config import settings
import json

@dataclass
class MergeFiles:


    async def merge(self) -> None:
        with open(os.path.join(os.getcwd(), settings.upload_files_bucket, "clientes.json"), 'r') as f:
            clientes = json.load(f)
        with open(os.path.join(os.getcwd(), settings.upload_files_bucket, "pedidos.json"), 'r') as f:
            pedidos = json.load(f)

        clientes_dict = {cliente['id']: cliente for cliente in clientes}


        merged = []
        for pedido in pedidos:
            client_id = pedido['client_id']
            if client_id in clientes_dict:
                merged_item = {
                    **clientes_dict[client_id],
                    **pedido
                }
                merged.append(merged_item)

        with open(os.path.join(settings.upload_files_bucket, "merged_files.json"), 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=4, ensure_ascii=False)



