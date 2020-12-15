class Sentence:
    ''' '''

class CreateDatabase(Sentence):
    def __init__(self, name, ifNotExistsFlag, OrReplace, OwnerMode):
        self.name = name
        self.ifNotExistsFlag = ifNotExistsFlag
        self.OrReplace = OrReplace
        self.OwnerMode = OwnerMode

class ShowDatabases(Sentence):
    ''''''

class DropDatabase(Sentence):
    def __init__(self, name, ifExistsFlag):
        self.name = name
        self.ifExistsFlag = ifExistsFlag

class DropTable(Sentence):
    def __init__(self, name):
        self.name = name

class Use(Sentence):
    def __init__(self, name):
        self.name = name

class AlterDatabaseRename(Sentence):
    def __init__(self, oldname,newname):
        self.oldname = oldname
        self.newname = newname

class AlterDatabaseOwner(Sentence):
    def __init__(self, name, newowner):
        self.name = name
        self.newowner = newowner

class AlterTableDropColumn(Sentence):
    def __init__(self, table, column):
        self.table = table
        self.column = column

class AlterTableAddConstraintUnique(Sentence):
    def __init__(self, table, constraint, column):
        self.table = table
        self.constraint = constraint
        self.column = column

class AlterTableAddForeignKey(Sentence):
    def __init__(self, table, column, rel_table, rel_column):
        self.table = table
        self.column = column
        self.rel_table = rel_table
        self.rel_column = rel_column
        
class AlterTableAlterColumnSetNull(Sentence):
    def __init__(self, table, column, null):
        self.table = table
        self.column = column
        self.null = null

class AlterTableAlterColumnType(Sentence):
    def __init__(self, table, column, newtype):
        self.table = table
        self.column = column
        self.newtype = newtype # type [type,length] or type = [type] 

class AlterTableDropConstraint(Sentence):
    def __init__(self, table, constraint):
        self.table = table
        self.constraint = constraint

class Insert(Sentence):
    def __init__(self, table, columns, values):
        self.table = table
        self.columns = columns
        self.values = values

class InsertAll(Sentence):
    def __init__(self, table, values):
        self.table = table
        self.values = values

class Delete(Sentence):
    def __init__(self, table, expression):
        self.table = table
        self.expression = expression

class Truncate(Sentence):
    def __init__(self, tables):
        self.tables = tables

class Update(Sentence):
    def __init__(self, table, values, expression):
        self.table = table
        self.values = values #values = [value1,value2,...,valuen] -> value = [id,expression]  
        self.expression = expression

class CreateType(Sentence):
    def __init__(self, name, expressions):
        self.name = name
        self.expressions = expressions #expressions = [expression1,expression2,...,expressionn]