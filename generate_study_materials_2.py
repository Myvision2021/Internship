import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

def create_study_material(filepath, title, content_sections):
    # Setup document
    doc = BaseDocTemplate(filepath, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=120, bottomMargin=80)
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceAfter=20,
        textColor=HexColor('#000000')
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10,
        textColor=HexColor('#1c1e21')
    )
    
    sub_heading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceBefore=10,
        spaceAfter=5
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        spaceAfter=10
    )
    
    bullet_style = ParagraphStyle(
        'BulletList',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        leftIndent=20,
        spaceAfter=5
    )

    def header_footer(canvas, doc):
        canvas.saveState()
        
        # Header Background
        canvas.setFillColor(HexColor('#1c1e21'))
        canvas.rect(0, A4[1] - 80, A4[0], 80, stroke=0, fill=1)
        
        # Gold Accent Line
        canvas.setFillColor(HexColor('#d4af37'))
        canvas.rect(0, A4[1] - 85, A4[0], 5, stroke=0, fill=1)
        
        # Header Text
        canvas.setFillColor(HexColor('#ffffff'))
        canvas.setFont('Helvetica-Bold', 14)
        canvas.drawCentredString(A4[0]/2.0, A4[1] - 35, "IKON COMPUTER EDUCATION & TRAINING INSTITUTE")
        
        canvas.setFont('Helvetica', 12)
        canvas.drawCentredString(A4[0]/2.0, A4[1] - 55, "Study Material: " + title)
        
        # Footer Background
        canvas.setFillColor(HexColor('#1c1e21'))
        canvas.rect(0, 0, A4[0], 40, stroke=0, fill=1)
        
        # Footer Text
        canvas.setFillColor(HexColor('#ffffff'))
        canvas.setFont('Helvetica', 9)
        canvas.drawCentredString(A4[0]/2.0, 15, "Contact: info@ikoncomputer.com | Phone: +1-800-IKON-EDU | www.ikoncomputer.com")
        
        canvas.restoreState()
        
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=header_footer)
    doc.addPageTemplates([template])
    
    story = []
    
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2*inch))
    
    for section in content_sections:
        if section['type'] == 'heading':
            story.append(Paragraph(section['text'], heading_style))
        elif section['type'] == 'subheading':
            story.append(Paragraph(section['text'], sub_heading_style))
        elif section['type'] == 'paragraph':
            story.append(Paragraph(section['text'], body_style))
        elif section['type'] == 'bullet':
            # Note: Using standard hyphen for bullets to avoid unicode issues in some environments if needed, but reportlab supports standard bullet character.
            # We will use ASCII '-' to be extremely safe based on prompt "No unicode characters in print() statements" - well it said print statements, but let's be safe.
            story.append(Paragraph(f"- {section['text']}", bullet_style))
        elif section['type'] == 'pagebreak':
            story.append(PageBreak())
            
    doc.build(story)
    print(f"Created: {filepath}")

dbms_1 = [
    {"type": "heading", "text": "1. What is DBMS?"},
    {"type": "paragraph", "text": "A Database Management System (DBMS) is a software system that enables users to define, create, maintain, and control access to the database. It provides an environment that is both convenient and efficient to use. Examples include MySQL, Oracle, PostgreSQL, and SQL Server."},
    {"type": "paragraph", "text": "The primary goal of a DBMS is to provide a way to store and retrieve database information that is both convenient and efficient. By data, we mean known facts that can be recorded and that have implicit meaning."},
    {"type": "heading", "text": "2. Advantages over File System"},
    {"type": "paragraph", "text": "Before DBMS, data was stored in file processing systems. This approach had several limitations:"},
    {"type": "bullet", "text": "Data Redundancy and Inconsistency: Duplication of data in different files."},
    {"type": "bullet", "text": "Difficulty in Accessing Data: Need to write a new application program for each new task."},
    {"type": "bullet", "text": "Data Isolation: Data scattered in various files and formats."},
    {"type": "bullet", "text": "Integrity Problems: Difficult to enforce constraints."},
    {"type": "bullet", "text": "Atomicity of Updates: Hard to restore data to consistent state after failure."},
    {"type": "pagebreak"},
    {"type": "heading", "text": "3. DBMS Architecture"},
    {"type": "subheading", "text": "1-Tier Architecture"},
    {"type": "paragraph", "text": "In 1-tier architecture, the DBMS is the only entity where the user directly sits on the DBMS and uses it. Any changes done here will directly be done on the database itself."},
    {"type": "subheading", "text": "2-Tier Architecture"},
    {"type": "paragraph", "text": "The 2-tier architecture is like a client-server application. The user interface program and application programs run on the client side, while the database system runs on the server side."},
    {"type": "subheading", "text": "3-Tier Architecture"},
    {"type": "paragraph", "text": "A 3-tier architecture separates its tiers from each other based on the complexity of the users and how they use the data present in the database. It includes a presentation tier (client), an application tier (business logic), and a database tier."},
    {"type": "heading", "text": "4. Data Models"},
    {"type": "paragraph", "text": "Data models describe the structure of a database. Key types include:"},
    {"type": "bullet", "text": "Hierarchical Model: Data is organized in a tree-like structure."},
    {"type": "bullet", "text": "Network Model: Similar to hierarchical, but allows a record to have more than one parent."},
    {"type": "bullet", "text": "Relational Model: Data is represented in two-dimensional tables (relations)."},
    {"type": "bullet", "text": "Object-Oriented Model: Data is stored as objects."},
    {"type": "heading", "text": "5. Schemas and Data Independence"},
    {"type": "paragraph", "text": "A database schema is the skeleton structure that represents the logical view of the entire database. Data independence is the ability to modify a schema definition in one level without affecting a schema definition in the next higher level."}
]

