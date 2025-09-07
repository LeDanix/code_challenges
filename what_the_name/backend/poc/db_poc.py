import time
from names_dataset import NameDataset
from pycountry import countries as py_countries

class ParserServicePoC:
    _nd: NameDataset

    def __init__(self):
        self._nd = NameDataset()
    
    def exists_name(self, name: str) -> bool:
        return bool(self._nd.search(name).get("first_name"))
    
    def get_name(self, name: str) -> bool:
        return self._nd.search(name)

    def selection_by_country(self, full_name: str, country: str) -> dict[str, list[str]]:
        # TODO Procesar todo tipo de caracteres especiales
        tokens = full_name.split()
        first_names = []
        last_names = []
        chances = []

        for token in tokens:
            result = self._nd.search(token)

            if not result:
                last_names.append(token)
                continue

            fn_countries = result.get("first_name").get("country", {})
            in_fn_country = country in fn_countries
            ln_countries = result.get("last_name").get("country", {})
            in_ln_country = country in ln_countries

            if in_fn_country and not in_ln_country:
                first_names.append(token)
                chances.append(10)
                continue

            if in_ln_country and not in_fn_country:
                last_names.append(token)
                chances.append(10)
                continue
        
            if in_ln_country and in_fn_country:
                fn_appearance_rate = result.get("first_name").get("country").get(country)
                ln_appearance_rate = result.get("last_name").get("country").get(country)

                if fn_appearance_rate > ln_appearance_rate:
                    first_names.append(token)
                    chances.append(fn_appearance_rate/(fn_appearance_rate+ln_appearance_rate))
                else:
                    last_names.append(token)
                    chances.append(ln_appearance_rate/(fn_appearance_rate+ln_appearance_rate))

        
        if len(first_names) == 0:
            first_names = None

        if len(last_names) == 0:
            last_names = None

        return {"first_names": first_names, "last_names": last_names, "chances": chances}
        
if __name__ == "__main__":
    t0 = time.perf_counter()
    service = ParserServicePoC()
    t1 = time.perf_counter()
    print(f"Does the name 'Alice' exist? {service.exists_name("Alice")}")
    t2 = time.perf_counter()

    print(f"t2 - t1: {t2 - t1}")
    print(f"t1 - t0: {t1 - t0}")

    print(f"{service.get_name("Alice")}")

    print(f"service.search('Smith', 'Spain'): {service.search('Smith', 'Spain')}")

