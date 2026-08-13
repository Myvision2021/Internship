import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

def create_header_footer(canvas, doc, title):
    canvas.saveState()
    
    # Header background
    canvas.setFillColor(HexColor('#1c1e21'))
    canvas.rect(0, doc.pagesize[1] - 1.2*inch, doc.pagesize[0], 1.2*inch, fill=1, stroke=0)
    
    # Gold accent line
    canvas.setFillColor(HexColor('#d4af37'))
    canvas.rect(0, doc.pagesize[1] - 1.25*inch, doc.pagesize[0], 0.05*inch, fill=1, stroke=0)
    
    # Header text - Institute Name
    canvas.setFont('Helvetica-Bold', 14)
    canvas.setFillColor(HexColor('#ffffff'))
    canvas.drawCentredString(doc.pagesize[0]/2.0, doc.pagesize[1] - 0.4*inch, "IKON COMPUTER EDUCATION & TRAINING INSTITUTE")
    
    # Header text - Subtitle
    canvas.setFont('Helvetica', 10)
    canvas.drawCentredString(doc.pagesize[0]/2.0, doc.pagesize[1] - 0.6*inch, "Study Material")
    
    # Header text - Topic Title
    canvas.setFont('Helvetica-Bold', 12)
    canvas.setFillColor(HexColor('#d4af37'))
    canvas.drawCentredString(doc.pagesize[0]/2.0, doc.pagesize[1] - 0.9*inch, title)
    
    # Footer background
    canvas.setFillColor(HexColor('#1c1e21'))
    canvas.rect(0, 0, doc.pagesize[0], 0.6*inch, fill=1, stroke=0)
    
    # Footer text
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(HexColor('#ffffff'))
    canvas.drawString(0.5*inch, 0.2*inch, "IKON COMPUTER EDUCATION | Contact: info@ikon.edu | www.ikon.edu")
    
    # Page number
    page_num = canvas.getPageNumber()
    canvas.drawRightString(doc.pagesize[0] - 0.5*inch, 0.2*inch, f"Page {page_num}")
    
    canvas.restoreState()

def generate_pdf(filename, title, content_list):
    doc = SimpleDocTemplate(
        filename, 
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=110,
        bottomMargin=60
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceAfter=16,
        textColor=HexColor('#1c1e21')
    )
    
    heading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
        textColor=HexColor('#1c1e21')
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        spaceAfter=10,
        leading=16,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        spaceAfter=6,
        leading=16,
        leftIndent=20,
        bulletIndent=10
    )

    Story = []
    
    # Title
    Story.append(Paragraph(title, title_style))
    Story.append(Spacer(1, 12))
    
    for item in content_list:
        if item['type'] == 'heading':
            Story.append(Paragraph(item['text'], heading_style))
        elif item['type'] == 'body':
            Story.append(Paragraph(item['text'], body_style))
        elif item['type'] == 'bullet':
            Story.append(Paragraph(item['text'], bullet_style))
        elif item['type'] == 'pagebreak':
            Story.append(PageBreak())
            
    doc.build(Story, onFirstPage=lambda c, d: create_header_footer(c, d, title), onLaterPages=lambda c, d: create_header_footer(c, d, title))

