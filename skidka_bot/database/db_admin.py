import ydb
from typing import List

from config import configuration
from exception import ConnectionFailure

class YDBClient:
    def __init__(self):
        self.config = configuration
        self.driver = self.create_driver()
        self.session = self.driver.table_client.session().create()  
        # self.session.execute_scheme(
        #     """                
        #         CREATE table packages (
        #             user_id Uint64,                   
        #             package_url Utf8,
        #             package_name Utf8,
        #             brand_name Utf8,
        #             old_price Uint64,
        #             new_price Uint64,
        #             PRIMARY KEY (package_url)
        #         )
        #         """
            
        # )

    def create_driver(self) -> ydb.Driver:
        driver = ydb.Driver(endpoint=self.config.endpoint, database=self.config.database)

        try:
            driver.wait(timeout=5)
        except Exception:
            raise ConnectionFailure(driver.discovery_debug_details())

        return driver


    @property
    def table_client(self) -> ydb.TableClient:
        return self.driver.table_client


    def bulk_upsert(self, rows: List, column_types: ydb.BulkUpsertColumns):
        self.table_client.bulk_upsert(self.config.full_path, rows, column_types)


    def execute(self, query, params = None):
        return self.session.transaction(ydb.SerializableReadWrite()).execute(
            query,
            params,
            commit_tx=True,
        )


    def add_new_user(self, user_id, user_name, date):          
        self.execute(f"INSERT INTO users (user_id, user_name, connect_date) VALUES({user_id}, '{user_name}', DateTime::MakeDatetime(DateTime::FromMilliseconds({date})));")

    
    def add_item_info(self, user_id, package_url, package_name, brand_name, old_price):
        self.execute(f"INSERT INTO packages (user_id, package_url, package_name, brand_name, old_price) VALUES({user_id}, '{package_url}', '{package_name}', '{brand_name}', {old_price})")    

    
    def check_user_in_db(self, user_id):    
        result_set = self.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")        
        return bool(result_set[0].rows)

    
    def check_packages(self, user_id):
        return self.execute(
            f"SELECT package_url, package_name, brand_name, new_price, old_price FROM packages WHERE user_id = {user_id}"
            )[0].rows
        

    
    def delete_item_from_db(self, package_url):
        self.execute(f"DELETE from packages WHERE package_url = {package_url}")

    
    def check_prices(self):        
        return self.execute("SELECT user_id, old_price, new_price, package_url, package_name FROM packages")[0].rows

    
    def check_new_price(self, user_id):
        return self.execute(f"SELECT new_price FROM packages WHERE user_id = {user_id}")[0].rows

    
    def take_url(self):
        return self.execute("SELECT package_url from packages")[0].rows


    def add_discount(self, user_id, discount):
        self.execute(f"UPDATE users SET discount = '{discount}' WHERE user_id = {user_id}")


    def add_new_price(self, price_for_update, url_for_update):
        self.execute(f"UPDATE packages SET new_price = {price_for_update} WHERE package_url = '{url_for_update}'")
    

    def update_old_price(self, price_for_update, url_for_update):
        self.execute(f"UPDATE packages SET old_price = {price_for_update} WHERE package_url = '{url_for_update}'")


    def delete_all_items(self, user_id):
        self.execute(f"DELETE FROM packages WHERE user_id ={user_id}")


ydb_client = YDBClient()
