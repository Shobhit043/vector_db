from vector_db import vector_db

db = vector_db()


docs = [
    # ============================================================
    # PYTHON / PROGRAMMING
    # ============================================================

    "Python is a programming language used to build backend services, REST APIs, web servers, and automation scripts.",

    "Python is widely used for data analysis, scientific computing, numerical processing, and machine learning.",

    "Python can be used to write command-line tools, automation programs, data processing pipelines, and web applications.",

    # Repeated Python-related terminology -> useful for testing TF
    "Python Python Python is commonly used for backend development. "
    "Python applications can expose APIs and Python services can run web servers.",

    # Same concept with different vocabulary -> semantic test
    "Server-side applications can be implemented using high-level programming languages "
    "and deployed as network services.",


    # ============================================================
    # DATABASES
    # ============================================================

    "PostgreSQL is a relational SQL database that stores structured records in tables and supports complex queries.",

    "PostgreSQL provides transactions, indexing, joins, constraints, and SQL queries for structured relational data.",

    "Redis is an in-memory key-value store commonly used for caching, sessions, queues, and low-latency data access.",

    "Redis stores frequently accessed values in memory to reduce latency and improve application response times.",

    # Semantic equivalent but few lexical matches
    "An in-memory data store can keep frequently requested information close to the application "
    "so that repeated reads are much faster.",

    # Long document containing database terms but weaker relevance
    "Modern applications often use databases, APIs, services, authentication, logging, monitoring, "
    "message queues, caches, background workers, containers, and cloud infrastructure. "
    "Relational databases can store structured records and applications can use SQL to retrieve them. "
    "Caching systems can reduce the number of database reads required by frequently accessed operations.",


    # ============================================================
    # CONTAINERS / DEPLOYMENT
    # ============================================================

    "Docker packages an application and its dependencies into isolated containers so it can run consistently across environments.",

    "Docker containers isolate applications from the host operating system and package libraries, binaries, and configuration together.",

    "Kubernetes orchestrates containers across clusters and manages deployment, scaling, scheduling, and service availability.",

    "Kubernetes automatically schedules container workloads across machines and can scale services based on demand.",

    "Containers provide process isolation and reproducible environments for running applications consistently across development, testing, and production.",

    # Deployment without the word Docker/Kubernetes
    "Applications can be released to production using isolated runtime environments that package "
    "the application together with everything it needs to execute.",


    # ============================================================
    # RETRIEVAL / RAG
    # ============================================================

    "RAG systems retrieve relevant documents from a knowledge base and provide that information as context to a language model.",

    "Retrieval augmented generation combines document search with language models so that generated answers can use external knowledge.",

    "Vector databases store embeddings and retrieve documents based on semantic similarity between their vector representations.",

    "Semantic search finds information based on meaning rather than requiring the query and document to contain exactly the same words.",

    "A retrieval system searches a collection of documents, ranks the candidates, and returns the most relevant passages to the user.",

    # Strong lexical match for retrieval but different concept
    "Document retrieval systems use ranking algorithms to score documents according to their relevance to a search query.",

    # ============================================================
    # MACHINE LEARNING
    # ============================================================

    "PyTorch is a deep learning framework used to build, train, and optimize neural network models.",

    "PyTorch provides tensors, automatic differentiation, neural network layers, optimizers, and tools for model training.",

    "TensorFlow is a machine learning framework used to train neural networks and deploy artificial intelligence models.",

    "Machine learning frameworks provide tools for training predictive models on large datasets.",

    "Neural networks learn patterns from training data and can be optimized using gradient-based methods.",


    # ============================================================
    # STREAMING / INFRASTRUCTURE
    # ============================================================

    "Apache Kafka is a distributed event streaming platform used to publish, store, and process streams of events.",

    "Kafka allows distributed applications to exchange events through durable topics and partitions.",

    "Nginx is a web server and reverse proxy commonly used to route HTTP requests and serve web applications.",

    "Nginx can distribute incoming HTTP traffic between multiple backend servers.",

    "Git is a version control system used to track source code changes and collaborate on software projects.",

    "Prometheus collects and monitors metrics from applications and infrastructure and can trigger alerts.",

    "Cloud platforms provide virtual machines, storage, networking, and managed services for deploying applications.",

    "Monitoring systems collect measurements from infrastructure and applications to detect failures and performance problems.",


    # ============================================================
    # CROSS-CONCEPT / DISTRACTOR DOCUMENTS
    # ============================================================

    "A web application may contain a frontend, backend API, database, cache, message queue, "
    "monitoring system, and deployment infrastructure.",

    "Application performance can depend on CPU usage, memory consumption, network latency, "
    "database queries, caching, concurrency, and infrastructure configuration.",

    "Distributed systems coordinate multiple computers so that applications can continue operating "
    "even when individual machines or services fail.",

    "Production systems commonly require deployment automation, observability, security, scalability, "
    "database management, caching, and reliable networking.",

    # Very short document -> document length normalization test
    "Docker deployment.",

    # Very long document with many generic terms -> BM25 length-normalization test
    """
    Modern software systems consist of applications, services, APIs, databases, caches,
    queues, workers, containers, virtual machines, networks, storage systems, monitoring
    platforms, logging systems, authentication systems, authorization systems, deployment
    pipelines, cloud infrastructure, and machine learning components.

    Applications may communicate through HTTP APIs, asynchronous messages, event streams,
    databases, caches, and internal service interfaces. Developers may use Python, Java,
    Go, JavaScript, or other programming languages. Databases may be relational or
    non-relational. Infrastructure may run on virtual machines, containers, Kubernetes
    clusters, or managed cloud services.

    Production environments require deployment, monitoring, logging, scaling, security,
    backups, testing, observability, networking, and resource management.
    """,
]


