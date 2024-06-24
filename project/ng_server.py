import requests
import json
import os


class NGWServer:
    url_upload = os.getenv('NGW_UPLOAD_URL', 'http://10.7.246.199:8080/api/component/file_upload/')
    url_resource = os.getenv('NGW_RESOURCE_URL', 'http://10.7.246.199:8080/api/resource/')
    auth = (os.getenv('NGW_USER'), os.getenv('NGW_PASSWORD'))
    parent_id = os.getenv('NGW_RESOURCE_DIR')
    headers = {'Accept': '*/*'}

    @staticmethod
    def upload_file(file_path):
        if not os.path.exists(file_path):
            raise Exception('NGWServer (upload_file): Файл не найден')

        files = {'file': open(file_path, 'rb')}
        response = requests.post(
            NGWServer.url_upload,
            files=files
        )

        if response.status_code == 200:
            return response.json()['upload_meta'][0]
        else:
            raise Exception('NGWServer (upload_file): Ошибка при загрузке файла:<br>', response.json())

    @staticmethod
    def create_resource(file_meta, filename=None):
        if not file_meta:
            raise Exception('NGWServer (create_resource): Не указаны мета-данные файла')

        data = {
            "resource": {
                "cls": "vector_layer",
                "description": "test geojson upload",
                "display_name": filename or file_meta['name'],
                "parent": {"id": NGWServer.parent_id},
            },
            "vector_layer": {
                "source": {
                    "encoding": "utf-8",
                    "id": file_meta['id'],
                    "mime_type": file_meta['mime_type'],
                    "name": file_meta['name'],
                    "size": file_meta['size'],
                    "skip_errors": True,
                    "fix_errors": "LOSSY",
                },
                "srs": {"id": 3857}
            }
        }

        response = requests.post(
            NGWServer.url_resource,
            auth=NGWServer.auth,
            headers=NGWServer.headers,
            data=json.dumps(data)
        )

        if response.status_code == 201:
            return response.json()['id']
        else:
            raise Exception("NGWServer (create_resource): Ошибка при создании ресурса:<br>", response.json())

    @staticmethod
    def create_qgis_style(self, file_meta, layer_id, style_name):
        data = {
            "qgis_vector_style": {
                "file_upload": {
                    "id": file_meta['id'],
                    "mime_type": file_meta['mime_type'],
                    "size": file_meta['size']
                }
            },
            "resource": {
                "cls": "qgis_vector_style",
                "display_name": style_name,
                "parent": {
                    "id": layer_id
                }
            }
        }
        response = requests.post(
            self.url_resource,
            auth=self.auth,
            headers=NGWServer.headers,
            data=json.dumps(data)
        )

        if response.status_code == 201:
            return response.json()['id']
        else:
            raise Exception("NGWServer (create_qgis_style): Ошибка при создании стиля:<br>", response.json())

    def get_resource(self, resource_id):
        url = f"{self.url_resource}{resource_id}"
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("NGWServer (get_resource): Ошибка при получении ресурса:<br>", response.json())

    # def update_resource(self, resource_id, style_id):
    #     headers = {'Accept': '*/*', 'Content-Type': 'application/json'}
    #     resource = self.get_resource(resource_id)
    #     print(resource)
    #
    # def get_webmap(self, webmap_id):
    #     url = f"{self.url_resource}{webmap_id}"
    #     response = requests.get(url, auth=self.auth)
    #     if response.status_code == 200:
    #         return response.json()['webmap']
    #     else:
    #         raise Exception("Ошибка при получении веб-карты", response.status_code)
    #
    # def update_webmap(self, webmap_id):
    #     current_webmap = self.get_webmap(webmap_id)
    #     current_layers = current_webmap['root_item']['children']
    #
    #     new_layer = {
    #         'display_name': 'жопа',
    #         'draw_order_position': None,
    #         'item_type': 'layer',
    #         'layer_adapter': 'image',
    #         'layer_enabled': True,
    #         'layer_identifiable': True,
    #         'layer_max_scale_denom': None,
    #         'layer_min_scale_denom': None,
    #         'layer_style_id': 40,
    #         'layer_transparency': None,
    #         'legend_symbols': None,
    #         'style_parent_id': 37
    #     }
    #
    #     current_layers.append(new_layer)
    #
    #     payload = {'webmap': {'root_item': {'item_type': 'root', 'children': current_layers}}}
    #     url = f"{self.url_resource}{webmap_id}"
    #     response = requests.put(url, json=payload, auth=self.auth)
    #     if response.status_code == 200:
    #         print("Веб-карта успешно обновлена")
    #     else:
    #         raise Exception("Ошибка при обновлении веб-карты", response.status_code)
    #
    # @staticmethod
    # def rename_id_field(file):
    #     """
    #     Переименование поля id в id_ogr
    #     :param file: Путь к файлу
    #     :return: Путь к файлу
    #     """
    #     if not file:
    #         raise Exception('NGToolbox (rename_id_field): Не указан файл для переименования поля id')
    #
    #     if not os.path.exists(file):
    #         raise Exception('NGToolbox (rename_id_field): Файл не найден')
    #
    #     with open(file, 'r') as f:
    #         content = f.read()
    #         content = content.replace('"id":', '"id_ogr":')
    #
    #     with open(file, 'w') as f:
    #         f.write(content)
    #
    #     return file
