import mysql.connector
import json 
CONFIG_PATH = 'python-crud/config.json'

def load_config(CONFIG_PATH):
    with open(CONFIG_PATH) as file:
        config = json.load(file)
    return config

class Crud: 
    def __init__(self, config) -> None:
        self.config = config
        self.connection = self.get_connection()

    def get_connection(self):
        try: 
            connection = mysql.connector.connect(host=self.config["host"],
                                                username=self.config["username"],
                                                password=self.config["password"],
                                                database=self.config["database"])
            return connection
        except Exception as e:
            print(f"Falha ao conectar-se ao banco de dados: {e}")


    def execute_query(self, query, values): 
        try: 
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            return cursor.fetchall()
        except Exception as e: 
            print(f"Falha ao executar query: {e}")
            raise
        finally:
            cursor.close() 
        

    def get_all_clients(self):
        try:
            all_clients = self.execute_query(query="SELECT * FROM clients", 
                                            values=None)
            return all_clients
        except Exception as e: 
            print(f"Falha resgatar todos os clientes - {e}")

    
    def get_client_by_id(self, id):
        try: 
            client = self.execute_query(query="SELECT * FROM clients WHERE client_id=%s", 
                                        values=[id])
            return client
        except Exception as e:
            print(f"Falha ao resgatar cliente de id {id} - {e}")

    def insert_client(self, client): 
        try:
            self.execute_query(query="INSERT INTO clients(name, client_id) VALUES (%s, %s)",
                                values=[client["name"], client["client_id"]])
        except Exception as e:
            print(f"Falha ao inserir cliente {client} - {e}")

    
    def delete_client_by_id(self, id):
        try: 
            self.execute_query(query="DELETE FROM clients WHERE client_id=%s",
                                values=[id])
        except Exception as e:
            print(f"Falha ao deletar cliente de id {id} - {e}")


    def update_client(self, client):
        try:
            self.execute_query(query = "UPDATE clients SET name = %s WHERE client_id=%s",
                            values=[client["name"], client["client_id"]])
        except Exception as e:
            print(f"Falha atualizar cliente {client} - {e}")

    
def main():
    # Uso de exemplo:
    crud = Crud(config=load_config(CONFIG_PATH))
    all_clients = crud.get_all_clients()
    print(all_clients)

    novo_cliente = {"name": "Jorge", "client_id": 2}
    crud.insert_client(novo_cliente)
    print(crud.get_all_clients())

    one_client = crud.get_client_by_id(99)
    print(one_client)

    crud.delete_client_by_id(2)
    print(crud.get_all_clients())

    cliente_atualizado = {"name": "Joel", "client_id": 10}
    crud.update_client(cliente_atualizado)
    print(crud.get_all_clients())

if __name__ == "__main__":
    main()

    
