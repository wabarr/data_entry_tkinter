import yaml

class Config():

    def __init__(self):
        with open("config.yml", "r") as configfile:
            self.options = yaml.load(configfile)
            configfile.close()

    def validate(self):
        #make sure there is an entry for records_per_page

        try:
            val = int(self.options["records_per_page"])
        except:
            raise ValueError("You must include an integer value for the 'records_per_page' option in the config.yml file.")

        valid_fieldtypes = ["text","datetime","integer","decimal"]
        for fieldname, values in self.options["fields"].iteritems():
            if not values["datatype"] in valid_fieldtypes:
                raise ValueError("datatype '%s' for fieldname '%s' is invalid. Valid datatypes include %s" % (values["datatype"] ,fieldname, ", ".join(valid_fieldtypes)))