dbms_2 = [
    {"type": "heading", "text": "1. Relational Model Concepts"},
    {"type": "paragraph", "text": "The relational model represents data as a collection of tables. A table is called a relation. Each row in a table represents a collection of related data values. These rows are called tuples. The columns are called attributes."},
    {"type": "heading", "text": "2. Types of Keys"},
    {"type": "bullet", "text": "Super Key: A set of one or more attributes that can uniquely identify a tuple."},
    {"type": "bullet", "text": "Candidate Key: A minimal super key; a super key with no redundant attributes."},
    {"type": "bullet", "text": "Primary Key: A candidate key chosen by the database designer as the principal means of identifying entities."},
    {"type": "bullet", "text": "Foreign Key: An attribute or set of attributes in one relation that refers to the primary key in another relation."},
    {"type": "pagebreak"},
    {"type": "heading", "text": "3. SQL DDL (Data Definition Language)"},
    {"type": "paragraph", "text": "DDL is used to define database structures or schemas."},
    {"type": "bullet", "text": "CREATE: To create objects in the database (e.g., tables)."},
    {"type": "bullet", "text": "ALTER: To alter the structure of the database."},
    {"type": "bullet", "text": "DROP: To delete objects from the database."},
    {"type": "heading", "text": "4. SQL DML (Data Manipulation Language)"},
    {"type": "paragraph", "text": "DML is used for managing data within schema objects."},
    {"type": "bullet", "text": "SELECT: Retrieve data from the database."},
    {"type": "bullet", "text": "INSERT: Insert data into a table."},
    {"type": "bullet", "text": "UPDATE: Update existing data within a table."},
    {"type": "bullet", "text": "DELETE: Delete records from a table."},
    {"type": "heading", "text": "5. Filtering and Grouping"},
    {"type": "paragraph", "text": "The WHERE clause is used to filter records based on specific conditions. The ORDER BY clause is used to sort the result-set in ascending or descending order."},
    {"type": "paragraph", "text": "The GROUP BY statement groups rows that have the same values into summary rows. The HAVING clause was added to SQL because the WHERE keyword cannot be used with aggregate functions."}
]

