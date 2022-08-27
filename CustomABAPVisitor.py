
from antlr4 import *
from ABAPParser import ABAPParser as rules 
from ABAPLexer import ABAPLexer
from ABAPVisitor import ABAPVisitor


class CustomABAPVisitor(ABAPVisitor):
    def __init__(self, outputFile):
        self.outputFile = outputFile
        self.indent = 0
        self.output("Here is your translated code-")
        
    def up(self):self.indent+=4

    def down(self):self.indent-=4

    def output(self, text):self.outputFile.write(" "*self.indent + text+".\n")

    def visitProgram(self, ctx:rules.ProgramContext):
        self.visitChildren(ctx)

    def visitProgramName(self, ctx:rules.ProgramNameContext):
        self.output("Create a "+ctx.getChild(0).getText()+" named "+self.visit(ctx.id_()))
        self.up()
    
    def visitBlock(self, ctx:rules.BlockContext):
        self.visitChildren(ctx)
        self.down()

    def visitClassHeader(self, ctx:rules.ClassHeaderContext):
        self.output(("Declare" if ctx.DEFINITION()  else "Implement" )+ " a class named "+self.visit(ctx.id_()))
        self.up()

    def visitEventHeader(self, ctx:rules.EventHeaderContext):
        self.output("Start the event "+ctx.getText())
        self.up()
     
    def visitSectionHeader(self, ctx:rules.SectionHeaderContext):
        self.output("Start the "+self.visit(ctx.id_())+" Section")
        self.up()

    def visitSectionBlock(self, ctx:rules.SectionBlockContext):
        self.visitChildren(ctx)
        self.down()

    def visitMethodHeader(self, ctx:rules.MethodHeaderContext):
        self.output("Declare a method named "+self.visit(ctx.id_()))
        self.up()

    def visitMethodBlock(self, ctx:rules.MethodBlockContext):
        self.visitChildren(ctx)
        self.down()

    def visitStatement(self, ctx:rules.StatementContext):
        statement = ctx.getChild(0)   
        if isinstance(statement, rules.ExpressionContext):self.output(self.expressionStatement(statement))

        elif isinstance(statement, rules.KeywordStatementContext):self.output(self.visit(statement))

        elif isinstance(statement, rules.BlockStatementContext):(self.visitBlockStatement(statement))

    def expressionStatement(self, ctx):
        if hasattr(ctx, 'bop') and ctx.bop:
            
            l = self.visitExpression(ctx.children[0])
            r = self.visitExpression(ctx.children[2])
            
            if ctx.bop.text in {"=>","->"}:return "Call method ("+r+") on "+l
            elif ctx.bop.text == "=": return "Set " +l+ " equal to "+r

        elif isinstance(ctx.children[0], rules.MethodCallContext):
            return "Call method "+ self.visitExpression(ctx)
    
        return self.visitExpression(ctx)
    
    def visitIfBlock(self, ctx: rules.IfBlockContext):
        self.visitChildren(ctx)
        self.output("End of if block")

    def visitTryBlock(self, ctx: rules.TryBlockContext):
        self.visitChildren(ctx)
        self.output("End of try block")

    def visitLoopBlock(self, ctx: rules.LoopBlockContext):
        self.visitChildren(ctx)
        self.output("End of loop")
    

    def visitIf_(self, ctx: rules.If_Context):
        self.output("If " + self.visit(ctx.expression()))
        self.up()
        self.visit(ctx.statementList())
        self.down()

    def visitElif_(self, ctx: rules.Elif_Context):
        self.output("Else if " + self.visit(ctx.expression()))
        self.up()
        self.visit(ctx.statementList())
        self.down()

    def visitElse_(self, ctx: rules.Else_Context):
        self.output("Else")
        self.up()
        self.visit(ctx.statementList())
        self.down()

    def visitTry_(self, ctx: rules.Try_Context):
        self.output("Try")
        self.up()
        self.visit(ctx.statementList())
        self.down()

    def visitCatch_(self, ctx: rules.Catch_Context):
        self.output("Catch "+self.visit(ctx.expression()))
        self.up()
        self.visit(ctx.statementList())
        self.down()

    def visitLoop(self, ctx: rules.LoopContext):
        self.output("Loop at table "+self.visit(ctx.declaration()))
        self.up()
        self.visit(ctx.statementList())
        self.down()

    def visitDo_(self, ctx: rules.Do_Context):
        self.output("Repeat "+self.visit(ctx.times().getText())+" times.")
        self.up()
        self.visit(ctx.statementList())
        self.down()

    def visitKeywordStatement(self, ctx:rules.KeywordStatementContext):
            if ctx.COLON():
                keywords = self.visitKeywords(ctx.keywords(), True)
                return keywords +" "+ self.readStatementGroup(ctx.declarations(), rules.DeclarationContext, currLineCount = len(keywords) +1 )
            else:
                keywords = self.visitKeywords(ctx.keywords())
                return keywords +" "+ self.visitDeclaration(ctx.declaration())

    #helper method to help with visiting rules like expressions
    def readStatementGroup(self, ctx, ctxtype, numbered = False, currLineCount = 0):
        text=[]
        joinStr = "\n" + " "*(self.indent + currLineCount) if currLineCount>0 else " "
        if len(ctx.children) == 1: return self.visit(ctx.children[0])
        if numbered: 
            for i in range(len(ctx.children)): 
                child = ctx.children[i]
                if isinstance(child, ctxtype): text.append(str(i+1) + ")"+ self.visit(child))
            return joinStr.join(text)
        else:
            joinStr = "," + joinStr
            count = 0
            for child in ctx.children: 
                if isinstance(child, ctxtype): 
                    text.append(self.visit(child))
                    count += 1
            return joinStr.join(text)

    
    def visitKeywords(self, ctx:rules.KeywordsContext, isColon = False):
        keywords = ctx.getText().upper()
        keywords = keywords + ":" if isColon else keywords
        keywordsdict ={
            "DATA"              :"Declare data called",
            "DATA:"             :"Declare the following data-",
            "CLASS-DATA"        :"Declare class data called",
            "CLASS-DATA:"       :"Declare the following class data-",
            "CLASS-METHODS"     :"Declare class method called",
            "CLASS-METHODS:"    :"Declare the following class methods-",
            "MESSAGE"           :"Write message",
            "SELECT"            :"Select",
            "SELECT:"           :"Select the following-",
            "TYPE"              :"",
            "TYPES:"            :"Declare the following-",
            "SETHANDLER"        :"Set event handler",
            "READTABLE"         :"Read table called",
            "READTABLE:"        :"Read the following tables-",
            "CLEAR"             :"Clear table called",
            "CLEAR:"            :"Clear the following tables-",
        }
        return keywordsdict[keywords]
        
        

    def visitDeclaration(self, ctx: rules.DeclarationContext):
        subject = self.visitSubject(ctx.subject())
        settings = "" if ctx.settings() is None else " " +self.visitSettings(ctx.settings())
        return subject + settings

    def visitSubject(self, ctx:rules.SubjectContext):
        if ctx.getText() == "*" : return "all fields"
        else: return self.visit(ctx.getChild(0))


    def visitStructure(self, ctx: rules.StructureContext):
        return "structured type "+ self.visit(ctx.beginStructure()) + " with components "+self.visit(ctx.structureItems())

    def visitBeginStructure(self, ctx: rules.BeginStructureContext):
        return self.visit(ctx.id_())

    def visitStructureItems(self, ctx: rules.StructureItemsContext):
        return self.readStatementGroup(ctx, (rules.DeclarationContext, rules.StructureContext))
    
    def visitSettings(self, ctx:rules.SettingsContext):
        return self.readStatementGroup(ctx, rules.SettingContext)

    def visitSetting(self, ctx:rules.SettingContext):
        return self.visitChildren(ctx)
    def visitFlag(self, ctx:rules.FlagContext):
        return self.visitChildren(ctx)

    def visitSimpleSetting(self, ctx:rules.SimpleSettingContext):
        return self.visitChildren(ctx)

    def visitType(self, ctx:rules.TypeContext):
        dataType = self.visit(ctx.dataType()) if ctx.dataType() else self.visit(ctx.literal())
        return dataType

    def visitPointer(self, ctx:rules.PointerContext):
        text = ""
        if ctx.TYPE():text = "of type"
        if ctx.LIKE():text = "like"
        if ctx.REF():text = "reference pointing to"
        return text

    def visitDataType(self, ctx:rules.DataTypeContext):
        return self.visitChildren(ctx)

    def visitClassOrInterface(self, ctx:rules.ClassOrInterfaceContext):
        return "of type "+self.visit(ctx.id_())

    def visitPrimitives(self, ctx:rules.PrimitivesContext):
        return "of type " +self.visit(ctx.getText().lower())


    def visitTable(self, ctx:rules.TableContext):
        text = "as a"
        if ctx.id_(): text+= " "+self.visit(ctx.id_())
        text+= " table "+self.visit(ctx.dataType())
        return text


    # Visit a parse tree produced by rules#importExportChanging.
    def visitImportExportChanging(self, ctx:rules.ImportExportChangingContext): 
        text = ""
        if ctx.IMPORTING():text+= "with input"
        elif ctx.EXPORTING():text+= "with output"
        elif ctx.CHANGING():text+= "that changes"
        if len(ctx.children[1].children)>1: text+="s"

        return text + " " + self.visit(ctx.getChild(1))

    def visitParams(self, ctx:rules.ParamsContext):
        return self.readStatementGroup(ctx, rules.ParamContext, numbered = True)


    def visitParam(self, ctx:rules.ParamContext):
        text = "optional parameter " if ctx.OPTIONAL() else ""
        text += self.visit(ctx.id_())
        if ctx.type_(): text += " "+ self.visit(ctx.type_())
        if ctx.DEFAULT(): text += " that defaults to "+ ctx.literal().getText()
        return text
        
    def visitWith(self, ctx:rules.WithContext):
        withthing = "with"
        if ctx.key():
            withthing += " a"
            if ctx.keytype(): withthing+= " "+ self.visit(ctx.keytype())
            withthing+= " " + self.visit(ctx.key())
        return withthing

    def visitKeytype(self, ctx:rules.KeytypeContext):
        types = []
        for child in ctx.children: types.append(child.getText().upper()) 
        return ", ".join(types)

    def visitKey(self, ctx:rules.KeyContext):
        key = "key"
        if ctx.id_(): key += " called "+ self.visit(ctx.id_())
        if ctx.alias(): key += ", "+self.visit(ctx.alias().id_())
        if ctx.components(): key += ", "+self.visit(ctx.components())
        return key

    def visitAlias(self, ctx:rules.AliasContext):
        return "with alias "+self.visitChildren(ctx)

    def visitComponents(self, ctx:rules.ComponentsContext):
        return "with components "+self.readStatementGroup(ctx.expressions(), rules.ExpressionContext, numbered = True)

    def visitIndex(self, ctx:rules.IndexContext):
        return "at row number "+ self.visit(ctx.id_())


    def visitRaising(self, ctx:rules.RaisingContext):
        return self.visitChildren(ctx)


    def visitFrom(self, ctx:rules.FromContext):
        return "from "+ self.visit(ctx.id_())


    def visitTo(self, ctx:rules.ToContext):
        return "to "+ self.visit(ctx.id_())


    def visitWhere(self, ctx:rules.WhereContext):
        return "where " + self.visitChildren(ctx)


    def visitUsing(self, ctx:rules.UsingContext):
        if ctx.key():
            return "use a "+self.visit(ctx.key())


    def visitInto(self, ctx:rules.IntoContext):
        text=[]
        for child in ctx.children:
            if isinstance(child, TerminalNode):text.append(child.getText())
            else:text.append(self.visit(child))
        return " ".join(text)


    def visitAssigning(self, ctx:rules.AssigningContext):
        return "assign the content to "+ self.visit(ctx.fieldSymbol().id_())

    def visitReference(self, ctx:rules.ReferenceContext):
        return "create a reference to the content in reference table "+self.visit(ctx.into().expression())

    def visitComparing(self, ctx:rules.ComparingContext):
        return "compare "+self.visit(ctx.transportObjects())+" from the content and transport them into the work area"

    def visitTransporting(self, ctx:rules.TransportingContext):
        return "transport "+self.visit(ctx.transportObjects())+" from the content into the work area"

    def visitTransportObjects(self, ctx:rules.TransportObjectsContext):
        if ctx.expressions(): return self.visit(ctx.expressions())
        else: return ctx.getChild(0).getText() +" "+ ctx.getChild(1).getText()

    def visitFieldSymbol(self, ctx:rules.FieldSymbolContext):
        text = ""
        if(ctx.FIELDSYMBOL()): text += "field symbol "
        return text +self.visit(ctx.id_())

    def visitFor_(self, ctx:rules.For_Context):
        if ctx.EVENT():
            return "for event "+ self.visit(ctx.id_()[0]) + " of reference " + self.visit(ctx.id_()[1])
        return "for " + ctx.expression()[0].getText()

    def visitDisplay(self, ctx:rules.DisplayContext):
        return "like "+self.visit(ctx.type_())

    def visitExpressions(self, ctx:rules.ExpressionsContext):
        return self.readStatementGroup(ctx, rules.ExpressionContext)
    
    def visitExpression(self, ctx:rules.ExpressionContext):
        if hasattr(ctx,'bop') and ctx.bop:
            l = self.visitExpression(ctx.children[0])
            r = self.visitExpression(ctx.children[2])

            if ctx.bop.text != "=" :
                if not isinstance(ctx.children[0].children[0], rules.PrimaryContext):l = "(" + l + ")"
                if not isinstance(ctx.children[2].children[0], rules.PrimaryContext):r = "(" + r + ")"


            operators = {
            '='     :""+l+" = "+r,
            '<>'    :""+l+" is not equal to "+r+"",
            '=>'    :"result of method "+r+", on " +l+"",
            '->'    :"result of instance method "+r+" on " +l+"",
            '+'     :""+l+" + "+r+"",
            '-'     :""+l+" - "+r+"",
            '*'     :""+l+" x "+r+"",
            '/'     :""+l+" / "+r+"",
            'MOD'   :""+l+" modulus "+r,
            'NOT'   :" not "+r,
            'AND'   :""+l +" and "+ r+"",
            'OR'    :""+l +" or "+ r+"",
            '<'     :""+l+" is less than "+r+"",
            '>'     :""+l+" is greater than "+r+"",
            '<='    :""+l+" is less than or equal to "+r+"",
            '>='    :""+l+" is greater than or equal to "+r+"",
            '*='    :"Set "+ l+" equal to => "+l+" multiplied by "+r,
            '+='    :"Set "+ l+" equal to => "+l+" plus "+r,
            '-='    :"Set "+ l+" equal to => "+l+" minus "+r,
            '/='    :"Set "+ l+" equal to => "+l+" divided by "+r,
        }
            return operators[ctx.bop.text]
        elif isinstance(ctx,rules.MethodCallContext):return self.visitMethodCall(ctx)
        elif isinstance(ctx,rules.PrimaryContext):return self.visitPrimary(ctx)
        elif ctx.OPEN_PAR() and ctx.CLOSE_PAR(): return ctx.children[1].getText()
        return self.visitChildren(ctx)

    def visitMethodCall(self, ctx: rules.MethodCallContext):
        text = self.visit(ctx.id_())
        if ctx.expressions() or ctx.settings():
            text +=  " passing params "+ self.visit(ctx.expressions()) if ctx.expressions() else " "+ self.visit(ctx.settings())         
        return text

    def visitId(self, ctx:rules.IdContext):
        return ctx.getText().upper()

    def visitLiteral(self, ctx: rules.LiteralContext):
        return ctx.getText()

    def visitInline(self, ctx:rules.InlineContext):
        if ctx.CLASSDATA() or ctx.DATA(): return  "data called "+ self.visit(ctx.id_())
        else: return "a table named " + self.visit(ctx.id_())

    def visitCast(self, ctx:rules.CastContext): 
        return self.visit(ctx.id_())+" cast to " + self.visit(ctx.fieldSymbol())
                



    


input = FileStream("files/ABAPCode.txt")
lexer = ABAPLexer(input)
stream = CommonTokenStream(lexer)
parser = rules(stream)
tree = parser.program()
output = open('files/pseudoCode.txt','w+')
vis = CustomABAPVisitor(output)
vis.visit(tree)
output.close()