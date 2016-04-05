"""the dictionary for the game """


wordlist = ["the", "of", "and", "to", "a", \
"in", "for", "is", "on", "that", "by", "this",\
"with", "i", "you", "it", "not", "or", "be", \
"are", "from", "at", "as", "your", "all", "have", \
"new", "more", "an", "was", "we", "will", "home", \
"can", "us", "about", "if", "page", "my", "has", \
"search", "free", "but", "our", "one", "other", "do", \
"no", "information", "time", "they", "site", "he", "up", \
"may", "what", "which", "their", "news", "out", "use", "any", \
"there", "see", "only", "so", "his", "when", "contact", "here", \
"business", "who", "web", "also", "now", "help", "get", "pm", \
"view", "online", "c", "e", "first", "am", "been", "would", \
"how", "were", "me", "s", "services", "some", "these", "click", \
"its", "like", "service", "x", "than", "find", "price", "date", \
"back", "top", "people", "had", "list", "name", "just", "over", \
"state", "year", "day", "into", "email", "two", "health", "n", \
"world", "re", "next", "used", "go", "b", "work", "last", "most", \
"products", "music", "buy", "data", "make", "them", "should", \
"product", "system", "post", "her", "city", "t", "add", "policy", \
"number", "such", "please", "available", "copyright", "support", \
"message", "after", "best", "software", "then", "jan", "good", \
"video", "well", "d", "where", "info", "rights", "public", \
"books", "high", "school", "through", "m", "each", "links", \
"she", "review", "years", "order", "very", "privacy", "book", \
"items", "company", "r", "read", "group", "sex", "need", "many", "user", \
"said", "de", "does", "set", "under", "general", "research", \
"university", "january", "mail", "full", "map", "reviews", "program", \
"life", "know", "games", "way", "days", "management", "p", \
"part", "could", "great", "united", "hotel", "real", "f", \
"item", "international", "center", "ebay", "must", "store", \
"travel", "comments", "made", "development", "report", "off", \
"member", "details", "line", "terms", "before", "hotels", "did", \
"send", "right", "type", "because", "local", "those", "using", \
"results", "office", "education", "national", "car", "design", \
"take", "posted", "internet", "address", "community", "within", \
"states", "area", "want", "phone", "dvd", "shipping", "reserved", \
"subject", "between", "forum", "family", "l", "long", "based", "w", \
"code", "show", "o", "even", "black", "check", "special", "prices", \
"website", "index", "being", "women", "much", "sign", "file", \
"link", "open", "today", "technology", "south", "case", "project", \
"same", "pages", "uk", "version", "section", "own", "found", \
"sports", "house", "related", "security", "both", "g", "county", \
"american", "photo", "game", "members", "power", "while", \
"care", "network", "down", "computer", "systems", "three", "total", \
"place", "end", "following", "download", "h", "him", "without", \
"per", "access", "think", "north", "resources", "current", \
"posts", "big", "media", "law", "control", "water", "history", \
"pictures", "size", "art", "personal", "since", "including", \
"guide", "shop", "directory", "board", "location", "change", \
"white", "text", "small", "rating", "rate", "government", \
"children", "during", "usa", "return", "students", "v", "shopping", \
"account", "times", "sites", "level", "digital", "profile", \
"previous", "form", "events", "love", "old", "john", "main", \
"call", "hours", "image", "department", "title", "description", \
"non", "k", "y", "insurance", "another", "why", "shall", \
"property", "class", "cd", "still", "money", "quality", "every", \
"listing", "content", "country", "private", "little", "visit", \
"save", "tools", "low", "reply", "customer", "december", \
"compare", "movies", "include", "college", "value", "article", \
"york", "man", "card", "jobs", "provide", "j", "food", \
"source", "author", "different", "press", "u", "learn", \
"sale", "around", "print", "course", "job", "canada", \
"process", "teen", "room", "stock", "training", "too", \
"credit", "point", "join", "science", "men", "categories", \
"advanced", "west", "sales", "look", "english", "left", \
"team", "estate", "box", "conditions", "select", "windows", \
"photos", "gay", "thread", "week", "category", "note", \
"live", "large", "gallery", "table", "register", "however", \
"june", "october", "november", "market", "library", "really", \
"action", "start", "series", "model", "features", "air", \
"industry", "plan", "human", "provided", "tv", "yes", "required", \
"second", "hot", "accessories", "cost", "movie", "forums", \
"march", "la", "september", "better", "say", "questions", \
"july", "yahoo", "going", "medical", "test", "friend", "come", \
"dec", "server", "pc", "study", "application", "cart", \
"staff", "articles", "san", "feedback", "again", "play", \
"looking", "issues", "april", "never", "users", "complete", \
"street", "topic", "comment", "financial", "things", "working", \
"against", "standard", "tax", "person", "below", "mobile", \
"less", "got", "blog", "party", "payment", "equipment", "login", \
"student", "let", "programs", "offers", "legal", "above", \
"recent", "park", "stores", "side", "act", "problem", "red", \
"give", "memory", "performance", "social", "q", "august", \
"quote", "language", "story", "sell", "options", "experience", \
"rates", "create", "key", "body", "young", "america", "important", \
"field", "few", "east", "paper", "single", "ii", "age", \
"activities", "club", "example", "girls", "additional", "password", \
"z", "latest", "something", "road", "gift", "question", "changes", \
"night", "ca", "hard", "texas", "oct", "pay", "four", "poker", \
"status", "browse", "issue", "range", "building", "seller", \
"court", "february", "always", "result", "audio", "light", "write", \
"war", "nov", "offer", "blue", "groups", "al", "easy", "given", \
"files", "event", "release", "analysis", "request", "fax", "china", \
"making", "picture", "needs", "possible", "might", "professional", \
"yet", "month", "major", "star", "areas", "future", "space", \
"committee", "hand", "sun", "cards", "problems", "london", "washington", \
"meeting", "rss", "become", "interest", "id", "child", "keep", "enter", \
"california", "porn", "share", "similar", "garden", "schools", \
"million", "added", "reference", "companies", "listed", "baby", "learning"]