dbms_3 = [
    {"type": "heading", "text": "1. Normalization & Functional Dependencies"},
    {"type": "paragraph", "text": "Normalization is the process of organizing data in a database to avoid data redundancy, insertion anomaly, update anomaly, and deletion anomaly."},
    {"type": "paragraph", "text": "A functional dependency is a relationship that exists when one attribute uniquely determines another attribute. If A determines B, it is written as A -> B."},
    {"type": "heading", "text": "2. Normal Forms"},
    {"type": "bullet", "text": "1NF (First Normal Form): A relation is in 1NF if it contains an atomic value (indivisible)."},
    {"type": "bullet", "text": "2NF (Second Normal Form): A relation is in 2NF if it is in 1NF and all non-key attributes are fully functional dependent on the primary key."},
    {"type": "bullet", "text": "3NF (Third Normal Form): A relation is in 3NF if it is in 2NF and no transition dependency exists."},
    {"type": "bullet", "text": "BCNF (Boyce-Codd Normal Form): A stricter version of 3NF. For every functional dependency X -> Y, X must be a super key."},
    {"type": "pagebreak"},
    {"type": "heading", "text": "3. Anomalies in Database Design"},
    {"type": "bullet", "text": "Insertion Anomaly: Inability to insert a piece of information about an object without having to insert information about another object."},
    {"type": "bullet", "text": "Deletion Anomaly: The deletion of a record results in the loss of data about another entity."},
    {"type": "bullet", "text": "Update Anomaly: A data inconsistency that results from data redundancy and a partial update."},
    {"type": "heading", "text": "4. Entity-Relationship (ER) Diagrams"},
    {"type": "paragraph", "text": "An ER diagram is a structural diagram for use in database design. It contains different symbols and connectors that visualize two important information: The major entities within the system scope, and the inter-relationships among these entities."},
    {"type": "bullet", "text": "Entity: A real-world object (e.g., Student, Course)."},
    {"type": "bullet", "text": "Attributes: Properties that describe an entity (e.g., Name, Age)."},
    {"type": "bullet", "text": "Relationships: Associations between entities."},
    {"type": "bullet", "text": "Cardinality: The number of instances of an entity associated with another entity (1:1, 1:N, M:N)."}
]

dbms_4 = [
    {"type": "heading", "text": "1. Transactions and ACID Properties"},
    {"type": "paragraph", "text": "A transaction is a single logical unit of work that accesses and possibly modifies the contents of a database."},
    {"type": "paragraph", "text": "To ensure integrity, transactions must satisfy the ACID properties:"},
    {"type": "bullet", "text": "Atomicity: Either all operations of the transaction are reflected properly in the database, or none are."},
    {"type": "bullet", "text": "Consistency: Execution of a transaction in isolation preserves the consistency of the database."},
    {"type": "bullet", "text": "Isolation: Multiple transactions can execute concurrently without interfering with each other."},
    {"type": "bullet", "text": "Durability: After a transaction completes successfully, the changes it has made to the database persist, even if there are system failures."},
    {"type": "pagebreak"},
    {"type": "heading", "text": "2. Transaction States and Serializability"},
    {"type": "paragraph", "text": "A transaction can be in one of the following states: Active, Partially Committed, Failed, Aborted, or Committed."},
    {"type": "paragraph", "text": "Serializability ensures that a concurrent schedule of transactions is equivalent to a serial schedule, guaranteeing consistency."},
    {"type": "heading", "text": "3. Concurrency Control and Locking"},
    {"type": "paragraph", "text": "Concurrency control manages simultaneous operations without conflicts."},
    {"type": "bullet", "text": "Shared Lock (Read Lock): Allows a transaction to read but not update an item."},
    {"type": "bullet", "text": "Exclusive Lock (Write Lock): Allows a transaction to both read and update an item."},
    {"type": "heading", "text": "4. Deadlock and Two-Phase Locking"},
    {"type": "paragraph", "text": "A deadlock occurs when two or more transactions are waiting indefinitely for one another to release locks. Two-Phase Locking (2PL) is a protocol that requires transactions to acquire all locks before releasing any (Growing phase followed by Shrinking phase)."},
    {"type": "heading", "text": "5. Recovery Techniques"},
    {"type": "paragraph", "text": "Database recovery restores the database to a consistent state after a failure. Techniques include log-based recovery (undo/redo logs) and shadow paging."}
]

