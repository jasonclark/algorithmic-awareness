function getSearchResults(q, limit, start, sort, facet) {
  const key = "YOUR-GOOGLE-CUSTOM-SEARCH-API-KEY-HERE";
  const id = "YOUR-GOOGLE-CUSTOM-SEARCH-ENGINE-ID-HERE";
  const url = `https://www.googleapis.com/customsearch/v1?key=${key}&cx=${id}&alt=json${sort == null ? "" : `&sort=${sort}`}&num=${limit}&start=${start}&prettyprint=true&q=${q}${facet == null ? "" : `&hq=${facet}`}`;
  
  const xhr = new XMLHttpRequest();
  xhr.addEventListener("load", function () {
    if (this.status >= 200 && this.status < 300) {
      displaySearchResults.call(this);
      return;
    }
    alert("Search could not be completed. Please try again.");
    console.error("Search API error:", this.status, this.responseText);
  });
  xhr.addEventListener("error", function () {
    alert("Could not connect to the search service. Please try again.");
  });
  xhr.open("GET", url);
  xhr.send();
}

function displaySearchResults() {
  const results = JSON.parse(this.responseText);
  // Clear existing results
  const ul = document.querySelector("ul.result");
  ul.innerHTML = "";
  // Show info about results
  const resultinfo = document.getElementById("result-info");
  resultinfo.innerHTML = `Search for <em>${results.queries.request[0].searchTerms}</em> has about ${results.queries.request[0].totalResults} result(s)`;
  // Show current search category (facet)
  const sortcategory = document.getElementById("sort-category");
  if ("hq" in results.queries.request[0]) {
    sortcategory.innerHTML = `Category: ${results.queries.request[0].hq}`;
  }
  // Build the results links
  for (const result in results.items) {
    const item = document.createElement("li");
    item.innerHTML = `<a href='${results.items[result]["link"]}'>${results.items[result]["htmlTitle"]}</a><br />${results.items[result]["htmlFormattedUrl"]}`;
    ul.appendChild(item);
  } 
  // Clear existing pagination
  const pagination = document.querySelector("ul.pages");
  pagination.innerHTML = ""; 
  // Create back/forward buttons
  function paginate(pageRef, text, className) {
    if (typeof pageRef !== "undefined") {
      const page = document.createElement("li");
      const link = document.createElement("a");
      link.classList.add(className);
      link.href = "#";
      link.addEventListener("click", e => {
        e.preventDefault();
        getSearchResults(pageRef[0].searchTerms, 10, pageRef[0].startIndex, null, pageRef[0].hq);
      });
      link.innerText = text;
      page.appendChild(link);
      pagination.appendChild(page);
    }
  }
  
  paginate(results.queries.previousPage, "Previous", "previous");
  paginate(results.queries.nextPage, "Next", "next");
  
  const resultsdiv = document.querySelector(".results");
  if (ul.innerHTML == "") {
    resultsdiv.classList.remove("returned");
    resultsdiv.classList.add("none");
  } else {
    resultsdiv.classList.add("returned");
    resultsdiv.classList.remove("none");
  }
  
  // Show relevant facets
  console.log(results);
  const facets = document.getElementById("facets");
  // Clear existing facets
  facets.className = "flex-facet";
  // If you have results, make offers visible
  facets.classList.add("offer");

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
    // Create list of categories to narrow down search
    const searchFacets = results.context.facets;
    const terms = document.querySelector(".facet-categories p.terms");
    terms.innerHTML = "";
    
    // The first "all" category
    var link = document.createElement("a");
    link.href = "#";
    link.addEventListener("click", e => {
      e.preventDefault();
      getSearchResults(results.queries.request[0].searchTerms, 10, 1, null, null);
    });
    link.innerText = "All";
    terms.appendChild(link);
    
    for (const f in searchFacets) {
      var link = document.createElement("a");
      link.href = "#";
      (category => {
        link.addEventListener("click", e => {
          e.preventDefault();
          getSearchResults(results.queries.request[0].searchTerms, 10, 1, null, category);
        });
      })(searchFacets[f][0].anchor);
      link.innerText = searchFacets[f][0].anchor;
      terms.appendChild(link);
    }
  }
}

