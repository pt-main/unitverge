import exceptions as exc

class Utils:
    # verification for-C data function
    @staticmethod
    def check_c_available(data, allowed = []):
        # check data type
        if isinstance(data, tuple(allowed)): 
            return data # verefication compleate
        else: # if data type not in allowed types
            # raise unknon type exception
            raise exc.UnknownType(f"Unknown type: [ {data}:{type(data)} ]")