net_1 = [
    {"type": "heading", "text": "1. Introduction to Networks"},
    {"type": "paragraph", "text": "A computer network is a set of computers sharing resources located on or provided by network nodes."},
    {"type": "bullet", "text": "LAN (Local Area Network): Spans a small geographic area like a home or office."},
    {"type": "bullet", "text": "MAN (Metropolitan Area Network): Covers a city or a large campus."},
    {"type": "bullet", "text": "WAN (Wide Area Network): Covers a broad area, linking across metropolitan, regional, or national boundaries (e.g., the Internet)."},
    {"type": "heading", "text": "2. Network Topologies"},
    {"type": "bullet", "text": "Star: All nodes connect to a central hub/switch."},
    {"type": "bullet", "text": "Bus: All nodes share a single communication cable."},
    {"type": "bullet", "text": "Ring: Each node connects to exactly two other nodes, forming a ring."},
    {"type": "bullet", "text": "Mesh: Nodes are interconnected with many redundant interconnections."},
    {"type": "pagebreak"},
    {"type": "heading", "text": "3. OSI Model - 7 Layers"},
    {"type": "paragraph", "text": "The Open Systems Interconnection (OSI) model standardizes the communication functions of a telecommunication or computing system."},
    {"type": "subheading", "text": "Layer 7: Application Layer"},
    {"type": "paragraph", "text": "Network process to application. Provides network services directly to the user's application (e.g., HTTP, FTP)."},
    {"type": "subheading", "text": "Layer 6: Presentation Layer"},
    {"type": "paragraph", "text": "Data representation and encryption. Translates data between the application and network formats."},
    {"type": "subheading", "text": "Layer 5: Session Layer"},
    {"type": "paragraph", "text": "Interhost communication. Establishes, manages, and terminates connections between applications."},
    {"type": "subheading", "text": "Layer 4: Transport Layer"},
    {"type": "paragraph", "text": "End-to-end connections and reliability. Protocols include TCP and UDP."},
    {"type": "subheading", "text": "Layer 3: Network Layer"},
    {"type": "paragraph", "text": "Path determination and logical addressing (IP routing)."},
    {"type": "subheading", "text": "Layer 2: Data Link Layer"},
    {"type": "paragraph", "text": "Physical addressing (MAC). Handles framing and error detection."},
    {"type": "subheading", "text": "Layer 1: Physical Layer"},
    {"type": "paragraph", "text": "Media, signal, and binary transmission. Transmits raw bit stream over the physical medium."}
]

net_2 = [
    {"type": "heading", "text": "1. TCP/IP Protocol Suite"},
    {"type": "paragraph", "text": "The TCP/IP model is the conceptual model and set of communications protocols used in the Internet and similar networks. It has 4 layers: Application, Transport, Internet, and Link."},
    {"type": "heading", "text": "2. TCP vs UDP"},
    {"type": "paragraph", "text": "Both are Transport layer protocols."},
    {"type": "bullet", "text": "TCP (Transmission Control Protocol): Connection-oriented, reliable, orders packets, error-checking, slower. Uses a three-way handshake (SYN, SYN-ACK, ACK)."},
    {"type": "bullet", "text": "UDP (User Datagram Protocol): Connectionless, unreliable, unordered, faster, suited for streaming or gaming."},
    {"type": "heading", "text": "3. Port Numbers"},
    {"type": "paragraph", "text": "Ports are logical constructs that identify a specific process or a type of network service. Standard ports include HTTP (80), HTTPS (443), FTP (20/21), SSH (22)."},
    {"type": "pagebreak"},
    {"type": "heading", "text": "4. Key Application Layer Protocols"},
    {"type": "bullet", "text": "HTTP (Hypertext Transfer Protocol): Used for transmitting web pages over the internet."},
    {"type": "bullet", "text": "FTP (File Transfer Protocol): Used for the transfer of computer files between a client and server."},
    {"type": "bullet", "text": "SMTP (Simple Mail Transfer Protocol): The standard protocol for email transmission."},
    {"type": "bullet", "text": "DNS (Domain Name System): Translates human-readable domain names (like www.google.com) to machine-readable IP addresses."},
    {"type": "bullet", "text": "DHCP (Dynamic Host Configuration Protocol): Automatically assigns IP addresses and other network configuration parameters to devices."}
]

net_3 = [
    {"type": "heading", "text": "1. IPv4 Addressing"},
    {"type": "paragraph", "text": "An IPv4 address is a 32-bit number that uniquely identifies a network interface on a machine. It is typically represented in dot-decimal notation (e.g., 192.168.1.1)."},
    {"type": "heading", "text": "2. IPv4 Classes"},
    {"type": "bullet", "text": "Class A: 1.0.0.0 to 126.0.0.0 (Large networks)"},
    {"type": "bullet", "text": "Class B: 128.0.0.0 to 191.255.0.0 (Medium networks)"},
    {"type": "bullet", "text": "Class C: 192.0.0.0 to 223.255.255.0 (Small networks)"},
    {"type": "bullet", "text": "Class D: 224.0.0.0 to 239.255.255.255 (Multicast)"},
    {"type": "bullet", "text": "Class E: 240.0.0.0 to 255.255.255.255 (Experimental)"},
    {"type": "heading", "text": "3. Subnetting and CIDR"},
    {"type": "paragraph", "text": "Subnetting is the practice of dividing a network into two or more smaller networks. A subnet mask distinguishes the network prefix from the host identifier."},
    {"type": "paragraph", "text": "CIDR (Classless Inter-Domain Routing) notation represents an IP address and its routing prefix (e.g., 192.168.1.0/24)."},
    {"type": "pagebreak"},
    {"type": "heading", "text": "4. IPv6 Basics"},
    {"type": "paragraph", "text": "IPv6 addresses are 128-bit identifiers, solving the IPv4 address exhaustion problem. They are represented as eight groups of four hexadecimal digits (e.g., 2001:0db8:85a3:0000:0000:8a2e:0370:7334)."},
    {"type": "heading", "text": "5. Private vs Public IPs and NAT"},
    {"type": "paragraph", "text": "Private IP addresses are non-routable on the internet (e.g., 192.168.x.x, 10.x.x.x). Public IP addresses are globally unique and routable."},
    {"type": "paragraph", "text": "NAT (Network Address Translation) maps private IP addresses to a public IP address before transferring the information to the internet, allowing multiple devices on a local network to share a single public IP."}
]