queries = [

    # ============================================================
    # 1. EXACT / STRONG LEXICAL MATCH
    # ============================================================

    "Python backend REST API",

    "PostgreSQL SQL database tables",

    "Redis caching",

    "Docker containers",

    "Kubernetes container orchestration",

    "PyTorch neural networks",

    "Kafka event streaming",

    "Nginx reverse proxy",

    "Prometheus application metrics",


    # ============================================================
    # 2. SINGLE TERM
    # ============================================================

    "Python",

    "Docker",

    "Redis",

    "Kubernetes",

    "retrieval",

    "database",

    "monitoring",

    "containers",


    # ============================================================
    # 3. SYNONYM / SEMANTIC SEARCH
    # ============================================================

    "How can I create a server-side application?",

    "How can I perform calculations on numerical datasets?",

    "How can I make frequently requested data faster to retrieve?",

    "How can I isolate an application from the host environment?",

    "How can I coordinate applications running across multiple machines?",

    "How can an LLM use information stored in my documents?",

    "How can I find documents with similar meaning?",

    "What software can I use to build and train an AI model?",

    "How can I monitor the health of my infrastructure?",

    "How can I distribute HTTP traffic between servers?",


    # ============================================================
    # 4. TF TESTS
    # ============================================================

    # Python appears in several documents, but one document repeats it heavily
    "Python",

    "Python programming",

    "Python backend application",

    # Database appears in many documents
    "database",

    "database application",

    "application performance",


    # ============================================================
    # 5. IDF TESTS
    # ============================================================

    # "application" is very common
    "application",

    # "PostgreSQL" is rare
    "PostgreSQL",

    # "Kubernetes" is rare
    "Kubernetes",

    # "embeddings" is relatively rare
    "embeddings",

    # Rare multi-term query
    "PostgreSQL transactions joins constraints",


    # ============================================================
    # 6. DOCUMENT LENGTH NORMALIZATION
    # ============================================================

    "Docker deployment",

    "application database",

    "application infrastructure",

    "production deployment",

    "application monitoring",


    # ============================================================
    # 7. AMBIGUOUS QUERIES
    # ============================================================

    "How can I deploy an application?",

    "How can I improve application performance?",

    "How can I process data?",

    "How can I manage running applications?",

    "How can I store and retrieve information quickly?",

    "How can I search a large collection of documents?",

    "How can I monitor an application?",


    # ============================================================
    # 8. BM25 vs SEMANTIC TENSION
    # ============================================================

    "server application deployment",

    "fast information retrieval",

    "distributed application management",

    "machine learning model training",

    "application isolation",

    "intelligent document retrieval",

    "scalable application infrastructure",

    "numerical computation",


    # ============================================================
    # 9. CROSS-CONCEPT QUERIES
    # ============================================================

    "How do I deploy a backend service using containers?",

    "How do I build an application that retrieves knowledge for an LLM?",

    "How do I improve the speed of a database-backed application?",

    "How do I run machine learning workloads in production?",

    "How do I monitor infrastructure running my applications?",

    "How do I build a scalable distributed backend?",

    "How do I cache database results in a web application?",


    # ============================================================
    # 10. QUERY WITH COMMON STOP WORDS
    # ============================================================

    "How can I use Python to build an application?",

    "What is the best way to store data in a database?",

    "How do I deploy an application using Docker?",

    "What can I use to retrieve information from documents?",


    # ============================================================
    # 11. PARTIAL / MORPHOLOGICAL MATCHING
    # ============================================================

    "deploy",

    "deployment",

    "retrieve",

    "retrieval",

    "train",

    "training",

    "application",

    "applications",


    # ============================================================
    # 12. ZERO / LOW LEXICAL OVERLAP
    # ============================================================

    "How do I make my software run faster?",

    "How do I keep information available for repeated requests?",

    "How do I run software consistently on different machines?",

    "How do I find relevant knowledge for a language model?",

    "How do I distribute work across computers?",


    # ============================================================
    # 13. UNKNOWN TERMS
    # ============================================================

    "quantum computing",

    "blockchain smart contracts",

    "astronomy telescope images",

    "medical diagnosis",

    "electric vehicle batteries",


    # ============================================================
    # 14. MULTI-CONCEPT QUERIES
    # ============================================================

    "Python PostgreSQL Docker",

    "Redis Kubernetes monitoring",

    "Python machine learning",

    "Docker Kubernetes deployment",

    "RAG vector database embeddings",

    "Kafka distributed applications",

    "Nginx backend API Docker",


    # ============================================================
    # 15. LONG NATURAL-LANGUAGE QUERIES
    # ============================================================

    "I am building a backend service in Python and I want to expose an API "
    "that can retrieve information from a database.",

    "I need a system that can search documents based on their meaning "
    "and then provide the retrieved information to a language model.",

    "I want to deploy several application services across multiple machines "
    "and automatically scale them when traffic increases.",

    "I have an application that frequently reads the same data and I want "
    "to reduce the latency of those repeated reads.",


    # ============================================================
    # 16. SHORT / EDGE CASES
    # ============================================================

    "",

    "API",

    "SQL",

    "AI",

    "data",

    "server",
]


db.add_doc_list(docs)


for query in queries:
    print(f"\nQuery: {query!r}")
    print("-" * 80)

    results = db.get_top_k_similar_docs(query, k=3)

    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")