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
    # Initialize dictionary of all pages with 0 probability
    out = {}
    for p in corpus:
        out[p] = 0

    # Check if there are direct links
    if corpus[page]:
        # Add probability of direct transition
        directLinks = corpus[page]

        for link in directLinks:
            out[link] = (1/len(directLinks)) * damping_factor

        # Add probability of random transition
        randomChance = (1-damping_factor) / len(out)
        for p in out:
            out[p] += randomChance
    else:
        for p in out:
            out[p] += 1/len(out)

    return out


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    currentPage = [random.choice(list(corpus.keys()))]

    transitions = {}  # Dictionary of pages to keep track of times pages visited
    for page in corpus.keys():
        transitions[page] = 0

    for i in range(n):
        currentTransitionModel = transition_model(corpus, currentPage[0], DAMPING)

        currentPage = random.choices(list(currentTransitionModel.keys()), weights=list(currentTransitionModel.values()))

        transitions[currentPage[0]] += 1

    N = sum(transitions.values())

    for page in transitions:
        transitions[page] /= N

    return transitions
    # COMMENTED THIS OUT DUE TO FLOATING POINT IMPRECISION
    # if sum(transitions.values()) == 1:
    #     return transitions
    # else:
    #     print("SUM OF TRANSITION VALUES,", sum(transitions.values()))
    #     raise ValueError("<<sample pagerank function>>\n PR values dont add up to one")


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # FORMULA
    # PR = (1-d)/N + d*E
    # E = i{ PR/NumLinks  }

    # Setting values for ease of use
    d = damping_factor
    N = len(corpus)

    # Initializing PageRanks
    PageRanks = {x: (1/N) for x in corpus.keys()}

    while True:
        differenceFlag = False

        # Loop over each page
        for currentPage in PageRanks:
            sigma = 0
            # Loop over all pages
            for incoming in corpus:
                # If no links add to sigma
                if not corpus[incoming]:
                    sigma += PageRanks[incoming] / N

                # If page links to current page add to sigma
                if currentPage in corpus[incoming]:
                    sigma += PageRanks[incoming] / len(corpus[incoming])

            # Use formula
            newPageRank = (1-d)/N + (d*sigma)

            difference = PageRanks[currentPage] - newPageRank

            PageRanks[currentPage] = newPageRank

            # Set flag if any page rank changed by more than 0.001
            if abs(difference) > 0.001:
                differenceFlag = True

        if not differenceFlag:
            break

    return PageRanks


if __name__ == "__main__":
    main()
