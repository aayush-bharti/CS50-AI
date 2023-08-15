import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    #creates variable to store the probabilities in
    probability_dist = {}
    current_links = corpus[page]
    num_links = len(current_links)
    
    #if there are no links, divide the probabilities equally between all pages
    if num_links == 0:
        for pages in corpus:
            probability_dist[pages] = 1/len(corpus)
    
    else:
        #for all the possible pages, divide the probability equally so that it will randomly choose out of all the pages
        for pages in corpus:
            probability_dist[pages] = (1 - damping_factor)/len(corpus)
            #if the page is in the links of the current page, add the probability of randomly choosing one of the linked pages
            if pages in current_links:
                probability_dist[pages] += damping_factor/num_links      

    return probability_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    #stores the pageranks
    pagerank = {}
    
    #sets them all equal to 0 at the start 
    for pages in corpus:
        pagerank[pages] = 0
    
    #randomly chooses a page to sample
    current_page = random.choice(list(pagerank))

    #loop through n times
    for i in range(1, n):
        #add the visit to the pagerank of the page
        pagerank[current_page] += 1/n
        #call the transition model function to get probabilities and then randomly choose the next page based off that
        weights = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(weights), weights.values())[0]
        
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    #create variables for the old pagerank and new pagerank
    old_pagerank = {}
    new_pagerank = {}
    boolean = True
    N = len(corpus)
    
    #set the pageranks equally dividing by the total number of pages
    for pages in corpus:
        old_pagerank[pages] = 1/N
 
    #loop through the pageranks
    while boolean:
        boolean = False
        #loops through all the pages
        for pages in corpus:
            total_sum = 0
            for links in corpus:
                #if the page has no links at all, that means there is a link for each page
                if len(corpus[links]) == 0:
                    total_sum += old_pagerank[links]/N
                #if the page is in the links, use the formula to calculate the value of the sum
                if pages in corpus[links]:
                    num_links = len(corpus[links])
                    total_sum += old_pagerank[links]/num_links

            #update the pagerank by completing the formula and multiplying the sum by the damping factor
            new_pagerank[pages] = (1 - damping_factor)/N + (damping_factor * total_sum)
            
            #if the difference between the old and new pagerank is higher than 0.001, make boolean true so that the while loop continues
            if abs(new_pagerank[pages] - old_pagerank[pages]) > 0.001:
                boolean = True
            #update the old pagerank values
            old_pagerank[pages] = new_pagerank[pages]
        
    
    return old_pagerank
        
        
if __name__ == "__main__":
    main()