function detectNaturalLanguage(q) {
  const cueWords = ["about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "by", "call", "can", "cannot", "cant", "could", "couldnt", "cry", "describe", "do", "either", "except", "few", "fill", "find", "found", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "how", "however", "hundred", "if", "in", "indeed", "interest", "into", "is", "keep", "might", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "never", "nevertheless", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps", "please", "put", "rather", "see", "seem", "seemed", "seeming", "seems", "should", "show", "side", "since", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "temp", "temperature", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "under", "until", "up", "upon", "us", "very", "time", "were", "weather", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"];
  // Find if first word in query exists in the list of cue words
  return cueWords.includes(q.split(" ", 1)[0]);
}

function researchOffer() {
  const today = new Date();
  console.log(today);
  // Note: avoid date ranges that include the new year
  const ranges = [
    {
      start: [10, 1], // MM, DD
      end: [12, 18],
      message: 'It is that time of the year. The days are shorter and research papers are happening. Get started by <a href="http://ask.lib.montana.edu/ask">talking to a Librarian</a>.',
      annotation: "The current date falls within our fall research paper period, so we're suggesting help from a librarian."
    },
    {
      start: [3, 1],
      end: [5, 18],
      message: 'It is that time of the year. Spring fever is almost here, but you have a research paper to write. Get started by <a href="http://ask.lib.montana.edu/ask">talking to a Librarian</a>.',
      annotation: "It's getting later in the spring semester, so since you might be needing help with research, we're giving you a link to talk with a librarian."
    },
    {
      start: [5, 18],
      end: [8, 31],
      message: "School may be out but it's never a bad time to come in to the library. Stop in to chat with your friendly librarians today.",
      annotation: "It's summer, and most students will be out for summer break, so we're not going to show suggestions about helping with research."
    }
  ];
  
  const offerElement = document.getElementById("research-offer");
  
  for (let i in ranges) {
    startDate = new Date(today.getFullYear(), ranges[i].start[0] - 1, ranges[i].start[1]);
    endDate = new Date(today.getFullYear(), ranges[i].end[0] - 1, ranges[i].end[1]);
    if (startDate < today && today < endDate) {
      offerElement.innerHTML = ranges[i].message;
      annotate(offerElement, ranges[i].annotation);
    }
  }
}

function getClientLocation() {
//const apiUrl = 'https://ipinfo.io/json';
const apiUrl = 'https://freegeoip.app/json/';
  fetch(apiUrl).then(function (response) {
    // The API call was successful!
    if (response.ok) {
      return response.json();
    } else {
      return Promise.reject(response);
    }
  }).then(function (data) {
    console.log(data);
    const lat = data.latitude;
    const lon = data.longitude;
    const city = data.city;
    console.log(lat);
    console.log(lon);
    console.log(city);
    return lat;
    return lon;
    return city;
  }).catch(function (err) {
    console.warn('Something went wrong.', err);
  });
}

function annotate(node, annotation) {
  node.classList.add("annotation");
  node.setAttribute("data-annotation", annotation);
  enableAnnotation(node);
}

function enableAnnotation(node) {
  node.addEventListener("click", e => {
    if(document.body.classList.contains("xray")) {
      alert(node.getAttribute("data-annotation"));
      if (!node.matches("summary")) {
        e.preventDefault();
      }
    }
  });
}

function addInitialAnnotations() {
  annotations = document.getElementsByClassName("annotation");
  for(i = 0; i < annotations.length; i++) {
    enableAnnotation(annotations[i]);
  }
}

function showTerms({coords}) {
  const lat = parseFloat(coords.latitude);
  const lon = parseFloat(coords.longitude);
  const coordinates = `${lat}|${lon}`;
  console.log(coordinates);
  let api_url = 'https://en.wikipedia.org/w/api.php';

  const params = {
    action: "query",
    list: "geosearch",
    gscoord: coordinates,
    gsradius: "10000",
    gslimit: "25",
    format: "json"
  };

  api_url = `${api_url}?origin=*`;
  Object.keys(params).forEach(key => {
    api_url += `&${key}=${params[key]}`;
  });

  fetch(api_url)
    .then(response => response.json())
    .then(({query}) => {
      // Hide loading message
      msg.style.display = 'none';
      const container = document.getElementById("terms");
      let markup = '';
      const search_url = 'http://www.worldcat.org/search?q=su:';
      const pages = query.geosearch;
      for (const page in pages) {
	markup += `<a title="${pages[page].title}" href="${search_url}${pages[page].title}">${pages[page].title}</a>`;
      }
      container.innerHTML = `${markup}`;
    })
    .catch(error => {
      console.log(error);
    });
}

function weatherOffer({coords}) {
  const lat = parseFloat(coords.latitude);
  const lon = parseFloat(coords.longitude);
  const coordinates = `${lat},${lon}`;
  console.log(coordinates);

  let api_url = `https://api.weather.gov/points/${coordinates}`;
  console.log(api_url);
  let city;
  let state;

  fetch(api_url)
    .then(response => response.json())
    .then(data => {
      // Get forecast data URL, call second fetch
      console.log(data);
      console.log(data.properties.forecastGridData);
      city = data.properties.relativeLocation.properties.city;
      state = data.properties.relativeLocation.properties.state;
      console.log(city);
      console.log(state);
      return fetch(data.properties.forecastGridData);
    })
    .then(response => response.json())
    .then(({properties}) => {
      // Work with returned forecast data
      console.log(properties);
      // Hide loading message
      msg.style.display = 'none';
      const container = document.getElementById("weather-offer");
      let markup = '';
      const cloudCover = properties.skyCover.values[13].value;
      markup = `<p>Here comes the sun in ${city} (${state}), stop in for a cup of something cool. Check out the <a href="http://www.montana.edu/ufs/menus/brewed_awakening.php">"Brewed Awakening" hours and menu</a>.`;
      if (cloudCover > 55) {
        markup = `It's cloudy and cold in ${city} (${state}), stop in for a cup of something warm. Check out the <a href="http://www.montana.edu/ufs/menus/brewed_awakening.php">"Brewed Awakening" hours and menu</a>.`;
      }
      container.innerHTML = `${markup}`;
    })
    .catch(error => {
      console.log(error)
  });
}

// Page references used by preserved functions and event wiring.
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("q");
const msg = document.getElementById("message");
const xrayToggle = document.getElementById("xraytoggle");
const progress = document.querySelector(".progress");

// Orchestration helpers for main app functions
function runSearch(q) {
  searchInput.value = q;
  const kbUrl = new URL("http://ask.lib.montana.edu/search/");
  kbUrl.searchParams.set("q", q);
  document.getElementById("kbsearch").href = kbUrl.href;

  if (!q.trim()) {
    document.querySelector("ul.result").replaceChildren();
    document.querySelector("ul.pages").replaceChildren();
    document.getElementById("result-info").textContent = "";
    document.getElementById("sort-category").textContent = "";
    document.querySelector(".results").classList.remove("returned", "none");
    document.getElementById("facets").className = "flex-facet";
    return;
  }

  document.getElementById("sort-category").textContent = "";
  // The preserved request function interpolates q into its URL directly.
  getSearchResults(encodeURIComponent(q), 10, 1, null, null);
}

function restoreSearchFromUrl() {
  const url = new URL(window.location.href);
  runSearch(url.searchParams.get("q") || "");
}

function initializeLocation() {
  if (!navigator.geolocation) {
    msg.textContent = "Location is unavailable in this browser.";
    msg.style.display = "block";
    return;
  }

  msg.style.display = "block";
  navigator.geolocation.getCurrentPosition(position => {
    showTerms(position);
    weatherOffer(position);
  }, error => {
    msg.textContent = error.code === 1
      ? "Location access was declined. Nearby topics and weather are unavailable."
      : "Unable to determine your location. Nearby topics and weather are unavailable.";
    msg.style.display = "block";
  }, { timeout: 10000, maximumAge: 300000 });
}

function updateScrollProgress() {
  const root = document.documentElement;
  const scrollableHeight = root.scrollHeight - root.clientHeight;
  const percent = scrollableHeight > 0 ? root.scrollTop / scrollableHeight * 100 : 0;
  progress.style.setProperty("--scroll", Math.min(100, Math.max(0, percent)) + "%");
}

searchForm.addEventListener("submit", event => {
  event.preventDefault();
  const q = searchInput.value;
  const url = new URL(window.location.href);
  url.searchParams.set("q", q);
  if (url.href !== window.location.href) {
    history.pushState(null, "", url);
  }
  runSearch(q);
});

window.addEventListener("popstate", restoreSearchFromUrl);
xrayToggle.addEventListener("click", () => {
  const enabled = document.body.classList.toggle("xray");
  xrayToggle.setAttribute("aria-pressed", String(enabled));
});
document.addEventListener("scroll", updateScrollProgress, { passive: true });
window.addEventListener("resize", updateScrollProgress);

addInitialAnnotations();
researchOffer();
restoreSearchFromUrl();
initializeLocation();
updateScrollProgress();