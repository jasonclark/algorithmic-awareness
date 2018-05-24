function getSearchResults(q, limit, start, sort, facet) {
	var key = "YOUR-GOOGLE-CUSTOM-SEARCH-API-KEY-HERE";
	var id = "YOUR-GOOGLE-CUSTOM-SEARCH-ENGINE-ID-HERE";
	var url = "https://www.googleapis.com/customsearch/v1?key=" + key + "&cx=" + id + "&alt=json" + (sort == null ? "" : "&sort=" + sort) + "&num=" + limit + "&start=" + start + "&prettyprint=true&q=" + q + (facet == null ? "" : "&hq=" + facet);
	
	var xhr = new XMLHttpRequest();
	xhr.addEventListener("load", displaySearchResults);
	xhr.open("GET", url);
	xhr.send();
}

function displaySearchResults() {
	var results = JSON.parse(this.responseText);
	
	// Clear existing results
	var ul = document.querySelector("ul.result");
	ul.innerHTML = "";
	
	// Build the results links
	for (var result in results.items) {
		var item = document.createElement("li");
		item.innerHTML = "<a href='" + results.items[result]["link"] + "'>" + results.items[result]["htmlTitle"] + "</a><br />" + results.items[result]["htmlFormattedUrl"];
		ul.appendChild(item);
	}
	
	// Clear existing pagination
	var pagination = document.querySelector("ul.pages");
	pagination.innerHTML = "";
	
	// Create back/forward buttons
	function paginate(pageRef, text, className) {
		if (typeof pageRef !== "undefined") {
			var page = document.createElement("li");
			var link = document.createElement("a");
			link.classList.add(className);
			link.href = "#";
			link.addEventListener("click", function(e) {
				e.preventDefault();
				getSearchResults(pageRef[0].searchTerms, 10, pageRef[0].startIndex, null, null);
			});
			link.innerText = text;
			page.appendChild(link);
			pagination.appendChild(page);
		}
	}
	
	paginate(results.queries.previousPage, "Previous", "previous");
	paginate(results.queries.nextPage, "Next", "next");
	
	var resultsdiv = document.querySelector(".results");
	if (ul.innerHTML == "") {
		resultsdiv.classList.remove("returned");
		resultsdiv.classList.add("none");
	} else {
		resultsdiv.classList.add("returned");
		resultsdiv.classList.remove("none");
	}
	
	// Show relevant facets
	console.log(results);
	var facets = document.getElementById("facets")
	// Clear existing facets
	facets.className = "flex-facet";
	
	if (detectNaturalLanguage(results.queries.request[0].searchTerms)) {
		facets.classList.add("naturallanguage");
	}
	
	if (parseInt(results.searchInformation.totalResults) > 30) {
		facets.classList.add("many");
	}
	
	if (parseInt(results.searchInformation.totalResults) <= 0) {
		facets.classList.add("none");
	} else {
		facets.classList.add("categories");
		
		var searchFacets = results.context.facets;
		var terms = document.querySelector(".facet-categories p.terms");
		terms.innerHTML = "";
		
		var link = document.createElement("a");
		link.href = "#";
		link.addEventListener("click", function(e) {
			e.preventDefault();
			getSearchResults(results.queries.request[0].searchTerms, 10, results.queries.request[0].startIndex, null, null);
		});
		link.innerText = "All";
		terms.appendChild(link);
		
		for (var f in searchFacets) {
			var link = document.createElement("a");
			link.href = "#";
			link.addEventListener("click", function(e) {
				e.preventDefault();
				getSearchResults(results.queries.request[0].searchTerms, 10, results.queries.request[0].startIndex, null, searchFacets[f][0].anchor);
			});
			link.innerText = searchFacets[f][0].anchor;
			terms.appendChild(link);
		}
	}
}

function detectNaturalLanguage(q) {
	var cueWords = ["about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "by", "call", "can", "cannot", "cant", "could", "couldnt", "cry", "describe", "do", "either", "except", "few", "fill", "find", "found", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "how", "however", "hundred", "if", "in", "indeed", "interest", "into", "is", "keep", "might", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "never", "nevertheless", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps", "please", "put", "rather", "see", "seem", "seemed", "seeming", "seems", "should", "show", "side", "since", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "temp", "temperature", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "under", "until", "up", "upon", "us", "very", "time", "were", "weather", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"];
	
	// Find if first word in query exists in the list of cue words
	return cueWords.includes(q.split(" ", 1)[0]);
}

document.querySelector("form").addEventListener("submit", function(e) {
	e.preventDefault();
	var q = document.getElementById("q").value;
	getSearchResults(q, 10, 1, null, null);
});

