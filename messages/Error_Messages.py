
class Errors:
    @staticmethod
    def db_error(error_type, model_type):
        db_errors = {
            'insert': 'an error occurred while inserting ',
            'update': 'an error occurred while updating ',
            'delete': 'an error occurred while deleting',
        }
        return db_errors[error_type] + model_type

    @staticmethod
    def no_results(model_type):
        return 'No results were found for ' + model_type

    @staticmethod
    def no_accounts(usrname):
        return 'No accounts were found for user ' + usrname
