import betfairlightweight
from betfairlightweight import filters
import pandas as pd
import numpy as np
import os
import json
import datetime

certs_path = '/Users/alexmorton/api-ng-ssl'

my_username = 'alexmorton'
my_password = 'RES4545breh%1'
my_app_key = 'oJnXnECanrlK156n'

trading = betfairlightweight.APIClient(username = my_username, password = my_password, app_key = my_app_key, certs = certs_path)

trading.login()


# event_types = trading.betting.list_event_types()

# sport_ids = pd.DataFrame({
#     'Sport': [event_type_object.event_type.name for event_type_object in event_types],
#     'ID': [event_type_object.event_type.id for event_type_object in event_types]
# }).set_index('Sport').sort_index()

# # Filter for just horse racing
# horse_racing_filter = betfairlightweight.filters.market_filter(text_query='Horse Racing')

# # This returns a list
# horse_racing_event_type = trading.betting.list_event_types(
#     filter=horse_racing_filter)


# # Get the first element of the list
# horse_racing_event_type = horse_racing_event_type[0]

# horse_racing_event_type_id = horse_racing_event_type.event_type.id
#print(f"The event type id for horse racing is {horse_racing_event_type_id}")

#The event type id for horse racing is 7



# Define a market filter
thoroughbreds_event_filter = betfairlightweight.filters.market_filter(
    event_type_ids=['7'],
    market_countries=['AU'],
    market_start_time={
        'to': (datetime.datetime.utcnow() + datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%TZ")
    }
)

# Print the filter
# print(thoroughbreds_event_filter)

# # Get a list of all thoroughbred events as objects
aus_thoroughbred_events = trading.betting.list_events(
    filter=thoroughbreds_event_filter
)

# # Create a DataFrame with all the events by iterating over each event object
aus_thoroughbred_events_today = pd.DataFrame({
    'Event Name': [event_object.event.name for event_object in aus_thoroughbred_events],
    'Event ID': [event_object.event.id for event_object in aus_thoroughbred_events],
    'Event Venue': [event_object.event.venue for event_object in aus_thoroughbred_events],
    'Country Code': [event_object.event.country_code for event_object in aus_thoroughbred_events],
    'Time Zone': [event_object.event.time_zone for event_object in aus_thoroughbred_events],
    'Open Date': [event_object.event.open_date for event_object in aus_thoroughbred_events],
    'Market Count': [event_object.market_count for event_object in aus_thoroughbred_events]
})

# print(aus_thoroughbred_events_today)
tb_event_ids = [event_object.event.id for event_object in aus_thoroughbred_events]
# print(tb_event_ids)
# # Define a market filter


mf_tb_flat = betfairlightweight.filters.market_filter(
    event_ids=tb_event_ids, 
    market_betting_types=["ODDS"], 
    race_types= ["Flat"] 
    )

market_catalogues = trading.betting.list_market_catalogue(
    filter=mf_tb_flat,
    max_results='300',
    sort='FIRST_TO_START'
)

# Create a DataFrame for each market catalogue
mf_tb_flat_df = pd.DataFrame({
    'Market Name': [market_cat_object.market_name for market_cat_object in market_catalogues],
    'Market ID': [market_cat_object.market_id for market_cat_object in market_catalogues],
    'Runners': [market_cat_object.runners for market_cat_object in market_catalogues],
})
# print(mf_tb_flat_df)



def process_runner_books(runner_books):
    '''
    This function processes the runner books and returns a DataFrame with the best back/lay prices + vol for each runner
    :param runner_books:
    :return:
    '''
    best_back_prices = [runner_book.ex.available_to_back[0].price
                        if runner_book.ex.available_to_back
                        else np.NAN
                        for runner_book
                        in runner_books]
    best_back_sizes = [runner_book.ex.available_to_back[0].size
                       if runner_book.ex.available_to_back
                       else np.NAN
                       for runner_book
                       in runner_books]

    best_lay_prices = [runner_book.ex.available_to_lay[0].price
                       if runner_book.ex.available_to_lay
                       else np.NAN
                       for runner_book
                       in runner_books]
    best_lay_sizes = [runner_book.ex.available_to_lay[0].size
                      if runner_book.ex.available_to_lay
                      else np.NAN
                      for runner_book
                      in runner_books]

    selection_ids = [runner_book.selection_id for runner_book in runner_books]
    # last_prices_traded = [runner_book.last_price_traded for runner_book in runner_books]
    total_matched = [runner_book.total_matched for runner_book in runner_books]
    # statuses = [runner_book.status for runner_book in runner_books]
    # scratching_datetimes = [runner_book.removal_date for runner_book in runner_books]
    # adjustment_factors = [runner_book.adjustment_factor for runner_book in runner_books]

    df = pd.DataFrame({
        'Selection ID': selection_ids,
        'Best Back Price': best_back_prices,
        'Best Back Size': best_back_sizes,
        'Best Lay Price': best_lay_prices,
        'Best Lay Size': best_lay_sizes,
        # 'Last Price Traded': last_prices_traded,
        'Total Matched': total_matched,
        # 'Status': statuses,
        # 'Removal Date': scratching_datetimes,
        # 'Adjustment Factor': adjustment_factors
    })
    return df

price_filter = betfairlightweight.filters.price_projection(
    price_data=['EX_BEST_OFFERS']
)

mcf = betfairlightweight.filters.market_filter(
    market_betting_types=["ODDS"], 
    race_types= ["Flat"],
    market_countries=['AU'],
    event_type_ids=['7'],
    market_type_codes=["WIN"],
    market_start_time={
            'to': (datetime.datetime.utcnow() + datetime.timedelta(days=0.25)).strftime("%Y-%m-%dT%TZ")
        }
    )

market_catalogues = trading.betting.list_market_catalogue(
    filter=mcf,
    max_results="40",
    sort = "FIRST_TO_START")

m_names = [market_cat_object.market_name for market_cat_object in market_catalogues]
m_ids = [market_cat_object.market_id for market_cat_object in market_catalogues]
# print(m_names, m_ids, len(m_ids))

ex_best_offers_filter = betfairlightweight.filters.ex_best_offers_overrides(rollup_model='STAKE',rollup_limit=0)
price_filter = betfairlightweight.filters.price_projection(price_data=['EX_BEST_OFFERS'],virtualise=True,ex_best_offers_overrides=ex_best_offers_filter)



market_books = trading.betting.list_market_book(
    market_ids = m_ids, 
    price_projection=price_filter    
    )

j = 0 
while j <len(market_books):
    market_book = market_books[j]
    runner_books = market_book.runners
    
    event = trading.betting.list_events(
    filter=betfairlightweight.filters.market_filter(market_ids = [market_book.market_id] )
    )

    market_cat =  trading.betting.list_market_catalogue(
    filter= betfairlightweight.filters.market_filter(market_ids = [market_book.market_id] )
    )


    print(market_book.market_id)
    print(event[0].event.name, market_cat[0].market_name)
    

    # i = 0
    # while i < len(runner_books):
    #     if runner_books[i].status == "REMOVED":
    #         runner_books.remove(runner_books[i])
    #         continue
    #     i += 1
    
    
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(process_runner_books(runner_books))
    print("\n")
    j += 1