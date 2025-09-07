import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import statistics
from typing import Dict, Union, Any

from names_dataset import NameDataset
from app.model.contants import NameSchema
from app.core.logging_config import LoggerManager


class Posibilities:
    "Percentage"
    TOKEN_NOT_FOUND_LN = 50
    TOKEN_FOUND_FN = 100
    TOKEN_FOUND_LN = 100
    PYLANCE_WARNING_WORKRND = 100


class ParserService:
    _nd: NameDataset
    log = LoggerManager().get_logger(__name__)

    def __init__(self):
        self._nd = NameDataset()
        
    def exists_name(self, word: str) -> bool:
        return bool(self._nd.search(word).get(NameSchema.first_name))

    def search(self, full_name: str, country: str) -> Dict[str, Union[str, float]]:
        first_name: list[str] = []
        last_name: list[str] = []
        chance: list[int] = []

        for token in self.__proccess_raw_name(full_name=full_name):
            self.log.debug(f"token: {token}")
            country_deep_search = self.__selection_by_country(name_appearance_data=self.__controlled_search(token), country=country)

            self.log.debug(f"country_deep_search: {country_deep_search}")
            if country_deep_search.get(NameSchema.first_name):
                first_name.append(token)
                chance.append(country_deep_search.get(NameSchema.chance, Posibilities.PYLANCE_WARNING_WORKRND))

            if country_deep_search.get(NameSchema.last_name):
                last_name.append(token)
                chance.append(country_deep_search.get(NameSchema.chance, Posibilities.PYLANCE_WARNING_WORKRND))
        
        return {NameSchema.first_name: ' '.join(first_name), 
                NameSchema.last_name: ' '.join(last_name), 
                NameSchema.chance: statistics.mean(chance)}

    def __proccess_raw_name(self, full_name: str):
        # TODO Procesar todo tipo de caracteres especiales
        tokens = full_name.split()
        return tokens

    def __controlled_search(self, token: str) -> Dict:
        try:
            return self._nd.search(token)
        except Exception as e:
            self.log.warning(f"The token was not found. Error {e}. Returning empty dict...")
            return {}

    def __selection_by_country(self, name_appearance_data: dict, country: str) -> Dict[str, Any]:
        if len(name_appearance_data) == 0:
            self.log.debug(f"Empty data in 'name_appearance_data' var")
            return {NameSchema.first_name: False, NameSchema.last_name: True, NameSchema.chance: Posibilities.TOKEN_NOT_FOUND_LN}
        
        in_fn_country = self.__country_filtering_fn(name_appearance_data=name_appearance_data, country=country)
        in_ln_country = self.__country_filtering_ln(name_appearance_data=name_appearance_data, country=country)

        self.log.debug(f"in_fn_country | in_ln_country: {in_fn_country} | {in_ln_country}")
            
        if in_fn_country and not in_ln_country:
            self.log.debug(f"AQUI 1")
            return {NameSchema.first_name: True, NameSchema.last_name: False, NameSchema.chance: Posibilities.TOKEN_FOUND_FN}

        if in_ln_country and not in_fn_country:
            self.log.debug(f"AQUI 2")
            return {NameSchema.first_name: False, NameSchema.last_name: True, NameSchema.chance: Posibilities.TOKEN_FOUND_LN}
    
        if in_ln_country and in_fn_country:
            fn_appearance_rate = name_appearance_data.get(NameSchema.first_name, {}).get(NameSchema.country, {}).get(country, 0.0)
            ln_appearance_rate = name_appearance_data.get(NameSchema.last_name, {}).get(NameSchema.country, {}).get(country, 0.0)

            if fn_appearance_rate >= ln_appearance_rate:
                self.log.debug(f"AQUI 3")
                return {NameSchema.first_name: True, NameSchema.last_name: False, NameSchema.chance: fn_appearance_rate * 100/(fn_appearance_rate+ln_appearance_rate)}
            self.log.debug(f"AQUI 4")
            return {NameSchema.first_name: False, NameSchema.last_name: True, NameSchema.chance: ln_appearance_rate * 100/(fn_appearance_rate+ln_appearance_rate)}

        return {NameSchema.first_name: False, NameSchema.last_name: True, NameSchema.chance: Posibilities.TOKEN_NOT_FOUND_LN}  # Not found in name so, probabily is a last name

    def __country_filtering_fn(self, name_appearance_data: dict, country: str):
        try:
            fn_countries = name_appearance_data.get(NameSchema.first_name, {}).get(NameSchema.country, {})
            return country in fn_countries
        except AttributeError as e:
            self.log.warning(f"Token doesn't appear into First Names. Error: {e}")
            return False
    
    def __country_filtering_ln(self, name_appearance_data: dict, country: str):
        try:
            ln_countries = name_appearance_data.get(NameSchema.last_name, {}).get(NameSchema.country, {})
            self.log.debug(f"ln_countries: {ln_countries} | country: {country}")
            return country in ln_countries
        except AttributeError as e:
            self.log.warning(f"Token doesn't appear into Last Names. Error: {e}")
            return False


if __name__ == "__main__":
    service = ParserService()
    # print(service._nd.search("Azor"))
    service.search("Daniel Saiz", "Spain")