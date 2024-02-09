from p2app.events import *
from .helper_functions import *

class RegionLevelHandler:
    def __init__(self, engine: 'Engine') -> None:
        self.connection = engine.connection

    def region_search(self, region_search_event: StartRegionSearchEvent) -> RegionSearchResultEvent | None:
        """Handles the region search event"""
        region_dict = dict()
        region_dict['name'] = region_search_event.name()
        region_dict['region_code'] = region_search_event.region_code()
        region_dict['local_code'] = region_search_event.local_code()
        region_dict = remove_none_dict(region_dict)
        where = create_where_from_dict(region_dict)
        select = Region._fields
        select = ', '.join(select)
        cursor = self.connection.execute(
            f'''SELECT {select}'''
            ''' FROM region'''
            f''' WHERE {where};''', region_dict
        )
        result = cursor.fetchall()
        cursor.close()
        if result:
            for region in result:
                yield RegionSearchResultEvent(Region(*region))
        else:
            yield from ()

    def load_region(self, load_region_event: LoadRegionEvent) -> RegionLoadedEvent:
        """Handles region loaded event"""
        region_dict = dict()
        region_dict['region_id'] = load_region_event.region_id()
        region_dict = remove_none_dict(region_dict)
        where = create_where_from_dict(region_dict)
        select = Region._fields
        select = ', '.join(select)
        cursor = self.connection.execute(
            f'''SELECT {select}'''
            ''' FROM region'''
            f''' WHERE {where};''', region_dict
        )
        result = cursor.fetchall()
        cursor.close()
        if result:
            for region in result:
                yield RegionLoadedEvent(Region(*region))
        else:
            yield ErrorEvent('No region loaded.')

    def save_new_region(self, save_new_region_event: SaveNewRegionEvent) -> RegionSavedEvent | SaveRegionFailedEvent:
        """Handles the save new region event"""
        region = save_new_region_event.region()
        region_dict = region._asdict()
        region_dict['region_id'] = get_new_unused_id('region', self.connection)
        insert = create_insert_from_dict(region_dict)
        values = create_values_from_dict(region_dict)
        try:
            cursor = self.connection.execute(
                f'''INSERT INTO region {insert}'''
                f''' VALUES {values};''', region_dict
            )
            self.connection.commit()
            cursor.close()
            yield RegionSavedEvent(Region(**region_dict))
        except Exception as e:
            yield SaveRegionFailedEvent(f'Failed to save the new country: {e}')

    def save_region(self, save_region_event: SaveRegionEvent) -> RegionSavedEvent | SaveRegionFailedEvent:
        """Handles the save region event"""
        region = save_region_event.region()
        region_dict = region._asdict()
        region_id_dict = {key:val for key, val in region_dict.items() if key == 'region_id'}
        region_code_name_dict = {key:val for key, val in region_dict.items() if key != 'region_id'}
        set_str = create_set_from_dict(region_code_name_dict)
        where = create_where_from_dict(region_id_dict)
        try:
            cursor = self.connection.execute(
                '''UPDATE region'''
                f''' SET {set_str}'''
                f''' WHERE {where}''', region_dict
            )
            self.connection.commit()
            cursor.close()
            yield RegionSavedEvent(Region(**region_dict))
        except Exception as e:
            yield SaveRegionFailedEvent(f'Failed to save the modified region: {e}')