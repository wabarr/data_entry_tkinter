import yaml

class Config():

    def __init__(self):
        with open("config.yml", "r") as configfile:
            self.options = yaml.load(configfile)
            configfile.close()

    def validate(self):
        valid_fieldtypes = ["text","datetime","integer","decimal"]
        for fieldname, values in self.options["fields"].items():
            if not values["datatype"] in valid_fieldtypes:
                raise ValueError("datatype '%s' for fieldname '%s' is invalid. Valid datatypes include %s" % (values["datatype"] ,fieldname, ", ".join(valid_fieldtypes)))