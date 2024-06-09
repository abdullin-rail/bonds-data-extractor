from datetime import datetime
from decimal import Decimal

import requests

from models.bond import Bond


class MoexService:
    def __init__(self):
        self.cached_data = None
        self.moex_bonds_base_url = "https://iss.moex.com/iss/engines/stock/markets/bonds/boards/"

    def get_boards(self) -> list[str]:
        return [
            "TQOB", # Т+ Гособлигации
            "TQCB", # Корпоративные

            # "TQOS"
            # "TQNO",
            # "TQOV",
            #
            # "TQNB",
            # "TQUS",
            #
            # "TQRD",
            # "TQIR",
            # "TQOD",
            # "TQUD",
            # "TQIU",
        ]

    def get_bonds(self, board_id: str) -> list[Bond]:
        columns = self._get_columns_list()
        columns_str = ",".join(columns)
        url = self.moex_bonds_base_url + f"{board_id}/securities.json?iss.meta=off&iss.only=securities&securities.columns={columns_str}"
        response = requests.get(url)
        response.raise_for_status()
        response_json = response.json()

        securities = response_json['securities']
        columns = securities['columns']
        data = securities['data']

        mapped_data = []
        for row in data:
            item = {columns[i]: row[i] for i in range(len(columns))}
            mapped_data.append(item)

        bonds = [self._bond_from_moex_data(bond_data) for bond_data in mapped_data]
        return bonds

    def get_bond(self, isin, board_id: str) -> Bond:
        # print("board_id ", board_id)
        # print("isin ", isin)
        columns = self._get_columns_list()
        columns_str = ",".join(columns)
        url = self.moex_bonds_base_url + f"{board_id}/securities.json?iss.meta=off&iss.only=securities&securities.columns={columns_str}" # + \
            # f"&//data[SECID={isin}]"

        print(url)

        try:
            if self.cached_data == None:
                response = requests.get(url)
                response.raise_for_status()

                # print("response ", response)
                # Разбор полученных данных
                self.cached_data = response.json()
            # print("data ", self.cached_data)

            # print("isin ", isin)

            # Здесь нужно найти правильный путь к цене в ответе, это зависит от структуры данных
            # Например, это может выглядеть так:
            bond_info = self.cached_data['securities']['data']

            # print("bond_info ", bond_info)

            # print("bond_info ", bond_info)
            bond_price = next((item[1] for item in bond_info if item[0] == isin), None)

            coupon_period = next((item[2] for item in bond_info if item[0] == isin), None)

            end_date = next((item[3] for item in bond_info if item[0] == isin), None)
            face_value = next((item[4] for item in bond_info if item[0] == isin), None)


            return bond_price, coupon_period, end_date, face_value

        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6

    @staticmethod
    def _get_columns_list() -> list[str]:
        return [
            "SECID", # ISIN
            "BOARDID",
            "PREVWAPRICE", #  last price
            "COUPONPERIOD", # coupon period in days
            "COUPONPERCENT", # Coupon percent
            "MATDATE", # Maturiy date
            "LOTVALUE", # Nominal price
            "FACEUNIT", # Currency
            "BUYBACKPRICE", # buy back price
            "BUYBACKDATE", # buy back date
            "OFFERDATE", # offer date
            "SECNAME" # name
        ]

    @staticmethod
    def _bond_from_moex_data(bond_data: dict) -> Bond:
        maturity_date = None
        if bond_data.get("MATDATE"):
            try:
                maturity_date = datetime.strptime(bond_data["MATDATE"], "%Y-%m-%d")
            except ValueError:
                pass

        offer_date = None
        if bond_data.get("OFFERDATE"):
            try:
                offer_date = datetime.strptime(bond_data["OFFERDATE"], "%Y-%m-%d")
            except ValueError:
                pass

        buy_back_date = None
        if bond_data.get("BUYBACKDATE"):
            try:
                buy_back_date = datetime.strptime(bond_data["BUYBACKDATE"], "%Y-%m-%d")
            except ValueError:
                pass

        return Bond(
            isin=bond_data.get("SECID"),
            board_id=bond_data.get("BOARDID"),
            name=bond_data.get("SECNAME"),
            coupon_rate=Decimal(bond_data["COUPONPERCENT"]) if bond_data.get("COUPONPERCENT") else None,
            nominal_price=Decimal(bond_data["LOTVALUE"]) if bond_data.get("LOTVALUE") else None,
            current_price_percent=Decimal(bond_data["PREVWAPRICE"]) if bond_data.get("PREVWAPRICE") else None,
            payments_interval=int(bond_data["COUPONPERIOD"]) if bond_data.get("COUPONPERIOD") else None,
            maturity_date=maturity_date,
            currency=bond_data["FACEUNIT"] if bond_data.get("FACEUNIT") else None,
            buy_back_date=buy_back_date,
            offer_date=offer_date,
            buy_back_price=Decimal(bond_data["BUYBACKPRICE"]) if bond_data.get("BUYBACKPRICE") else None,
        )