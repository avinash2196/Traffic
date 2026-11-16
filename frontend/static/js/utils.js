// General Utilities

// Debounce function
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Throttle function
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Poll API endpoint
function pollEndpoint(endpoint, callback, interval = 30000, maxAttempts = null) {
  let attempts = 0;
  
  const poll = async () => {
    attempts++;
    if (maxAttempts && attempts > maxAttempts) {
      return;
    }
    
    const result = await API[endpoint]();
    callback(result);
    
    setTimeout(poll, interval);
  };
  
  poll();
}

// Get query parameter
function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

// Set query parameter
function setQueryParam(name, value) {
  const params = new URLSearchParams(window.location.search);
  params.set(name, value);
  window.history.replaceState({}, '', `${window.location.pathname}?${params}`);
}

// Copy to clipboard
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Failed to copy:', err);
    return false;
  }
}

// Deep clone object
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

// Merge objects
function mergeObjects(obj1, obj2) {
  return { ...obj1, ...obj2 };
}

// Check if object is empty
function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

// Get random ID
function generateId() {
  return Math.random().toString(36).substr(2, 9);
}

// Retry function
async function retry(func, maxAttempts = 3, delay = 1000) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await func();
    } catch (error) {
      if (i === maxAttempts - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Wait for element
function waitForElement(selector, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const element = document.querySelector(selector);
    if (element) {
      resolve(element);
      return;
    }

    const observer = new MutationObserver(() => {
      const element = document.querySelector(selector);
      if (element) {
        observer.disconnect();
        resolve(element);
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });

    setTimeout(() => {
      observer.disconnect();
      reject(new Error(`Element ${selector} not found within ${timeout}ms`));
    }, timeout);
  });
}

// Export functions
window.UTILS = {
  debounce,
  throttle,
  pollEndpoint,
  getQueryParam,
  setQueryParam,
  copyToClipboard,
  deepClone,
  mergeObjects,
  isEmpty,
  generateId,
  retry,
  waitForElement,
};