def get_java_content_01():
    return [
        {'type': 'heading', 'text': '1. What is Java?'},
        {'type': 'body', 'text': 'Java is a high-level, class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible. It is a general-purpose programming language intended to let programmers write once, run anywhere (WORA), meaning that compiled Java code can run on all platforms that support Java without the need to recompile.'},
        {'type': 'body', 'text': 'Java applications are typically compiled to bytecode that can run on any Java virtual machine (JVM) regardless of the underlying computer architecture.'},
        {'type': 'heading', 'text': '2. JDK, JRE, and JVM'},
        {'type': 'body', 'text': 'Understanding the differences between JDK, JRE, and JVM is crucial for any Java developer:'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>JVM (Java Virtual Machine):</b> It is an abstract machine. It is a specification that provides a runtime environment in which Java bytecode can be executed. It can also run those programs which are written in other languages and compiled to Java bytecode.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>JRE (Java Runtime Environment):</b> It is a software package that contains what is required to run a Java program. It includes a Java Virtual Machine implementation together with an implementation of the Java Class Library.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>JDK (Java Development Kit):</b> It is a software development environment used for developing Java applications and applets. It includes the JRE, an interpreter/loader (Java), a compiler (javac), an archiver (jar), a documentation generator (Javadoc) and other tools needed in Java development.'},
        {'type': 'pagebreak', 'text': ''},
        {'type': 'heading', 'text': '3. Features of Java'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Simple:</b> Java is easy to learn, and its syntax is clean, crisp, and easy to understand.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Object-Oriented:</b> In Java, everything is an Object. Java can be easily extended since it is based on the Object model.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Platform Independent:</b> Unlike many other programming languages including C and C++, when Java is compiled, it is not compiled into platform-specific machine, rather into platform-independent byte code.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Secure:</b> With Java\'s secure feature, it enables to develop virus-free, tamper-free systems.'},
        {'type': 'heading', 'text': '4. OOP Principles in Java'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Encapsulation:</b> Wrapping data and code together as a single unit.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Inheritance:</b> Mechanism where one class acquires the properties of another.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Polymorphism:</b> Ability of a variable, function or object to take on multiple forms.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Abstraction:</b> Hiding internal details and showing functionality only.'},
        {'type': 'heading', 'text': '5. First Java Program and Compilation'},
        {'type': 'body', 'text': 'A basic Java program looks like this:'},
        {'type': 'body', 'text': 'public class HelloWorld {<br/>  public static void main(String[] args) {<br/>    System.out.println("Hello, World!");<br/>  }<br/>}'},
        {'type': 'body', 'text': 'Compilation: javac HelloWorld.java (produces HelloWorld.class)<br/>Execution: java HelloWorld (runs the bytecode on the JVM).'}
    ]

def get_java_content_02():
    return [
        {'type': 'heading', 'text': '1. Primitive Data Types'},
        {'type': 'body', 'text': 'Java is a strongly typed language, which means that every variable must be declared with a data type. There are 8 primitive data types in Java:'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>byte:</b> 8-bit signed two\'s complement integer. (min -128, max 127)'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>short:</b> 16-bit signed two\'s complement integer.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>int:</b> 32-bit signed two\'s complement integer.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>long:</b> 64-bit signed two\'s complement integer.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>float:</b> single-precision 32-bit IEEE 754 floating point.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>double:</b> double-precision 64-bit IEEE 754 floating point.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>boolean:</b> has only two possible values: true and false.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>char:</b> single 16-bit Unicode character.'},
        {'type': 'heading', 'text': '2. Type Casting'},
        {'type': 'body', 'text': 'Type casting is when you assign a value of one primitive data type to another type.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Widening Casting (Automatic):</b> converting a smaller type to a larger type size. byte -> short -> char -> int -> long -> float -> double'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Narrowing Casting (Manual):</b> converting a larger type to a smaller size type. double -> float -> long -> int -> char -> short -> byte'},
        {'type': 'pagebreak', 'text': ''},
        {'type': 'heading', 'text': '3. Control Flow: If-Else and Switch'},
        {'type': 'body', 'text': 'Java uses control flow statements to control the flow of execution of a program based on certain conditions.'},
        {'type': 'body', 'text': '<b>If-Else Statement:</b> executes a block of code if a specified condition is true. If the condition is false, another block of code can be executed.'},
        {'type': 'body', 'text': '<b>Switch Statement:</b> allows a variable to be tested for equality against a list of values. Each value is called a case, and the variable being switched on is checked for each case.'},
        {'type': 'heading', 'text': '4. Loops in Java'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>for loop:</b> Useful when you know exactly how many times you want to loop through a block of code.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>while loop:</b> Loops through a block of code as long as a specified condition is true.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>do-while loop:</b> This loop will execute the code block once, before checking if the condition is true, then it will repeat the loop as long as the condition is true.'},
        {'type': 'heading', 'text': '5. Break and Continue'},
        {'type': 'body', 'text': 'The <b>break</b> statement can also be used to jump out of a loop.'},
        {'type': 'body', 'text': 'The <b>continue</b> statement breaks one iteration (in the loop), if a specified condition occurs, and continues with the next iteration in the loop.'}
    ]

def get_java_content_03():
    return [
        {'type': 'heading', 'text': '1. Arrays in Java'},
        {'type': 'body', 'text': 'An array is a container object that holds a fixed number of values of a single type. The length of an array is established when the array is created. After creation, its length is fixed.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>1D Arrays:</b> A list of variables of the same type, accessed by a common name. Example: int[] arr = new int[5];'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>2D Arrays:</b> Arrays of arrays, often used to represent matrices or tables. Example: int[][] matrix = new int[3][3];'},
        {'type': 'heading', 'text': '2. Strings in Java'},
        {'type': 'body', 'text': 'Strings, which are widely used in Java programming, are a sequence of characters. In Java programming language, strings are objects. The Java platform provides the String class to create and manipulate strings.'},
        {'type': 'body', 'text': '<b>String immutability:</b> String objects are immutable, which means that once created, their values cannot be changed.'},
        {'type': 'body', 'text': 'Important String methods include: length(), charAt(), substring(), toLowerCase(), toUpperCase(), trim(), replace(), split().'},
        {'type': 'pagebreak', 'text': ''},
        {'type': 'heading', 'text': '3. StringBuilder and StringBuffer'},
        {'type': 'body', 'text': 'Because String objects are immutable, manipulating them can create many temporary objects and be inefficient. StringBuilder and StringBuffer classes are used when you want to modify character strings.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>StringBuilder:</b> Fast, not thread-safe.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>StringBuffer:</b> Slower, but thread-safe (synchronized).'},
        {'type': 'heading', 'text': '4. Exception Handling'},
        {'type': 'body', 'text': 'An exception is an unwanted or unexpected event, which occurs during the execution of a program i.e at run time, that disrupts the normal flow of the program\'s instructions.'},
        {'type': 'body', 'text': '<b>try-catch-finally block:</b>'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> The <b>try</b> statement allows you to define a block of code to be tested for errors while it is being executed.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> The <b>catch</b> statement allows you to define a block of code to be executed, if an error occurs in the try block.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> The <b>finally</b> statement lets you execute code, after try...catch, regardless of the result.'},
        {'type': 'heading', 'text': '5. Throw, Throws and Custom Exceptions'},
        {'type': 'body', 'text': 'The <b>throw</b> keyword is used to explicitly throw an exception.'},
        {'type': 'body', 'text': 'The <b>throws</b> keyword is used in a method signature to declare that it might throw exceptions.'},
        {'type': 'body', 'text': '<b>Custom Exceptions:</b> You can create your own exception classes by extending the Exception class (for checked exceptions) or RuntimeException class (for unchecked exceptions).'}
    ]

def get_java_content_04():
    return [
        {'type': 'heading', 'text': '1. What is JDBC?'},
        {'type': 'body', 'text': 'JDBC (Java Database Connectivity) is an application programming interface (API) for the programming language Java, which defines how a client may access a database. It is a Java-based data access technology used for Java database connectivity.'},
        {'type': 'body', 'text': 'It provides methods to query and update data in a database, and is oriented towards relational databases.'},
        {'type': 'heading', 'text': '2. JDBC Architecture'},
        {'type': 'body', 'text': 'The JDBC API supports both two-tier and three-tier processing models for database access but in general, JDBC Architecture consists of two layers:'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>JDBC API:</b> This provides the application-to-JDBC Manager connection.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>JDBC Driver API:</b> This supports the JDBC Manager-to-Driver Connection.'},
        {'type': 'heading', 'text': '3. Core JDBC Interfaces'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>DriverManager:</b> This class manages a list of database drivers. Matches connection requests from the java application with the proper database driver using communication sub protocol.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Connection:</b> Represents a session with a specific database. SQL statements are executed and results are returned within the context of a connection.'},
        {'type': 'pagebreak', 'text': ''},
        {'type': 'heading', 'text': '4. Statements and ResultSets'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Statement:</b> Interface used to execute static SQL statements and return the results it produces.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>PreparedStatement:</b> A precompiled SQL statement. This object can then be used to efficiently execute this statement multiple times. It also helps prevent SQL injection.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>ResultSet:</b> Represents a database result set, which is usually generated by executing a statement that queries the database.'},
        {'type': 'heading', 'text': '5. CRUD Operations Example Steps'},
        {'type': 'body', 'text': 'To perform CRUD (Create, Read, Update, Delete) operations using JDBC:'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> 1. Import JDBC packages.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> 2. Register JDBC driver (Class.forName).'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> 3. Open a connection (DriverManager.getConnection).'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> 4. Execute a query (using Statement or PreparedStatement).'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> 5. Extract data from result set (for Read operations).'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> 6. Clean up the environment (close ResultSet, Statement, Connection).'}
    ]

def get_python_content_01():
    return [
        {'type': 'heading', 'text': '1. What is Python?'},
        {'type': 'body', 'text': 'Python is an interpreted, high-level and general-purpose programming language. Created by Guido van Rossum and first released in 1991, Python\'s design philosophy emphasizes code readability with its notable use of significant indentation.'},
        {'type': 'body', 'text': 'Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects.'},
        {'type': 'heading', 'text': '2. Key Features of Python'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Easy to Learn and Use:</b> Python has a simple syntax similar to the English language.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Interpreted Language:</b> Python code is executed line by line, which makes debugging easier.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Dynamically Typed:</b> You don\'t need to declare the type of a variable when you create one.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Extensive Standard Library:</b> Python comes with a large standard library that supports many common programming tasks.'},
        {'type': 'pagebreak', 'text': ''},
        {'type': 'heading', 'text': '3. Variables and Data Types'},
        {'type': 'body', 'text': 'Variables are containers for storing data values. In Python, variables are created when you assign a value to it.'},
        {'type': 'body', 'text': 'Built-in Data Types:'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Text Type:</b> str'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Numeric Types:</b> int, float, complex'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Sequence Types:</b> list, tuple, range'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Mapping Type:</b> dict'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Set Types:</b> set, frozenset'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Boolean Type:</b> bool'},
        {'type': 'heading', 'text': '4. Input/Output and Type Conversion'},
        {'type': 'body', 'text': '<b>Output:</b> The print() function prints the specified message to the screen.'},
        {'type': 'body', 'text': '<b>Input:</b> The input() function allows user input. By default, it returns a string.'},
        {'type': 'body', 'text': '<b>Type Conversion (Casting):</b> You can convert from one type to another with the int(), float(), and str() methods.'},
        {'type': 'heading', 'text': '5. Operators in Python'},
        {'type': 'body', 'text': 'Operators are used to perform operations on variables and values.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Arithmetic:</b> +, -, *, /, // (floor division), % (modulus), ** (exponentiation)'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Comparison:</b> ==, !=, >, <, >=, <='},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Logical:</b> and, or, not'}
    ]

def get_python_content_02():
    return [
        {'type': 'heading', 'text': '1. Control Structures: If-Elif-Else'},
        {'type': 'body', 'text': 'Decision-making is anticipation of conditions occurring while execution of the program and specifying actions taken according to the conditions.'},
        {'type': 'body', 'text': 'Python uses if, elif (else if), and else statements. Indentation (whitespace at the beginning of a line) is used to define scope in the code.'},
        {'type': 'heading', 'text': '2. Loops in Python'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>while loop:</b> With the while loop we can execute a set of statements as long as a condition is true.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>for loop:</b> A for loop is used for iterating over a sequence (that is either a list, a tuple, a dictionary, a set, or a string).'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>range() function:</b> To loop through a set of code a specified number of times, we can use the range() function. It returns a sequence of numbers.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>break/continue:</b> \'break\' stops the loop entirely. \'continue\' stops the current iteration and continues with the next.'},
        {'type': 'pagebreak', 'text': ''},
        {'type': 'heading', 'text': '3. Defining Functions'},
        {'type': 'body', 'text': 'A function is a block of code which only runs when it is called. You can pass data, known as parameters, into a function. A function can return data as a result.'},
        {'type': 'body', 'text': 'In Python a function is defined using the <b>def</b> keyword.'},
        {'type': 'body', 'text': 'Example: def my_function(name): return f"Hello {name}"'},
        {'type': 'heading', 'text': '4. Parameters, Arguments and Return Values'},
        {'type': 'body', 'text': 'Information can be passed into functions as arguments.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Default Parameter Value:</b> You can define a default value for a parameter.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Arbitrary Arguments (*args):</b> If you do not know how many arguments will be passed, add a * before the parameter name.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Keyword Arguments (**kwargs):</b> If you do not know how many keyword arguments will be passed, add two asterisks: **.'},
        {'type': 'body', 'text': 'To let a function return a value, use the <b>return</b> statement.'},
        {'type': 'heading', 'text': '5. Lambda Functions and Scope'},
        {'type': 'body', 'text': 'A lambda function is a small anonymous function. It can take any number of arguments, but can only have one expression.'},
        {'type': 'body', 'text': 'Syntax: lambda arguments : expression'},
        {'type': 'body', 'text': '<b>Scope:</b> A variable is only available from inside the region it is created. This is called scope. (Local vs Global scope).'}
    ]

def get_python_content_03():
    return [
        {'type': 'heading', 'text': '1. Lists in Python'},
        {'type': 'body', 'text': 'Lists are used to store multiple items in a single variable. Lists are ordered, changeable (mutable), and allow duplicate values.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Methods:</b> append(), insert(), remove(), pop(), clear(), sort(), reverse().'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Slicing:</b> You can specify a range of indexes by specifying where to start and where to end the range. list[start:end:step]'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>List Comprehension:</b> Offers a shorter syntax when you want to create a new list based on the values of an existing list. Example: [x for x in fruits if "a" in x]'},
        {'type': 'heading', 'text': '2. Tuples'},
        {'type': 'body', 'text': 'Tuples are used to store multiple items in a single variable. A tuple is a collection which is ordered and <b>unchangeable</b> (immutable).'},
        {'type': 'body', 'text': 'Tuples are written with round brackets (). Because they are immutable, operations like append() or remove() are not available.'},
        {'type': 'pagebreak', 'text': ''},
        {'type': 'heading', 'text': '3. Sets'},
        {'type': 'body', 'text': 'A set is a collection which is unordered, unchangeable (but you can remove items and add new items), and unindexed. Sets do not allow duplicate values.'},
        {'type': 'body', 'text': 'Sets are written with curly brackets {}. They are highly efficient for membership testing (checking if an item exists) and removing duplicates from a sequence.'},
        {'type': 'body', 'text': 'Common operations include union(), intersection(), difference(), symmetric_difference().'},
        {'type': 'heading', 'text': '4. Dictionaries'},
        {'type': 'body', 'text': 'Dictionaries are used to store data values in key:value pairs. A dictionary is a collection which is ordered (as of Python 3.7), changeable and do not allow duplicates (keys must be unique).'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Methods:</b> get(), keys(), values(), items(), update(), pop().'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>Iteration:</b> You can loop through a dictionary to get keys, values, or both (using .items()).'},
        {'type': 'heading', 'text': '5. Nested Data Structures'},
        {'type': 'body', 'text': 'A dictionary can contain dictionaries, this is called nested dictionaries. Similarly, a list can contain lists (nested lists/2D arrays), or a list can contain dictionaries, etc.'},
        {'type': 'body', 'text': 'Nested structures are very common for representing complex data structures like JSON.'}
    ]

def get_python_content_04():
    return [
        {'type': 'heading', 'text': '1. File Handling Basics'},
        {'type': 'body', 'text': 'File handling is an important part of any web application. Python has several functions for creating, reading, updating, and deleting files.'},
        {'type': 'body', 'text': 'The key function for working with files in Python is the <b>open()</b> function. It takes two parameters; filename, and mode.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> "r" - Read (Default). Opens a file for reading, error if it doesn\'t exist.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> "a" - Append. Opens a file for appending, creates the file if it does not exist.'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> "w" - Write. Opens a file for writing, creates the file if it does not exist. (Overwrites existing content)'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> "x" - Create. Creates the specified file, returns an error if the file exists.'},
        {'type': 'heading', 'text': '2. The with Statement'},
        {'type': 'body', 'text': 'It is good practice to use the <b>with</b> keyword when dealing with file objects. The advantage is that the file is properly closed after its suite finishes, even if an exception is raised at some point.'},
        {'type': 'body', 'text': 'Example:<br/>with open("file.txt", "r") as f:<br/>    content = f.read()'},
        {'type': 'pagebreak', 'text': ''},
        {'type': 'heading', 'text': '3. CSV Handling'},
        {'type': 'body', 'text': 'CSV (Comma Separated Values) format is the most common import and export format for spreadsheets and databases. Python has a built-in module called <b>csv</b> to handle these files.'},
        {'type': 'body', 'text': 'You can use csv.reader() for reading and csv.writer() for writing data to CSV files.'},
        {'type': 'heading', 'text': '4. OS and Sys Modules'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>os module:</b> Provides a portable way of using operating system dependent functionality. (e.g., os.path.exists(), os.remove(), os.mkdir())'},
        {'type': 'bullet', 'text': '<bullet>&bull;</bullet> <b>sys module:</b> Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. (e.g., sys.argv for command line arguments).'},
        {'type': 'heading', 'text': '5. Modules and PIP'},
        {'type': 'body', 'text': 'Consider a module to be the same as a code library. A file containing a set of functions you want to include in your application.'},
        {'type': 'body', 'text': 'To create a module just save the code you want in a file with the file extension .py. To use a module, use the <b>import</b> statement.'},
        {'type': 'body', 'text': '<b>PIP:</b> PIP is a package manager for Python packages, or modules if you like. You can use it to install packages from the Python Package Index (PyPI).'}
    ]

def main():
    base_dir = r"d:\\Internshipsite\\study_materials"
    java_dir = os.path.join(base_dir, "java")
    python_dir = os.path.join(base_dir, "python")
    
    os.makedirs(java_dir, exist_ok=True)
    os.makedirs(python_dir, exist_ok=True)
    
    # Generate Java PDFs
    generate_pdf(os.path.join(java_dir, "java_01_introduction_oop.pdf"), "Introduction to Java & OOP Concepts", get_java_content_01())
    print("Created java_01_introduction_oop.pdf")
    
    generate_pdf(os.path.join(java_dir, "java_02_data_types_control.pdf"), "Data Types, Variables & Control Flow", get_java_content_02())
    print("Created java_02_data_types_control.pdf")
    
    generate_pdf(os.path.join(java_dir, "java_03_arrays_strings.pdf"), "Arrays, Strings & Exception Handling", get_java_content_03())
    print("Created java_03_arrays_strings.pdf")
    
    generate_pdf(os.path.join(java_dir, "java_04_jdbc.pdf"), "JDBC & Database Connectivity", get_java_content_04())
    print("Created java_04_jdbc.pdf")
    
    # Generate Python PDFs
    generate_pdf(os.path.join(python_dir, "python_01_basics.pdf"), "Python Basics & Data Types", get_python_content_01())
    print("Created python_01_basics.pdf")
    
    generate_pdf(os.path.join(python_dir, "python_02_control_functions.pdf"), "Control Structures & Functions", get_python_content_02())
    print("Created python_02_control_functions.pdf")
    
    generate_pdf(os.path.join(python_dir, "python_03_data_structures.pdf"), "Data Structures in Python", get_python_content_03())
    print("Created python_03_data_structures.pdf")
    
    generate_pdf(os.path.join(python_dir, "python_04_file_handling.pdf"), "File Handling & Modules", get_python_content_04())
    print("Created python_04_file_handling.pdf")
    
    print("All PDFs created successfully.")

if __name__ == "__main__":
    main()
