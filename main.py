from create_mapper import create_mapper
from collect_financial_data import collect_financial_data
from collect_price_and_volume import collect_price_and_volume
from concat_info import concat_info
from make_simple_portfolio import make_simple_portfolio

if __name__ == "__main__":
    create_mapper()
    collect_financial_data()
    collect_price_and_volume()
    concat_info()
    make_simple_portfolio(cur_date="2025-12-26")