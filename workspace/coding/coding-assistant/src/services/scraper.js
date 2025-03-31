/**
 * Web Scraper Function
 * 
 * This function scrapes information from a website using fetch and cheerio.
 * It supports returning different types of data based on selectors.
 * 
 * @param {string} url - The URL of the website to scrape
 * @param {Object} options - Configuration options for scraping
 * @param {string|string[]} options.selectors - CSS selector(s) to extract
 * @param {boolean} options.includeHtml - Whether to include HTML in the result (default: false)
 * @param {boolean} options.asArray - Return results as array even for single selector (default: false)
 * @param {string} options.attribute - Extract specific attribute instead of text (optional)
 * @returns {Promise<string|string[]|Object>} - The scraped data
 */
async function scrapeWebsite(url, options = {}) {
  try {
    // Import dependencies (assumes cheerio is available in the environment)
    // In Node.js environment, you would use:
    // const fetch = require('node-fetch');
    // const cheerio = require('cheerio');
    
    // Default options
    const {
      selectors = 'body',
      includeHtml = false,
      asArray = false,
      attribute = null
    } = options;
    
    // Fetch the website content
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch website: ${response.status} ${response.statusText}`);
    }
    
    const html = await response.text();
    
    // Load HTML into cheerio
    const $ = cheerio.load(html);
    
    // Handle different selector types
    if (Array.isArray(selectors)) {
      // Multiple selectors provided, return an object with results for each selector
      const results = {};
      
      selectors.forEach(selector => {
        results[selector] = extractData($, selector, { includeHtml, attribute });
      });
      
      return results;
    } else {
      // Single selector provided
      const result = extractData($, selectors, { includeHtml, attribute });
      return asArray ? [result] : result;
    }
  } catch (error) {
    console.error('Scraping error:', error);
    throw error;
  }
}

/**
 * Helper function to extract data based on selector
 * 
 * @param {Object} $ - Cheerio instance
 * @param {string} selector - CSS selector
 * @param {Object} options - Extraction options
 * @returns {string|string[]} - Extracted data
 */
function extractData($, selector, { includeHtml, attribute }) {
  const elements = $(selector);
  
  if (elements.length > 1) {
    return elements.map((_, el) => {
      const $el = $(el);
      if (attribute) {
        return $el.attr(attribute);
      }
      return includeHtml ? $el.html() : $el.text().trim();
    }).get();
  } else if (elements.length === 1) {
    if (attribute) {
      return elements.attr(attribute);
    }
    return includeHtml ? elements.html() : elements.text().trim();
  }
  
  return null;
}

// Example usage:
/*
// Simple text extraction
scrapeWebsite('https://example.com', {
  selectors: 'h1'
}).then(title => console.log('Page title:', title));

// Multiple selectors
scrapeWebsite('https://example.com', {
  selectors: ['h1', 'p', '.main-content']
}).then(results => console.log('Extracted data:', results));

// Extract attributes
scrapeWebsite('https://example.com', {
  selectors: 'a',
  attribute: 'href',
  asArray: true
}).then(links => console.log('All links:', links));
*/