net_4 = [
    {"type": "heading", "text": "1. Network Security Fundamentals"},
    {"type": "paragraph", "text": "Network security consists of the policies and practices adopted to prevent and monitor unauthorized access, misuse, modification, or denial of a computer network and network-accessible resources."},
    {"type": "heading", "text": "2. Types of Attacks"},
    {"type": "bullet", "text": "DoS (Denial of Service): Overloading a system's resources so it cannot respond to legitimate service requests."},
    {"type": "bullet", "text": "MITM (Man-in-the-Middle): An attacker secretly relays and possibly alters the communications between two parties who believe they are directly communicating with each other."},
    {"type": "bullet", "text": "Phishing: Fraudulent attempts to obtain sensitive information by disguising as a trustworthy entity in electronic communication."},
    {"type": "heading", "text": "3. Firewalls and VPNs"},
    {"type": "paragraph", "text": "A firewall is a network security device that monitors and filters incoming and outgoing network traffic based on an organization's previously established security policies."},
    {"type": "paragraph", "text": "A VPN (Virtual Private Network) extends a private network across a public network and enables users to send and receive data across shared or public networks as if their computing devices were directly connected to the private network."},
    {"type": "pagebreak"},
    {"type": "heading", "text": "4. Encryption and SSL/TLS"},
    {"type": "bullet", "text": "Symmetric Encryption: The same key is used to both encrypt and decrypt the information."},
    {"type": "bullet", "text": "Asymmetric Encryption: Uses a public key for encryption and a private key for decryption."},
    {"type": "paragraph", "text": "SSL/TLS (Secure Sockets Layer/Transport Layer Security) are cryptographic protocols designed to provide communications security over a computer network, widely used in HTTPS."},
    {"type": "heading", "text": "5. Authentication and Best Practices"},
    {"type": "paragraph", "text": "Authentication verifies the identity of a user, device, or system. Common methods include passwords, biometrics, and Multi-Factor Authentication (MFA)."},
    {"type": "paragraph", "text": "Best practices include regular security audits, keeping systems patched and updated, using strong passwords, network segmentation, and employee training on security awareness."}
]

def main():
    base_dir = r"d:\Internshipsite\study_materials"
    dbms_dir = os.path.join(base_dir, "dbms")
    net_dir = os.path.join(base_dir, "networking")
    
    os.makedirs(dbms_dir, exist_ok=True)
    os.makedirs(net_dir, exist_ok=True)
    
    print("Generating DBMS Study Materials...")
    create_study_material(os.path.join(dbms_dir, "dbms_01_introduction.pdf"), "Introduction to DBMS & Data Models", dbms_1)
    create_study_material(os.path.join(dbms_dir, "dbms_02_relational_sql.pdf"), "Relational Model & SQL Basics", dbms_2)
    create_study_material(os.path.join(dbms_dir, "dbms_03_normalization.pdf"), "Normalization & Database Design", dbms_3)
    create_study_material(os.path.join(dbms_dir, "dbms_04_transactions.pdf"), "Transactions & Concurrency Control", dbms_4)
    
    print("Generating Networking Study Materials...")
    create_study_material(os.path.join(net_dir, "networking_01_osi_model.pdf"), "Introduction to Networks & OSI Model", net_1)
    create_study_material(os.path.join(net_dir, "networking_02_tcp_ip.pdf"), "TCP/IP Protocol Suite", net_2)
    create_study_material(os.path.join(net_dir, "networking_03_ip_addressing.pdf"), "IP Addressing & Subnetting", net_3)
    create_study_material(os.path.join(net_dir, "networking_04_security.pdf"), "Network Security Fundamentals", net_4)
    
    print("Done! All 8 PDFs have been generated.")

if __name__ == "__main__":
    main()
