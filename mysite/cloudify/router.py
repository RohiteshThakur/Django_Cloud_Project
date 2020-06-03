class CloudifyRouter(): 
    def db_for_read(self, model, **hints):
        "Point all operations on cloudify models to 'ratecarddb'"
        if model._meta.app_label == 'cloudify':
            return 'ratecarddb'
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all operations on cloudify models to 'ratecarddb'"
        if model._meta.app_label == 'cloudify':
            return 'ratecarddb'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in cloudify app"
        if obj1._meta.app_label == 'cloudify' and obj2._meta.app_label == 'cloudify':
            return True
        # Allow if neither is cloudify app
        elif 'cloudify' not in [obj1._meta.app_label, obj2._meta.app_label]: 
            return True
        return False
    
    def allow_syncdb(self, db, model):
        if db == 'ratecarddb' or model._meta.app_label == "cloudify":
            return False                            # we're not using syncdb on our legacy database
        else:                                       # but all other models/databases are fine
            return True
