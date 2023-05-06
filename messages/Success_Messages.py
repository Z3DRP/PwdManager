
class Success:
    @staticmethod
    def db_success(operation_type, model_type):
        operations = {
            'insert': ' has been inserted successfully',
            'insert_p': 'have been inserted successfully',
            'update': ' has been updated successfully',
            'update_p': 'have been updated successfully',
            'delete': 'has been deleted successfully',
            'delete_p': 'have been deleted successfully',
        }
        return model_type + operations[operation_type]
